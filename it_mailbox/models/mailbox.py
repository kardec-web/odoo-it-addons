# -*- coding: utf-8 -*-
from openerp import _, models, fields, api
from openerp.exceptions import ValidationError


class InfrastructureMailbox(models.Model):
    _name = 'it.mailbox'

    email = fields.Char(
        string='E-mail', compute='_compute_display_name')
    name = fields.Char(string="Username", required=True, index=True)
    domain = fields.Many2one('it.domain', string="Domain", required=True)

    description = fields.Text(string="Description")
    active = fields.Boolean('Active', default=True, index=True)

    # Maybe is not required here
    password = fields.Char(string="Password")
    maildir = fields.Char(string="Maildir")
    quota = fields.Integer(string="Quota")
    quota_used = fields.Integer(string="Quota used")
    number_of_emails = fields.Integer(string="Number of message in mailbox")

    @api.one
    @api.depends('name', 'domain.name')
    def _compute_display_name(self):
        if self.name and self.domain:
            self.email = self.name + '@' + self.domain.name

    @api.multi
    @api.constrains('domain')
    def _check_max_mailboxes_limit(self):
        for record in self:
            if record.domain.max_mailbox > 0 and record.domain.max_mailbox and record.domain.max_mailbox < len(record.domain.mailboxes):
                raise ValidationError(
                    _('No more mailbox available for this domain.'))
