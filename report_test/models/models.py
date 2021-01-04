

from odoo import models, fields, api
from datetime import date

class report_test(models.Model):
    _name = 'report.test'
    _description = 'report_test.report_test'

    address = fields.Char()
    age = fields.Integer()
    
    date=fields.Date('Created Date', required=True, default=fields.Date.today())

