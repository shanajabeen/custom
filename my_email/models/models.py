

from odoo import models, fields, api


class my_email(models.Model):
 _inherit='sale.order'
    

 def action_send_email(self):
   mail_template = self.env.ref('my_email.email_template')
   mail_template.send_mail(self.id, force_send=True)