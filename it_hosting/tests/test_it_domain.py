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

from odoo.tests.common import TransactionCase


class TestItDomain(TransactionCase):

    def setUp(self):
        super(TestItDomain, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.hosting_env = self.env['it.hosting']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

    def test_compute_count_hosting(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })
        self.hosting_env.create({
            'name': 'Hosting 1',
            'domain_id': domain_1.id
        })
        self.hosting_env.create({
            'name': 'Hosting 2',
            'domain_id': domain_1.id
        })

        self.assertEqual(domain_1.number_of_hosting, 2)

    def test_open_hosting(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })

        action = domain_1.open_hosting()
        self.assertEqual(action['xml_id'], 'it_hosting.it_hosting_action')
