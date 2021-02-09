

from odoo import models, fields, api


class bi_overhead(models.Model):
    _inherit = 'mrp.production'

    def action_add(self):
        return {
            'name': 'Add Product', 
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bi.overhead.wizard', 
            'context': {
                       'default_self_id': self.id
                   },
            'target': 'new', }
        
class OverheadWizard(models.TransientModel): 
    _name = 'bi.overhead.wizard'

    self_id = fields.Many2one('mrp.production', string='')
    workcenter_id = fields.Many2one('mrp.workcenter', string='Work Center')
    employee_ids = fields.Many2many('hr.employee')
   

    def action_submit(self):

        overhead_list = []
        employee_list = []
        for rec in self.employee_ids:
            employee_list.append(rec.id)
        for each in self.workcenter_id:
            product_ids =(0,0,{
                'workcenter_id':each.id ,
                'employee_ids' : [(6,0,employee_list)]
              })
            overhead_list.append(product_ids)
        self.self_id.write({'overhead_ids':overhead_list})
        

