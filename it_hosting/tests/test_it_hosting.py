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


class TestItHosting(TransactionCase):

    def setUp(self):
        super(TestItHosting, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.hosting_env = self.env['it.hosting']
        self.server_ip_env = self.env['it.server.ip']
        self.link_env = self.env['it.link']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

    def test_write(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test',
        })
        hosting_1 = self.hosting_env.create({
            'name': 'Hosting 2',
            'domain_id': domain_1.id,
        })
        server_ip_1 = self.server_ip_env.create({
            'name': 'Hosting 1',
            'hosting_id': hosting_1.id,
        })
        link_1 = self.server_ip_env.create({
            'name': 'Link 1',
            'url': 'http://test.be',
            'hosting_id': hosting_1.id,
        })
        domain_2 = self.domain_env.create({
            'name': 'domain-2.test',
            'hosting_id': hosting_1.id,
        })

        hosting_1.write({
            'active': False,
        })

        self.assertFalse(server_ip_1.active)
        self.assertFalse(link_1.active)
        self.assertFalse(domain_2.active)

        hosting_1.write({
            'active': True,
        })

        self.assertTrue(server_ip_1.active)
        self.assertTrue(link_1.active)
        self.assertTrue(domain_2.active)
