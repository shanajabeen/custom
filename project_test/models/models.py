

from odoo import models, fields, api


class project_test(models.TransientModel):
    _name = 'project.test'
    
    product_id=fields.Many2one('product.product',string='product')
    customer_id=fields.Many2one('res.partner',string='customer name')
    qty=fields.Integer(string='quantity')

    def button1(self):
        record = self.env['sale.order'].browse(self._context.get('active_ids',[]))
        
        new_lines =[]
        new_lines.append((0, 0, {
            'product_id':self.product_id.id,
            'product_uom_qty':self.qty
        }))
        data= {
            'partner_id':self.customer_id.id,
            'order_line':new_lines,
          
        }
        sale = record.create(data)
        project_task_id = self.env['project.task'].browse(self.env.context['active_id'])
        project_task_id.sale_order_ids = [(4, sale.id)]
     
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id':sale.id ,
            # 'views': [(self.env.ref('sale.view_order_form').id, 'form')],
            'target': 'self',
           
            }


class project_button(models.Model):
    _inherit = 'project.task'

    vehicle_count  = fields.Char(compute='compute_display_name')
    sale_order_ids = fields.Many2many('sale.order', string='Sale IDs')
    
    def compute_display_name(self):
        self.sale_order_ids = self.mapped('sale_order_ids')
        for partner in self:
            partner.vehicle_count =len(partner.sale_order_ids)
             
    
    def get_vehicles(self):
        sale_order_ids = self.mapped('sale_order_ids')
         
        if len( sale_order_ids) > 1:
            return {
                'name': ('Attachments'),
                'type': 'ir.actions.act_window',
                'res_model':'sale.order',
                'view_mode':'tree,form',
                'domain': [('id', 'in', self.sale_order_ids.ids)],
                'target':'current',
            }
        elif len(sale_order_ids) == 1:
            return {
                'name': ('Attachments'),
                'type': 'ir.actions.act_window',
                'res_model':'sale.order',
                'view_mode':'form',
                'res_id': self.sale_order_ids.id,
                'target':'current',
         }

         