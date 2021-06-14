from odoo import _, api, fields, models
from datetime import date


class PurhaseOrderLine(models.Model):
    _inherit = 'bi.material.issue.diesel.line'
    
    product_budget_widget = fields.Boolean(default=True)

    @api.model
    def get_product_details(self, arg1):

        details = {}
        product_id=self.env['product.product'].browse(arg1['arg1'])
        location_ids = self.env['stock.location'].sudo().search([])
        for each in location_ids:
            qty = product_id.sudo().with_context({'location' : self.env['stock.location'].sudo().search([('id','=',each.id)]).id}).free_qty
            details[each.complete_name] = {
            'qty' : qty,
            }
        sum_qty=0    
        for each in details:
            sum_qty+=details[each]['qty']
        return sum_qty
