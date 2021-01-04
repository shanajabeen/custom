# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class TestReport1(models.TransientModel):
    _name = 'test1.report'
    
    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')

    def test_report1(self): 
        data = {
            'ids':self.ids,
            'model':self._name,
            'form':{'start_date':self.date_from,
            'end_date':self.date_to } 
            }
        return self.env.ref('custom_sql.print_report_pdf').report_action(self,data=data)

    def test_report2(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('custom_sql.report_id_xlx1').report_action(self, data=datas,config=False)

class TestReport2 (models.AbstractModel):
    _name='report.custom_sql.my_template'
    def _get_report_values(self, docids, data):
        first=data['form']['start_date']
        last=data['form']['end_date']
        
        self.env.cr.execute('select am.name as id,pt.name as customer_name,am.invoice_date,am.invoice_date_due,am.amount_untaxed_signed,'\
        'am.amount_total_signed,am.amount_residual_signed,am.state,am.invoice_user_id,rp.name as name '\
        'from account_move am '\
        'join res_users ru on ru.id = am.invoice_user_id '\
        'join res_partner rp on ru.partner_id = rp.id '\
        'join res_partner pt on pt.id = am.partner_id '\
        'where invoice_date '\
        'between %s '\
        'and %s ORDER by am.partner_id ',                                   
        (str(first),str(last)))

        values=self.env.cr.dictfetchall()

        return {'values':values,
         }
        
 