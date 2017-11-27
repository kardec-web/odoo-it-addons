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
from odoo.exceptions import AccessError


class TestOne(TransactionCase):

    def setUp(self):
        super(TestOne, self).setUp()

        self.usersEnv = self.env['res.users']
        self.linkEnv = self.env['it.link']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

        self.res_users_it_admin = self.usersEnv.create({
            'company_id': self.main_company_id,
            'name': 'IT Admin',
            'login': 'itadmin',
            'email': 'it_admin@example.com',
            'groups_id': [(6, 0, [self.group_it_admin_id])],
            'notify_email': False,
        })

        self.res_users_user = self.usersEnv.create({
            'company_id': self.main_company_id,
            'name': 'User',
            'login': 'user',
            'email': 'user@example.com',
            'groups_id': [(6, 0, [self.group_user_id])],
            'notify_email': False,
        })

    def test_it_link(self):
        '''Test it.link model'''

        self.linkEnv.sudo(user=self.res_users_it_admin.id).create({
            'name': 'first link',
            'protocol': 'ftp',
            'url': 'ftp://test.com',
        })

        with self.assertRaises(AccessError):
            self.linkEnv.sudo(user=self.res_users_user.id).create({
                'name': 'second link',
                'protocol': 'ftp',
                'url': 'ftp://test.com',
            })
