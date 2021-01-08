# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class bi_point_of_sale(models.Model):
    _name = 'bi.pointsale'
    _description = 'bi_point_of_sale.bi_point_of_sale'
    
    _rec_name = 'sequence_no'
    sequence_no = fields.Char('sequence_no', readonly=True,default='New')

    cash_from_cash = fields.Float(string='Cash from Cash Box')
    cash_by_google_pay = fields.Float(string='Cash by Google Pay')
    cash_by_card = fields.Float(string='Cash by Card Swiping')
    cash_deposited= fields.Float(string='Cash deposited to Cash Box')
    total_a = fields.Float(string='Total A')
    
    sales_from_pos = fields.Float(string='Sales from POS')
    date = fields.Date(string='Date:',default=datetime.today())
    sales_from_invoice = fields.Float(string='Sales from Invoice')
    cash_from_snack= fields.Float(string='Collection from Snacks sales')
    cash_from_water = fields.Float(string='Cash from Water Sales')
    cash_for_purchase = fields.Float(string='Cash taken for Purchase')
    invoice_not_collected = fields.Float(string='Invoice not Collected')
    prev = fields.Float(string='Previously invoiced and collected today')
    total_b=fields.Float(string='Total B')
    total=fields.Float(string='Total A - Total B',)


    @api.onchange('date')
    def _onchange_date(self):
        for order in self:
            if self.date:
                pos_id=self.env['pos.order'].search([('date_order','>=',order.date),('date_order','<=',order.date)])
                sum =0
                for rec in pos_id:
                    sum+=rec.amount_total
                order.sales_from_pos=sum

    @api.onchange('date') 
    def _invoice_total(self):
        for order in self:
            if self.date:
                invoice_ids=self.env['account.move'].search([('invoice_date','=',order.date),('invoice_payment_state','=','paid')])
                sum_invoice =0
                for rec in invoice_ids:
                    sum_invoice+=rec.amount_total
                order.sales_from_invoice=sum_invoice          
            
    @api.onchange('cash_from_cash','cash_by_google_pay','cash_by_card','cash_deposited')
    def total_first(self):
        for rec in self:
            rec.total_a=(rec.cash_from_cash+rec.cash_by_google_pay+rec.cash_by_card)-rec.cash_deposited

    @api.onchange('sales_from_pos','sales_from_invoice','cash_from_snack','cash_from_water','cash_for_purchase','invoice_not_collected','prev')       
    def total_second(self):
        for rec in self:
            rec.total_b=((rec.sales_from_pos+rec.sales_from_invoice+rec.cash_from_snack+rec.cash_from_water)-(rec.cash_for_purchase+rec.invoice_not_collected))+rec.prev

    @api.onchange('total_a','total_b')
    def subtotal(self):
        for rec in self:
            rec.total=rec.total_a-rec.total_b

    @api.onchange('date')
    def prev_invoiced_pay(self):
        for rec in self:
            
            invoice_id=self.env['account.move'].search([('invoice_payment_state','=','paid'),('invoice_date','<',rec.date)])
            payment_ids=self.env['account.payment'].search([('payment_date','=',rec.date),('invoice_ids','in',invoice_id.ids)])     
            sum_prev_invoice =0
            for doc in payment_ids:
                sum_prev_invoice+=doc.amount
            rec.prev=sum_prev_invoice

    @api.onchange('date') 
    def _invoice_pending_today_total(self):
        for order in self:
            if self.date:
                invoice_ids=self.env['account.move'].search([('invoice_date','=',order.date),('invoice_payment_state','=','not_paid')])
                sum_invoice =0
                for rec in invoice_ids:
                    sum_invoice+=rec.amount_total
                order.invoice_not_collected=sum_invoice  
    @api.model
    def create(self, vals):
        if vals.get('sequence_no', 'New') == 'New':
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code('bi.pointsale') or '/'
        return super(bi_point_of_sale, self).create(vals)