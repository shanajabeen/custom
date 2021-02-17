# See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class classExamResult(models.TransientModel):
    '''designed for printing class report'''

    _name = "exam.classwise.result"
    _description = "class wise Exam Result"

    standard_id = fields.Many2one("school.standard",
                                  "Standard",
                                  help="select standard")
    year = fields.Many2one('academic.year', 'Academic Year',
                           help="Select Academic Year")
    exam_name = fields.Many2one('exam.exam', 'Exam Name')

    
    def print_class_report(self):
        data = {
            'ids'   : self.ids,
            'model' : self._name,
            'form'  : {
                    'stand': self.standard_id.id,
                    'year'  : self.year.id,
                    'exam' : self.exam_name.id
                },
            }
        return self.env.ref('bi_reports.class_result_qweb').report_action(self, data=data,config=False)
