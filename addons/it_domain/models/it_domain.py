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
import logging
import socket
import ssl
from datetime import date, datetime

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'


class InfrastructureDomain(models.Model):
    _name = 'it.domain'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Domain Name'

    name = fields.Char(string="Domain", required=True, index=True)
    description = fields.Text()
    customer_id = fields.Many2one(
        'res.partner',
        string="Customer",
        context="{'res_partner_search_mode': 'customer'}")
    date_expiration = fields.Date(string="Expiration Date")
    is_expired = fields.Boolean(compute='_compute_is_expired', tracking=True)

    verify_certificate_validity = fields.Boolean(index=True)
    is_certificate_expired = fields.Boolean(tracking=True)
    certificate_expire_on = fields.Date()
    certificate_ocsp = fields.Char(
        help="TLS Certificate Status Request Extension")
    certificate_generate_by = fields.Char()

    active = fields.Boolean(default=True, index=True)

    technical_contact_id = fields.Many2one(
        'res.partner', index=True, string="Technical Contact")

    internal_note = fields.Text(string="Note")
    system = fields.Boolean(help="By exemple server domain", index=True)

    dnsbelgium_url = fields.Char(
        string="Dns Belgium", compute='_compute_dnsbelgium_url')

    eurid_url = fields.Char(
        string="Eurid", compute='_compute_eurid_url')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Technical name already exists !"),
    ]

    def _compute_is_expired(self):
        for record in self:

            if not record.date_expiration:
                record.is_expired = False
                continue

            record.is_expired = fields.Date.from_string(
                record.date_expiration) <= date.today()

    def action_verify_ssl_validity(self):
        for record in self:
            if not record.verify_certificate_validity:
                record.is_certificate_expired = False
                continue

            ssl_info = self.getcert(record.name)

            if not ssl_info:
                record.is_certificate_expired = False
                return False

            record.certificate_expire_on = datetime.strptime(
                ssl_info['notAfter'], ssl_date_fmt)
            record.certificate_ocsp = ssl_info['OCSP'][0]
            record.certificate_generate_by = ssl_info['caIssuers'][0]

            today = date.today()
            if record.certificate_expire_on <= today:
                record.is_certificate_expired = True
            else:
                record.is_certificate_expired = False

    def _compute_dnsbelgium_url(self):
        url = 'https://www.dnsbelgium.be/fr/whois/info/%s/details'
        for record in self:
            record.dnsbelgium_url = url % record.name

    def _compute_eurid_url(self):
        url = 'https://whois.eurid.eu/en/?domain=%s'
        for record in self:
            record.eurid_url = url % record.name

    @api.model
    def _needaction_domain_get(self):
        return []

    @api.model
    def getcert(self, hostname, port=443, timeout=3.0):  # pragma: no cover
        """Retrieve server's certificate at the specified address (host, port)
        ."""
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=hostname,
        )
        conn.settimeout(3.0)

        try:
            conn.connect((hostname, port))
            return conn.getpeercert()
        except ssl.SSLError:
            _logger.error(_("Certificate verify failed: %s ") % hostname)

        return False

    def _track_template(self, changes):
        res = super(InfrastructureDomain, self)._track_template(changes)
        test_domain = self[0]
        if 'is_certificate_expired' in changes and \
                test_domain.is_certificate_expired:

            template_id = self.env.ref(
                'it_domain.email_template_domain_expired')
            res['is_certificate_expired'] = (template_id, {
                'auto_delete_message': True,
                'subtype_id': self.env['ir.model.data'].xmlid_to_res_id(
                    'mail.mt_note'),
                'email_layout_xmlid': 'mail.mail_notification_light'
            })
        return res
