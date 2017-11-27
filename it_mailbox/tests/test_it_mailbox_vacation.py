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


class TestItMailboxVacation(TransactionCase):

    def setUp(self):
        super(TestItMailboxVacation, self).setUp()

        self.users_env = self.env['res.users']
        self.domain_env = self.env['it.domain']
        self.mailbox_env = self.env['it.mailbox']
        self.mailbox_vacation_env = self.env['it.mailbox.vacation']
        self.group_user_id = self.ref('base.group_user')
        self.group_it_admin_id = self.ref('it_base.it_admin')
        self.main_company_id = self.ref('base.main_company')

    def test_domain_changed(self):
        domain_1 = self.domain_env.create({
            'name': 'domain-1.test',
        })

        domain_2 = self.domain_env.create({
            'name': 'domain-2.test',
        })

        vacation_1 = self.mailbox_vacation_env.create({
            'name': 'user-1',
            'domain_id': domain_1.id,
        })

        vacation_1.write({
            'domain_id': domain_2.id,
        })

        result = vacation_1.domain_changed()

        self.assertEqual(result['domain_id']['mailbox_id'],
                         [('domain_id', '=', domain_2.id)])

        self.assertEqual(result['domain_id']['alias_id'],
                         [('domain_id', '=', domain_2.id)])
