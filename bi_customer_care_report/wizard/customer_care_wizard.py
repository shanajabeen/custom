
from odoo import models, fields, api

class TestReport(models.TransientModel):
    _name = 'customer.care_report'
    
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    employee_id=fields.Many2one('res.users', string='Customer Care')

    def customer_care_report(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
       
        return self.env.ref('bi_customer_care_report.customer_care_report_id_xlx').report_action(self, data=datas,config=False)

class CustomerService(models.Model):
    _inherit = 'bi.complaint.registration'


    emp_id=fields.Many2one('res.users', string='Employee', index=True, tracking=2, default=lambda self: self.env.user)

    