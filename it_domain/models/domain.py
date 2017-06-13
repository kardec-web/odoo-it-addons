# -*- coding: utf-8 -*-
from openerp import models, fields, api
import datetime


class InfrastructureDomain(models.Model):
    _name = 'it.domain'
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Domain", required=True, index=True)
    description = fields.Text(string="Description")
    customer = fields.Many2one('res.partner', string="Customer",
                               domain="[('customer', '=', True)]", context="{'default_customer':1}")
    date_expiration = fields.Date(string="Expiration Date")
    is_expired = fields.Boolean(string="Is Expired", compute='_is_expired')

    active = fields.Boolean('Active', default=True, index=True)

    technical_contact = fields.Many2one(
        'res.partner', tring="Technical Contact", index=True)

    internal_note = fields.Text(string="Note")

    state = fields.Selection(
        [('active', 'Active'), ('expired', 'Expired')], string="State", default="active")

    @api.multi
    def _is_expired(self):
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

    @api.model
    def _needaction_domain_get(self):
        return []
