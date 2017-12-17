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


class InfrastructureServer(models.Model):
    _inherit = 'it.server'

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    estimate_cost_ids = fields.One2many(
        'it.estimate.cost', 'server_id', string="Estimate Cost(s)")

    estimate_cost_total = fields.Monetary(
        compute="_compute_estimate_cost_total", default=0, store=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        required=True, readonly=True,
        default=_default_currency,
        track_visibility='always')

    @api.multi
    @api.depends('estimate_cost_ids')
    def _compute_estimate_cost_total(self):
        for record in self:
            if record.estimate_cost_ids:
                for estimate_cost in record.estimate_cost_ids:
                    record.estimate_cost_total += estimate_cost.estimate_cost
