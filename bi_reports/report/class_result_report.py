# See LICENSE file for full copyright and licensing details.

from odoo import models, api
from odoo.exceptions import ValidationError, UserError



class classExamReport(models.AbstractModel):
    _name = 'report.bi_reports.exam_result_class'
    _description = "class wise Exam Result"

    @api.model
    def _get_report_values(self, docids, data=None):
        class_result = self.env['ir.actions.report']._get_report_from_name(
            'bi_reports.exam_result_class')
        docs = self.env['exam.result'].search([('academic_year', '=',data['form']['year']),('s_exam_ids', '=',data['form']['exam']),
                                             ('standard_id', '=', data['form']['stand'])])
        
        return {'doc_ids': docids,
                'doc_model': class_result.model,
                # 'docs': class_model,
                'docs': docs,
                'data': data,
                'stand':data['form']['stand1'],
                'year':data['form']['year1'],
                'exam':data['form']['exam1'],
               
                }
