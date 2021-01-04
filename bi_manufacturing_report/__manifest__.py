# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 Bassam Infotech LLP(<https://www.bassaminfotech.com>).
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
{
    'name': "Manufacturing Report",
    'version': '13.0.1',
    'category': 'Manufacturing',
    'summary': 'Manufacturing Report XLS',
    'license':'AGPL-3',
    'description': """
        This module will create a excel report containing the important details of Manufacturing in a a specific time interval.
    """,
    'author': "Bassam Infotech LLP",
    'website': "http://www.bassaminfotech.com",
    'depends': ['base', 'mrp', 'report_xlsx'],
    # 'images': [ 'static/description/icon.png',],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_view.xml',
        'report/report_view.xml',
    ],
    'installable': True,
    'auto_install': False,

}