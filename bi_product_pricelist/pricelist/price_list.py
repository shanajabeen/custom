# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError

class bi_product_pricelist(models.Model):
    _inherit = 'product.pricelist'
    def action_name(self):
        return {
            'name': 'Add Product', 
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bi.pricelist.wizard', 
            'context': {
                       'default_product_pricelist_id': self.id
                   },
            'target': 'new', }
        
  
class bi_product_pricelist_order(models.Model):
    _inherit = 'product.pricelist.item'

    tax = fields.Float("")
    percentage=fields.Float("")
   
    @api.onchange('tax','percentage')
    def _onchange_tax(self):
        for each in self:
            value=(each.tax*each.percentage)/100
            each.fixed_price = each.tax-value

    @api.constrains('percentage')
    def _check_something(self):
        for record in self:
            if record.percentage > 100:
                raise ValidationError("Your Enterd More Than 100 for Tax : %s" % record.percentage)
        

class PriceListWizard(models.TransientModel): 
    _name = 'bi.pricelist.wizard'

    product_tmpl_id = fields.Many2many('product.template')
    product_pricelist_id = fields.Many2one('product.pricelist', string='')

    def action_submit(self):
        
        product_list = []
        for each in self.product_tmpl_id:
            product_ids =(0,0,{
                'product_tmpl_id': each.id
              })
            product_list.append(product_ids)
        self.product_pricelist_id.write({'item_ids':product_list})
    