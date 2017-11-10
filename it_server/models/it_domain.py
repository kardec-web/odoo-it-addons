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
from openerp.tools.translate import _


class InfrastructureDomain(models.Model):
    _inherit = 'it.domain'

    server_ids = fields.One2many('it.server', 'domain_id')
    has_server = fields.Boolean()
    number_of_server = fields.Integer(compute="_compute_count_server")

    @api.multi
    def _compute_count_server(self):
        it_server_env = self.env['it.server']
        for record in self:
            if record.id:
                record.number_of_server = it_server_env.search_count(
                    [('domain_id', '=', record.id)])

    @api.multi
    def open_server(self):
        """ open server view """

        domain = self[0]
        help = _(
            """<p class="oe_view_nocontent_create">Create a new server for
              '%s'.</p>""") % (domain.name,)

        action = self.env.ref('it_server.it_server_action').read()[0]
        action['help'] = help
        action['context'] = {
            'search_default_domain_id': [domain.id],
        }

        return action
