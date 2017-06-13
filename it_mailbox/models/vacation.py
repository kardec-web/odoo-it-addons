# -*- coding: utf-8 -*-
from openerp import models, fields, api


class OVHVacation(models.Model):
    _name = 'it.mailbox.vacation'

    name = fields.Char(string="Subject")
    active = fields.Boolean('Active', default=True, index=True)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ])
    domain = fields.Many2one('it.domain', string="Domain", required=True)
    # If not from_mailbox, the vacation is for an alias
    from_mailbox = fields.Boolean(
        string="From mailbox ?", default=True)
    mailbox = fields.Many2one('it.mailbox', string="Mailbox")
    alias = fields.Many2one('it.mailbox.alias', string="Alias")

    active_from = fields.Datetime(string="Active From")
    active_until = fields.Datetime(string="Active Until")

    body = fields.Html(string="Body")

    @api.onchange('domain', 'from_mailbox')
    def domain_changed(self):
        return {'domain': {
            'mailbox': [('domain', '=', self.domain.id)],
            'alias': [('domain', '=', self.domain.id)]
        }}
