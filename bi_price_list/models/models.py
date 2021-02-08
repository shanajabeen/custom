# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_round
from odoo.exceptions import AccessError, UserError
from datetime import date
from datetime import datetime

class Bipricelist(models.Model):
    _inherit = 'purchase.order'    

    purchase_line_ids = fields.One2many('purchase.line','partner_line_id',string="Purchase Lines",required=False, store=True) 

    @api.depends('order_line.product_id')
    def compute_mybutton(self):
        val = []
        price_id=self.env['product.pricelist'].search([])
        partner = self.partner_id.id
        for i in self.order_line:
            qty=i.product_qty
            for j in price_id:
                price = j.get_product_price(i.product_id,qty, partner,date=False, uom_id=False)
                if not price:
                    price = i.product_id.list_price
                val.append((0, 0, {'product_id':i.product_id.id,'price_list_id':j.id,'amount':price}))           
        purchase_line_dic = {
            'purchase_line_ids': val,
            }  
        self.update(purchase_line_dic)
        return True

 

class BiResPartnerLine(models.Model):
    
    _name = 'purchase.line'
    
    product_id = fields.Many2one("product.product",string="Product")
    price_list_id = fields.Many2one('product.pricelist',string='Price_List')
    amount = fields.Float(string='Amount')
    partner_line_id = fields.Many2one('purchase.order', required=False)

    

    
         