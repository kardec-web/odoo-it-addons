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
from openerp.exceptions import ValidationError


class TestItMailbox(TransactionCase):

    def setUp(self):
        super(TestItMailbox, self).setUp()

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

        mailbox_1 = self.mailbox_env.create({
            'name': 'user-1',
            'domain_id': domain_1.id,
        })

        self.assertEqual(mailbox_1.email, 'user-1@domain-1.test')

    def test_check_max_mailboxes_limit(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test',
            'max_mailbox': 1,
        })

        self.mailbox_env.create({
            'name': 'user-1',
            'domain_id': domain_1.id,
        })
        with self.assertRaises(ValidationError):
            self.mailbox_env.create({
                'name': 'user-1',
                'domain_id': domain_1.id,
            })
