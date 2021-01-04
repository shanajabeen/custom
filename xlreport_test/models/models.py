

from odoo import models, fields, api

class TestReport(models.TransientModel):
    _name = 'test1.report'
    
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    customer_ids=fields.Many2many('res.partner',string='customer')

    def test_report1(self):
        # record = self.env['account.move'].search([('invoice_date', '>=', self.date_from),('invoice_date', '<=', self.date_to)])
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
       
        return self.env.ref('xlreport_test.report_id_xlx').report_action(self, data=datas,config=False)