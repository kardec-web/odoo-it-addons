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
from datetime import date, datetime, timedelta

from mock import patch
from odoo import fields
from odoo.addons.it_domain.models.it_domain import ssl_date_fmt
from odoo.tests.common import TransactionCase
from psycopg2 import IntegrityError


class TestItDomain(TransactionCase):

    def setUp(self):
        super(TestItDomain, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

        # Patch get_cert method
        def getcert(hostname, port=443, timeout=3.0):
            if hostname == 'no_ssl':
                return False

            notafter = date.today() - timedelta(1)
            if hostname == 'future-url':
                notafter = date.today() + timedelta(1)

            return {
                'notAfter': notafter.strftime(ssl_date_fmt) + ' UTC',
                'OCSP': ['http://OCSP.test'],
                'caIssuers': ['http://caIssuers.test'],
            }

        patcher = patch(
            'odoo.addons.it_domain.models.'
            'it_domain.InfrastructureDomain.getcert',
            wraps=getcert
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_unique_name(self):
        self.domain_env.create({
            'name': 'domain-1.test'
        })

        with self.assertRaises(IntegrityError):
            self.domain_env.create({
                'name': 'domain-1.test'
            })

    def test_is_expired(self):
        yesterday = date.today() - timedelta(1)
        tomorrow = date.today() + timedelta(1)
        today = date.today()

        domain_1 = self.domain_env.create({
            'name': 'domain-1.test',
            'date_expiration': fields.Date.to_string(yesterday)
        })

        domain_2 = self.domain_env.create({
            'name': 'domain-2.test',
            'date_expiration': fields.Date.to_string(tomorrow)
        })

        domain_3 = self.domain_env.create({
            'name': 'domain-3.test',
            'date_expiration': fields.Date.to_string(today)
        })

        domain_4 = self.domain_env.create({
            'name': 'domain-4.test',
        })

        self.assertTrue(domain_1.is_expired)
        self.assertTrue(domain_3.is_expired)
        self.assertFalse(domain_2.is_expired)
        self.assertFalse(domain_4.is_expired)

    def test_action_verify_ssl_validity(self):
        all_domains = self.domain_env
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test',
            'verify_certificate_validity': False
        })

        domain_2 = self.domain_env.create({
            'name': 'future-url',
            'verify_certificate_validity': True
        })

        domain_3 = self.domain_env.create({
            'name': 'past-url',
            'verify_certificate_validity': True
        })

        domain_4 = self.domain_env.create({
            'name': 'no_ssl',
            'verify_certificate_validity': True
        })

        all_domains = domain_1 + domain_2 + domain_3 + domain_4

        all_domains.action_verify_ssl_validity()

        self.assertFalse(domain_1.is_certificate_expired)
        self.assertFalse(domain_2.is_certificate_expired)
        self.assertTrue(domain_3.is_certificate_expired)
        self.assertFalse(domain_4.is_certificate_expired)

        date_expected = (date.today() + timedelta(1)).strftime(
            ssl_date_fmt) + ' UTC'
        date_expected = datetime.strptime(date_expected, ssl_date_fmt).date()

        self.assertEqual(domain_2.certificate_expire_on, date_expected)
        self.assertEqual(domain_2.certificate_ocsp, 'http://OCSP.test')
        self.assertEqual(
            domain_2.certificate_generate_by, 'http://caIssuers.test')

    def test_needaction_domain_get(self):
        self.assertEqual(self.domain_env._needaction_domain_get(), [])

    def test_compute_dnsbelgium_url(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })

        dns_belgium_url = 'https://www.dnsbelgium.be/fr/whois/info/' + \
            'domain-1.test/details'
        self.assertEqual(domain_1.dnsbelgium_url, dns_belgium_url)

    def test_compute_eurid_url(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })
        eurid_url = u'https://whois.eurid.eu/en/' + \
            u'?domain=domain-1.test'
        self.assertEqual(domain_1.eurid_url, eurid_url)
