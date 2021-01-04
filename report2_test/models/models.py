from odoo import models, fields, api

class SALEORDER(models.Model):
    _inherit='account.move'

class TestReport(models.TransientModel):
    _name = 'test.report'
    
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    def test_report(self):
        record = self.env['account.move'].search([('invoice_date', '>=', self.date_from),('invoice_date', '<=', self.date_to)])
        # for i in record:
       
        return self.env.ref('report2_test.print_report_pdf').report_action(record)