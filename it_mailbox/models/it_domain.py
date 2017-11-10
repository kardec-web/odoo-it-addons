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

    mailboxes = fields.One2many('it.mailbox', 'domain')
    alias = fields.One2many(
        'it.mailbox.alias', 'domain', string="Mailbox Alias")

    has_mailbox = fields.Boolean()
    mailbox_quota = fields.Integer(string="Quota")
    mailbox_max_quota = fields.Integer(string="Max Quota")
    max_mailbox = fields.Integer(string="Maximum mailboxes allowed")
    number_of_mailbox = fields.Integer(compute="_compute_count_mailbox")
    number_of_alias = fields.Integer(compute="_compute_count_alias")

    mailbox_technical_contact = fields.Many2one(
        'res.partner', string="Technical Contact (Mailbox)", index=True)

    @api.multi
    def _compute_count_mailbox(self):
        for record in self:
            if record.id:
                record.number_of_mailbox = record.env[
                    'it.mailbox'].search_count([('domain', '=', record.id)])

    @api.multi
    def _compute_count_alias(self):
        alias_env = self.env['it.mailbox.alias']
        for record in self:
            if record.id:
                record.number_of_alias = alias_env.search_count([
                    ('domain', '=', record.id)
                ])

    @api.multi
    def open_mailboxes(self):
        """ open mailboxes view """

        domain = self[0]
        help = _(
            """<p class="oe_view_nocontent_create">Create a new mailbox for
              '%s'.</p>""") % (domain.name,)
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
            """<p class="oe_view_nocontent_create">Create a new alias for
             '%s'.</p>""") % (domain.name,)
        # view = self.env.ref('it_mailbox.it_mailbox_tree')
        action = self.env.ref('it_mailbox.it_mailbox_alias_action').read()[0]
        action['help'] = help
        action['context'] = {
            'search_default_domain': [domain.id],
        }

        return action
