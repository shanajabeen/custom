# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import AccessError, UserError
from datetime import date
from datetime import datetime

class secondary(models.Model):
    _inherit = 'stock.move'    

   
    sec = fields.Float("Secondary")
   
    
class BiStockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def button_validate(self):
        if self.product_id:
            date_ids = self.product_id.product_tmpl_id.mapped(
                'multi_uom_ids.date')
            date_today = date.today()
            if date_ids:
                nearest_date = min(date_ids,key=lambda x: abs(x-date_today))
                uom_id = self.product_id.product_tmpl_id.mapped(
                    'multi_uom_ids').filtered(lambda x: x.date == nearest_date)
                self.move_lines.sec = self.move_lines.product_uom_qty * uom_id.secondary_uom_ratio
            else:
                self.move_lines.sec = 0
        else:
            self.move_lines.sec = 0
        return super(BiStockPicking, self).button_validate() 