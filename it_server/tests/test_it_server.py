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


class TestItServer(TransactionCase):

    def setUp(self):
        super(TestItServer, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.server_env = self.env['it.server']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

    def test_default_owner(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })

        server_1 = self.server_env.create({
            'domain_id': domain_1.id,
            'server_type': 'dedicated',
        })

        self.assertEqual(server_1.owner_id.id, self.main_company_id)

    def test_compute_name(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test'
        })

        server_1 = self.server_env.create({
            'domain_id': domain_1.id,
            'server_type': 'dedicated',
        })

        server_2 = self.server_env.create({
            'friendly_name': 'server-1',
            'domain_id': domain_1.id,
            'server_type': 'dedicated',
        })

        self.assertEqual(server_1.name, 'domain-1.test')
        self.assertEqual(server_2.name, 'server-1 - domain-1.test')
