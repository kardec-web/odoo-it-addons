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


class InfrastructureServer(models.Model):
    _name = 'it.server'
    _inherit = ['mail.thread']

    name = fields.Char(required=True, compute='_compute_name')
    friendly_name = fields.Char()
    os = fields.Char()
    domain_id = fields.Many2one('it.domain', string="Hostname", required=True)
    technical_domain_id = fields.Many2one(
        'it.domain', string="Technical (Hostname)")
    active = fields.Boolean(default=True, index=True)
    vm_id = fields.Char()
    server_type = fields.Selection([
        ('dedicated', 'Dedicated'),
        ('virtual', 'Virtual'),
    ], string='Type', required=True)

    parent_id = fields.Many2one(
        'it.server', domain="[('server_type', '=', 'dedicated')]")
    tag_ids = fields.Many2many(
        'it.server.tag', 'server_tags_rel', 'server_id', 'tag_id',
        string='Tags')

    ip_ids = fields.One2many(
        'it.server.ip', 'server_id', string="IPs")

    @api.depends('domain_id')
    @api.multi
    def _compute_name(self):
        for server in self:
            server_name = ''
            if server.friendly_name:
                server_name += server.friendly_name

            if server.domain_id:
                if server.friendly_name:
                    server_name += " - "
                server_name += server.domain_id.name

            server.name = server_name
