

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError, ValidationError
import logging
class sale1_test(models.Model):
    _inherit='sale.order'
    def action_cancel(self):
        # return self.write({'state': 'cancel'})
        return{

        'name': 'you cant cancel',

        'type': 'ir.actions.act_window',

        'res_model': 'hr.wizard',

        'view_mode': 'form',

        'view_type': 'form',

        'target': 'new'

        }
    
      
class hr_wizard(models.TransientModel):

    _name = 'hr.wizard'

    _description = 'HR employee wizard'

    message = fields.Text(string="welcome", readonly=True, store=True)
    reason = fields.Char()
    