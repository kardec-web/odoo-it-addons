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
from odoo import models, fields, api
from odoo.tools.translate import _


class InfrastructureServer(models.Model):
    _inherit = 'it.server'

    hosting_ids = fields.One2many(
        'it.hosting', 'server_id', string="Hostings")

    number_of_hosting = fields.Integer(compute="_compute_count_hosting")

    @api.multi
    def _compute_count_hosting(self):
        it_hosting_env = self.env['it.hosting']
        for record in self:
            if record.id:
                record.number_of_hosting = it_hosting_env.search_count([
                    ('server_id', '=', record.id)
                ])

    @api.multi
    def open_hosting(self):
        """ open mailboxes view """

        server = self[0]
        help = _(
            """<p class="oe_view_nocontent_create">Create a new hosting for
              '%s'.</p>""") % (server.name,)

        action = self.env.ref('it_hosting.it_hosting_action').read()[0]
        action['help'] = help
        action['context'] = {
            'search_default_server_id': [server.id],
        }

        return action
