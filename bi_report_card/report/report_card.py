# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from datetime import datetime
_logger = logging.getLogger(__name__)
import datetime

class ReportReportCard(models.AbstractModel):
    _name = 'report.bi_report_card.report_card_report'

   
    def _get_report_values(self, docids, data):
        
        docs = self.env['student.student'].browse(data['context']['active_id']).sudo()
        date_today = fields.Date.today()
        attandance_id = self.env['daily.attendance.line'].search([('standard_id.date','<=',date_today),('stud_id.id','=',docs.id),('standard_id.standard_id','=',docs.standard_id.id),('standard_id.academic_year','=',data['form']['s_academic_year_id']),('standard_id.term','=',data['form']['s_term']),])
        attandance_id_term = self.env['daily.attendance'].search([('date','<=',date_today),('standard_id','=',docs.standard_id.id),('academic_year','=',data['form']['s_academic_year_id']),('term','=',data['form']['s_term']),])
       
        term1=0
        term2=0
        nterm1=0
        nterm2=0
        count = 0
        count2 = 0
        late=0
        termcount=0
        ccount=0
        ccount2=0
        dict2={}
        dict3=[]
        for each in attandance_id_term:
            termcount+=1
        for each in attandance_id:
            if each.is_present==True:
                count+=1 
            if each.is_absent==True:
                count2+=1
            if each.is_late==True:
                late+= each.late_time   
              
        year= self.env['academic.year'].search([('id','=',docs.year.id)])
        grade= self.env['grade.master'].search([('medium_id','=',docs.medium_id.id)])
        sco= self.env['bi.student.coscholastic'].search([('bi_coscholastic_id.medium_id','=',docs.medium_id.id),('bi_coscholastic_id.academic_year','=',docs.year.id),('bi_coscholastic_id.class_id','=',docs.standard_id.id),('bi_coscholastic_id.subject_type','=','coscholastic'),('student_id','=',docs.id)])
        nonsco= self.env['bi.student.coscholastic'].search([('bi_coscholastic_id.medium_id','=',docs.medium_id.id),('bi_coscholastic_id.academic_year','=',docs.year.id),('bi_coscholastic_id.class_id','=',docs.standard_id.id),('bi_coscholastic_id.subject_type','=','nonscholastic'),('student_id','=',docs.id)])
        id3=self.env['scholastic.report'].search([('bi_scholastic_id.student_id','=',docs.id),('bi_scholastic_id.academic_year','=',docs.year.id),('bi_scholastic_id.class_id','=',docs.standard_id.id)])
          
        for c in id3:
            if c.bi_scholastic_id.term=='term1':
                ccount+=1 
            if c.bi_scholastic_id.term=='term2':
                ccount2+=1     
        for g in grade.grade_ids:
            x=g.from_mark
            y=g.to_mark
            z=g.grade
            dict2[x]=y
            dict3.append(z)
        for sc in sco.bi_coscholastic_id:
            if sc.term=='term1':
                term1+=1
            if sc.term=='term2':
                term2+=1
        for sc1 in nonsco.bi_coscholastic_id:
            if sc1.term=='term1':
                nterm1+=1
            if sc1.term=='term2':
                nterm2+=1
        return {
                'docs' : docs,
                'present':count,
                'absent' : count2,
                'late':late,
                'dict2':dict2,
                'dict3':dict3,
                'term1':term1,
                'term2':term2,
                'nterm1':nterm1,
                'nterm2':nterm2,
                'sc':sco,
                'nsc':nonsco,
                'id3':id3,
                'ccount':ccount,
                'ccount2':ccount2,
                'termcount':termcount,
             
                }

    