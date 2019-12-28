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
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestOne(TransactionCase):

    def setUp(self):
        super(TestOne, self).setUp()

        self.user_env = self.env['res.users']
        self.link_env = self.env['it.link']
        self.ip_env = self.env['it.ip']
        self.estimate_cost_env = self.env['it.estimate.cost']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

        self.res_users_it_admin = self.user_env.create({
            'company_id': self.main_company_id,
            'name': 'IT Admin',
            'login': 'itadmin',
            'email': 'it_admin@example.com',
            'groups_id': [(6, 0, [self.group_it_admin_id])],
        })

        self.res_users_user = self.user_env.create({
            'company_id': self.main_company_id,
            'name': 'User',
            'login': 'user',
            'email': 'user@example.com',
            'groups_id': [(6, 0, [self.group_user_id])],
        })

    def test_it_link(self):
        """Test it.link model."""
        self.link_env.with_user(self.res_users_it_admin.id).create({
            'name': 'first link',
            'protocol': 'ftp',
            'url': 'ftp://test.com',
        })

        with self.assertRaises(AccessError):
            self.link_env.with_user(self.res_users_user.id).create({
                'name': 'second link',
                'protocol': 'ftp',
                'url': 'ftp://test.com',
            })

    def test_it_ip(self):
        """Test it.ip model."""
        all_ips = self.ip_env
        private_ip = self.ip_env.create({
            'function': 'Private Ip',
            'ip': '127.0.0.1',
        })
        all_ips += private_ip

        public_ip = self.ip_env.create({
            'function': 'Public Ip',
            'ip': '94.106.129.54',
        })

        bad_ip = self.ip_env.create({
            'function': 'Public Ip',
            'ip': 'not_an_ip',
        })
        all_ips += bad_ip

        all_ips._compute_is_private()

        self.assertTrue(private_ip.is_private)
        self.assertFalse(public_ip.is_private)
        self.assertFalse(bad_ip.is_private)

    def test_it_estimate_cost(self):
        """Test it.estimate.cost model."""
        currency = self.estimate_cost_env._default_currency()
        user_currency = self.env.user.company_id.currency_id

        self.assertEqual(currency.id, user_currency.id)
