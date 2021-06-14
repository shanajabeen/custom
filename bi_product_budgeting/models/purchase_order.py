from odoo import _, api, fields, models
from datetime import date


class PurhaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    product_budget_widget = fields.Boolean(default=True)

    @api.model
    def get_product_details(self, arg1):
        location_ids = self.env['stock.location'].sudo().search([('usage', '=', 'internal'),('branch_id','=',self.order_id.branch_id.id)])
        product = self.env['product.product'].browse(arg1['arg1'])
        today = date.today()
        details = {}
        purchase_order_line_ids = self.env['purchase.order.line'].search([('product_id','=',product.id),('state','=','purchase')])
        for each in location_ids:
            qty = product.sudo().with_context({'location' : self.env['stock.location'].sudo().search([('id','=',each.id)]).id}).free_qty
            avail_qty = product.sudo().with_context({'location' : self.env['stock.location'].sudo().search([('id','=',each.id)]).id}).qty_available
            ordered_qty = sum(purchase_order_line_ids.mapped('product_uom_qty'))
            ptg_calender_line_id = self.env['ptg.calendar.line'].search([('date_from','<=',today),('date_to','>=',today)])
            if ptg_calender_line_id:
                year = ptg_calender_line_id.ptg_calendar_id.year
                semester = ptg_calender_line_id.semester
                budget_id = self.env['bi.product.budgeting'].search([('year','=',year),('semester','=', semester),('branch_id','=',self.order_id.branch_id.id)])
                for val in budget_id:
                    budget_line_id = self.env['bi.product.budgeting.line'].search([('budgeted_id','=',val.id),('product_id','=',product.id)])
                    if budget_line_id:
                        details[each.complete_name] = {
                        'branch': each.complete_name,
                        'budgeted_qty' : budget_line_id.budgeted_qty,
                        'qty' : qty,
                        'uom' : product.uom_id.name,
                        'virtual_qty': avail_qty,
                        'ordered_qty':ordered_qty,
                        'pending_qty':budget_line_id.budgeted_qty - ordered_qty,
                        }
        return list(details.values())