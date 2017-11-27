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
from datetime import date, timedelta
from psycopg2 import IntegrityError

from odoo.tests.common import TransactionCase
from odoo import fields


class TestItDomain(TransactionCase):

    def setUp(self):
        super(TestItDomain, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

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

        self.assertTrue(domain_1.is_expired)
        self.assertTrue(domain_3.is_expired)
        self.assertFalse(domain_2.is_expired)

    def test_active(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })
        domain_1.action_active()
        self.assertEqual(domain_1.state, 'active')

    def test_expired(self):
        domain_2 = self.domain_env.create({
            'name': 'domain-2.test'
        })
        domain_2.action_expired()

        self.assertEqual(domain_2.state, 'expired')

    def test_needaction_domain_get(self):
        self.assertEqual(self.domain_env._needaction_domain_get(), [])

    def test_compute_dnsbelgium_url(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })
        dns_belgium_url = u'https://www.dnsbelgium.be/fr/' + \
            u'nom_de_domaine/disponibilité#/das/domain-1.test'
        self.assertEqual(domain_1.dnsbelgium_url, dns_belgium_url)

    def test_compute_eurid_url(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })
        eurid_url = u'https://whois.eurid.eu/en/' + \
            u'?domain=domain-1.test'
        self.assertEqual(domain_1.eurid_url, eurid_url)
