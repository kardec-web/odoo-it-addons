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
from odoo import api, fields, models


class EstimateCost(models.Model):
    _name = "it.estimate.cost"
    _order = "estimate_cost"
    _description = "Infrastructure Estimate Cost"

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    name = fields.Char(required=True, index=True)
    active = fields.Boolean(default=True, index=True)
    estimate_cost = fields.Monetary(currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        required=True, readonly=True,
        default=_default_currency,
        track_visibility='always')
