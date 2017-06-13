# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _


class InfrastructureDomain(models.Model):
    _inherit = 'it.domain'

    mailboxes = fields.One2many('it.mailbox', 'domain', string="Mailboxes")
    alias = fields.One2many(
        'it.mailbox.alias', 'domain', string="Mailbox Alias")

    has_mailbox = fields.Boolean(string="Has Mailbox")
    mailbox_quota = fields.Integer(string="Quota")
    mailbox_max_quota = fields.Integer(string="Max Quota")
    max_mailbox = fields.Integer(string="Maximum mailboxes allowed")
    number_of_mailbox = fields.Integer(
        string="Number of mailbox", compute="count_mailbox")
    number_of_alias = fields.Integer(
        string="Number of alias", compute="count_alias")

    mailbox_technical_contact = fields.Many2one(
        'res.partner', string="Technical Contact (Mailbox)", index=True)

    # transport = fields.Char(string="Transport")

    @api.multi
    def count_mailbox(self):
        for record in self:
            if record.id:
                record.number_of_mailbox = record.env[
                    'it.mailbox'].search_count([('domain', '=', record.id)])

    @api.multi
    def count_alias(self):
        for record in self:
            if record.id:
                record.number_of_alias = record.env[
                    'it.mailbox.alias'].search_count([('domain', '=', record.id)])

    @api.multi
    def open_mailboxes(self):
        """ open mailboxes view """

        domain = self[0]
        help = _(
            """<p class="oe_view_nocontent_create">Create a new mailbox for  '%s'.</p>""") % (domain.name,)
        # view = self.env.ref('it_mailbox.it_mailbox_tree')
        action = self.env.ref('it_mailbox.it_mailbox_action').read()[0]
        action['help'] = help
        action['context'] = {
            'search_default_domain': [domain.id],
        }

        return action

    @api.multi
    def open_aliases(self):
        """ open aliases view """

        domain = self[0]
        help = _(
            """<p class="oe_view_nocontent_create">Create a new alias for  '%s'.</p>""") % (domain.name,)
        # view = self.env.ref('it_mailbox.it_mailbox_tree')
        action = self.env.ref('it_mailbox.it_mailbox_alias_action').read()[0]
        action['help'] = help
        action['context'] = {
            'search_default_domain': [domain.id],
        }

        return action
