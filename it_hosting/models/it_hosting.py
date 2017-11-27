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
from openerp import models, fields, api


class InfrastructureHosting(models.Model):
    _name = 'it.hosting'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    domain_id = fields.Many2one('it.domain', string="Hostname", required=True)
    active = fields.Boolean(default=True, index=True)
    hosting_type = fields.Selection([
        ('web', 'Web'),
    ], string='Type', required=True, index=True, default='web')

    note = fields.Html()
    disk_size = fields.Integer(string="Disk size (GB)")
    os = fields.Char()

    date_creation = fields.Date(string="Creation Date", index=True)
    date_expiration = fields.Date(string="Expiration Date", index=True)

    resource_type = fields.Selection([
        ('shared', 'Shared'),
        ('dedicated', 'Dedicated'),
    ], string='Type', required=True, index=True, default='shared')

    ip_ids = fields.One2many(
        'it.server.ip', 'hosting_id', string="IPs")

    domains_ids = fields.One2many(
        'it.domain', 'hosting_id', string="Domains and Subdomains")

    links_ids = fields.One2many(
        'it.link', 'hosting_id', string="Links")

    environment = fields.Selection([
        ('development', 'Development'),
        ('production', 'Production'),
    ])

    @api.multi
    def write(self, values):
        server_ip_env = self.env['it.server.ip']
        links_env = self.env['it.link']
        domain_env = self.env['it.domain']
        for record in self:
            if 'active' in values:
                server_ip_env.search([
                    ('hosting_id', '=', record.id),
                    '|',
                    ('active', '=', True),
                    ('active', '=', False),
                ]).write({
                    'active': values['active']
                })
                links_env.search([
                    ('hosting_id', '=', record.id),
                    '|',
                    ('active', '=', True),
                    ('active', '=', False),
                ]).write({
                    'active': values['active']
                })
                domain_env.search([
                    ('hosting_id', '=', record.id),
                    '|',
                    ('active', '=', True),
                    ('active', '=', False),
                ]).write({
                    'active': values['active']
                })
        return super(InfrastructureHosting, self).write(values)
