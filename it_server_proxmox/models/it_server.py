# -*- coding: utf-8 -*-
##############################################################################
#
#    Kardec
#    Copyright (C) 2016-Today Kardec (<http://www.kardec.net>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from proxmoxer import ProxmoxAPI
from proxmoxer.backends.https import AuthenticationError
from proxmoxer.core import ResourceException
from paramiko.ssh_exception import AuthenticationException
from requests.exceptions import ConnectionError

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class InfrastructureServer(models.Model):
    _inherit = 'it.server'

    has_proxmox_os = fields.Boolean(string="Proxmox Server", index=True)

    proxmox_host = fields.Char(index=True)
    proxmox_port = fields.Integer(default=8006)
    proxmox_user = fields.Char()
    proxmox_password = fields.Char()
    proxmox_vm_type = fields.Selection([
        ('openvz', 'openvz'),
        ('lxc', 'lxc'),
    ])
    proxmox_protocol = fields.Selection([
        ('https', 'https')
    ], default="https")
    proxmox_url = fields.Char(compute='_compute_proxmox_url')

    @api.multi
    def _compute_proxmox_url(self):
        for record in self:
            record.proxmox_url = u'https://%s:%s' % (
                record.proxmox_host, record.proxmox_port)

    @api.model
    def fetch_promox_vms_cron(self):
        _logger.info("Begin Fetching proxmox VMs")

        it_server_env = self.env['it.server'].sudo()
        servers = it_server_env.search([
            ('proxmox_host', '!=', False),
            ('proxmox_vm_type', '!=', False),
        ])

        _logger.info("%d vms to fetch", len(servers))

        for proxmox in servers:
            proxmox_api = self._get_proxmox_api(proxmox)

            has_lxc = False
            has_openvz = False
            if proxmox.proxmox_vm_type:
                has_openvz = proxmox.proxmox_vm_type == 'openvz'
                has_lxc = proxmox.proxmox_vm_type == 'lxc'

            for node in proxmox_api.nodes.get():
                vms = []
                if has_openvz:
                    vms += self._get_openvz_vm(proxmox_api, node)

                if has_lxc:
                    vms += self._get_lxc_vm(proxmox_api, node)

                for vm in vms:
                    self._create_vm(vm, proxmox)

        _logger.info("Fetching proxmox VMs finished")

    def _create_vm(self, vm, proxmox_server):
        server = False
        server_env = self.env['it.server'].sudo()
        domain_env = self.env['it.domain'].sudo()
        server_ip_env = self.env['it.server.ip'].sudo()

        vm_domain = vm['name']
        domain = domain_env.search([
            ('name', '=', vm_domain)
        ])
        if domain:
            server = server_env.search(
                [('technical_domain_id', '=', domain.id)])

        values = {
            'last_synchronisation': fields.Datetime.now(),
            'server_type': 'virtual',
            'vm_id': vm['vmid'],
            'cpu': vm['cpus'],
            'memory': vm['maxmem'] / 1024 / 1024 / 1024,
            'disk': vm['maxdisk'] / 1024 / 1024 / 1024,
            'parent_id': proxmox_server.id,
        }

        if server:
            server.write(values)
        else:
            domain_id = domain_env.create({
                'name': vm_domain,
            }).id

            values['technical_domain_id'] = domain_id
            values['domain_id'] = domain_id
            server = server_env.create(values)

        server_ips = server_ip_env.search([
            ('server_id', '=', server.id),
        ])
        server_ips = [server_ip.name for server_ip in server_ips]
        if vm['ip'] not in server_ips:
            server_ip_env.create({
                'name': vm['ip'],
                'server_id': server.id,
            })

    def _get_proxmox_api(self, proxmox_server):
        try:
            return ProxmoxAPI(proxmox_server.proxmox_host,
                              user=proxmox_server.proxmox_user,
                              port=proxmox_server.proxmox_port,
                              password=proxmox_server.proxmox_password,
                              verify_ssl=False,
                              backend=proxmox_server.proxmox_protocol)
        except AuthenticationError:
            _logger.error(
                "Can't connect to %s (user or password invalid)",
                proxmox_server.proxmox_host)
            return False
        except ConnectionError:
            _logger.error(
                "Can't connect to %s",
                proxmox_server.proxmox_host)
            return False
        except AuthenticationException:
            _logger.error(
                "Authentification error to %s",
                proxmox_server.proxmox_host)
            return False

    def _get_openvz_vm(self, proxmox_api, node):
        try:
            return proxmox_api.nodes(node['node']).openvz.get()
        except ResourceException:
            return []

    def _get_lxc_vm(self, proxmox_api, node):
        try:
            return proxmox_api.nodes(node['node']).lxc.get()
        except ResourceException:
            return []
