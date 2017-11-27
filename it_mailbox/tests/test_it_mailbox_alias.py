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


class TestItMailboxAlias(TransactionCase):

    def setUp(self):
        super(TestItMailboxAlias, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.mailbox_env = self.env['it.mailbox']
        self.mailbox_alias_env = self.env['it.mailbox.alias']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

    def test_compute_display_name(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test',
        })

        alias_1 = self.mailbox_alias_env.create({
            'name': 'user-1',
            'goto': 'user-1@exemple.com',
            'domain_id': domain_1.id,
        })

        self.assertEqual(alias_1.email, 'user-1@domain-1.test')
