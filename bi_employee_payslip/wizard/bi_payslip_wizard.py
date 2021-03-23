from odoo import api, models,fields
from odoo.exceptions import UserError
from odoo import exceptions

class BiEmployeePayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip(self):
        datas = {'id': self.id}
        return self.env.ref('bi_employee_payslip.report_payslip_report').report_action(self, data=datas,config=False)
    