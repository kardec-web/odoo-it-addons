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


class InfrastructureMailboxAlias(models.Model):
    _name = 'it.mailbox.alias'

    email = fields.Char(string='From', compute='_compute_display_name')
    name = fields.Char(string="Alias", required=True)
    domain = fields.Many2one('it.domain', required=True)
    goto = fields.Char(string="Go To", required=True)
    active = fields.Boolean(default=True, index=True)

    @api.multi
    @api.depends('name', 'domain.name')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.domain:
                record.email = record.name + '@' + record.domain.name
