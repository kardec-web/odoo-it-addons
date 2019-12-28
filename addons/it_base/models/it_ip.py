
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
import ipaddress

from odoo import api, fields, models


class ServerIp(models.Model):

    _name = "it.ip"
    _rec_name = "ip"
    _description = "Infrastructure IP"

    ip = fields.Char('IP', required=True, index=True)
    active = fields.Boolean(default=True, index=True)
    function = fields.Char(
        help="Described how the IP is used")
    is_private = fields.Boolean(compute="_compute_is_private", store=True)

    @api.depends('ip')
    def _compute_is_private(self):
        # No coverage because the field is required but when we
        # create an new ip by the web interface Odoo throw an error.
        for record in self:  # pragma: no cover
            if not record.ip:
                record.is_private = False
                continue

            try:
                record.is_private = ipaddress.ip_address(
                    record.ip.split("/")[0]).is_private
            except ValueError:
                record.is_private = False
