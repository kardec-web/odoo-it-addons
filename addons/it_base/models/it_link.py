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
from odoo import fields, models


class Link(models.Model):
    _name = "it.link"
    _description = "Infrastructure Link"

    name = fields.Char(required=True, index=True)
    url = fields.Char(required=True, index=True)
    active = fields.Boolean(default=True, index=True)

    protocol = fields.Selection([
        ('ftp', 'FTP'),
        ('http', 'HTTP'),
        ('ssh', 'SSH'),
    ], default='http', index=True)

    hostname = fields.Char()
    port = fields.Integer()
    user = fields.Char()
