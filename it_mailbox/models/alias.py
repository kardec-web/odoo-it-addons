# -*- coding: utf-8 -*-
from openerp import models, fields, api


class InfrastructureMailboxAlias(models.Model):
    _name = 'it.mailbox.alias'

    email = fields.Char(string='From', compute='_compute_display_name')
    name = fields.Char(string="Alias", required=True)
    domain = fields.Many2one('it.domain', string="Domain", required=True)
    goto = fields.Char(string="Go To", required=True)
    active = fields.Boolean('Active', default=True, index=True)

    @api.one
    @api.depends('name', 'domain.name')
    def _compute_display_name(self):
        if self.name and self.domain:
            self.email = self.name + '@' + self.domain.name
