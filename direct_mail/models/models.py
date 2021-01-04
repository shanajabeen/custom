# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64

from datetime import date,timedelta
class direct_mail(models.Model):
    _inherit='report.xlreport_test.test_report_id_xlx'
    _name = 'direct.mail'
    _description = 'direct_mail.direct_mail'
    sender = fields.Char(string='')
    recipients_id = fields.Char()
    message_body = fields.Text(string='')
    current_date = fields.Date(string='', default=fields.Date.today)
    date_to=date.today()
    date_from =date_to-timedelta(60)
    attach=fields.Binary()
    # def action_send_email(self):
    # this function will send email without template 
    #     template_obj = self.env['mail.mail']
   
    #     template_data = {
    #                 'subject': 'Due Invoice Notification : ' + str(self.current_date),
    #                 'body_html': self.message_body,
    #                 'email_from': self.sender,
    #                 'email_to':self.recipients_id,
    #                 # 'attachment_ids': [(4, 0,attachment_id)]
    #                 }
    #     template_id = template_obj.sudo().create(template_data)
    #     template_id.sudo().send()
   

    def action_send_email(self):
        data={
            
            'form'  : {
                    'start_date': self.date_from,
                    'end_date'  : self.date_to,
                },
            }

        # below function will be the calling fuction in custom sql used to call date filter report
        #  .render_xlsx(self.data) if it is a xl report
        pdf= self.env.ref('custom_sql.print_report_pdf').render_qweb_pdf(self, data=data)
        pdfa=base64.b64encode(pdf[0])
        email_template = self.env.ref('direct_mail.email_template')
        attachment = {

               'name': "my attachements",
            #    'datas': self.attach,
                'datas': pdfa,
               'res_model': 'direct.mail',
               'type': 'binary'}
        id = self.env['ir.attachment'].create(attachment)
        email_template.attachment_ids = [(6,0,[id.id])]
        # mail_template = self.env.ref('direct_mail.email_template')
        email_template.send_mail(self.id, force_send=True)


