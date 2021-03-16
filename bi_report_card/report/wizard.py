from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError

class ReportCard1(models.TransientModel):
    _name = 'report.card1'

    def check_current_year(self):
        res = self.env['academic.year'].search([('current', '=',True)])
        if not res:
            raise ValidationError(_('''There is no current Academic Year defined!Please contact to Administator!'''))
        return res.id

    s_term = fields.Selection([
        ('term1', 'TERM 1'),
        ('term2', 'TERM 2')
    ], string='Term')
    s_academic_year_id = fields.Many2one('academic.year', string='Academic Year', default=check_current_year)


    def print_report(self):

        data = {
            'ids'   : self.ids,
            'model' : self._name,
            'form'  : {
                    's_term'            : self.s_term,
                    's_academic_year_id'    : self.s_academic_year_id.id,
                },
            }
            
        
        return self.env.ref('bi_report_card.report_card_pdf').report_action(self, data=data, config=False)

