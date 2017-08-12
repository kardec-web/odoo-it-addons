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


class OVHVacation(models.Model):
    _name = 'it.mailbox.vacation'

    name = fields.Char(string="Subject")
    active = fields.Boolean(default=True, index=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ])
    domain = fields.Many2one('it.domain', required=True)
    # If not from_mailbox, the vacation is for an alias
    from_mailbox = fields.Boolean(
        string="From mailbox ?", default=True)
    mailbox = fields.Many2one('it.mailbox')
    alias = fields.Many2one('it.mailbox.alias')

    active_from = fields.Datetime()
    active_until = fields.Datetime()

    body = fields.Html()

    @api.onchange('domain', 'from_mailbox')
    def domain_changed(self):
        return {'domain': {
            'mailbox': [('domain', '=', self.domain.id)],
            'alias': [('domain', '=', self.domain.id)]
        }}
