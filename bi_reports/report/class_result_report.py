# See LICENSE file for full copyright and licensing details.

from odoo import models, api
from odoo.exceptions import ValidationError, UserError



class classExamReport(models.AbstractModel):
    _name = 'report.bi_reports.exam_result_class'
    _description = "class wise Exam Result"

                    
    # def get_header_data(self, exam_name, standard_id, year):
    #     exam = self.env['exam.result'].search([('s_exam_ids', '=',
    #                                           exam_name.id),('academic_year', '=',year.id),
    #                                          ('standard_id', '=', standard_id.id)], limit=1)
       
    #     data_dict = {}
    #     sub_list = []
      
    #     for line in exam.result_ids:
    #         sub = line.subject_id.name
    #         sub_list.append(sub)

        
    #     data_dict.update({
    #                       'sub_list': sub_list,
                          
    #                       })
    #     return [data_dict]

    

    @api.model
    def _get_report_values(self, docids, data):
        class_result = self.env['ir.actions.report']._get_report_from_name(
            'bi_reports.exam_result_class')
        
        docs = self.env['exam.result'].search([('academic_year', '=',data['form']['year']),
                                             ('standard_id', '=', data['form']['stand'])])
                                                      
        return {'doc_ids': docids,
                'doc_model': class_result.model,
                'docs': docs,
                'data': data,
                # 'get_header_data': self.get_header_data,
                
                }
