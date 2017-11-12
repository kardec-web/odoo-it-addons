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
import datetime


class InfrastructureDomain(models.Model):
    _name = 'it.domain'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Domain", required=True, index=True)
    description = fields.Text()
    customer = fields.Many2one('res.partner',
                               domain="[('customer', '=', True)]",
                               context="{'default_customer':1}")
    date_expiration = fields.Date(string="Expiration Date")
    is_expired = fields.Boolean(compute='_compute_is_expired')

    active = fields.Boolean(default=True, index=True)

    technical_contact = fields.Many2one(
        'res.partner', index=True)

    internal_note = fields.Text(string="Note")
    system = fields.Boolean(help="By exemple server domain", index=True)

    state = fields.Selection([
        ('active', 'Active'),
        ('expired', 'Expired')
    ], default="active")

    dnsbelgium_url = fields.Char(
        string="Dns Belgium", compute='_compute_dnsbelgium_url')

    eurid_url = fields.Char(
        string="Eurid", compute='_compute_eurid_url')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Technical name already exists !"),
    ]

    @api.multi
    def _compute_is_expired(self):
        for record in self:
            record.is_expired = fields.Date.from_string(
                record.toDate) < datetime.date.today()

    @api.multi
    def action_active(self):
        for record in self:
            record.state = 'active'

    @api.multi
    def action_expired(self):
        for record in self:
            record.state = 'expired'

    @api.multi
    def _compute_dnsbelgium_url(self):
        for record in self:
            record.dnsbelgium_url = u'https://www.dnsbelgium.be/fr/' + \
                u'nom_de_domaine/disponibilité#/das/%s' % record.name

    @api.multi
    def _compute_eurid_url(self):
        for record in self:
            record.eurid_url = u'https://whois.eurid.eu/en/' + \
                u'?domain=%s' % record.name

    @api.model
    def _needaction_domain_get(self):
        return []
