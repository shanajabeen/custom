from odoo import fields, models, api, _
from odoo.exceptions import Warning

class wizard_pos_sale_report(models.TransientModel):
    _name = 'wizard.pos.sale.report'

    @api.model
    def get_ip(self):
        proxy_ip = self.env['res.users'].browse([self._uid]).company_id.report_ip_address or''
        return proxy_ip
  
    session_ids = fields.Many2many('pos.session', 'pos_session_list', 'wizard_id', 'session_id', string="Closed Session(s)")
    report_type = fields.Selection([('thermal', 'Thermal'),
                                        ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")
    proxy_ip = fields.Char(string="Proxy IP", default=get_ip)
    
    def print_receipt(self):
        # session_ids = fields.Many2many('pos.session', 'pos_session_list', 'wizard_id', 'session_id', string="Closed Session(s)")
        # report_type = fields.Selection([('thermal', 'Thermal'),
        #                                 ('pdf', 'PDF')], default='pdf', readonly=True, string="Report Type")
        # proxy_ip = fields.Char(string="Proxy IP", default=get_ip)




        orders = self.env['pos.order'].search([
            ('session_id.id', '=',self.session_ids.ids )
        ])
        order_line_ids = self.env['pos.order.line'].search([
            ('order_id', 'in', orders.ids)
        ])
        categ_sum = {}
        total_sales = 0
        for each_line in order_line_ids:
            if each_line.product_id.categ_id.name in categ_sum:
                categ_sum[each_line.product_id.categ_id.name] += each_line.price_subtotal_incl
            else:
                categ_sum[each_line.product_id.categ_id.name] = each_line.price_subtotal_incl
            total_sales += each_line.price_subtotal_incl
        vat_list = orders.mapped('amount_tax')
        vat_amount = sum(vat_list)
        paid_list = orders.mapped('amount_paid')
        paid_amount = sum(paid_list)
        round_amount = paid_amount - total_sales
        payment_ids = self.env['pos.payment'].search([
            ('session_id', '=',self.session_ids.ids )
        ])
        cash={}
        cash=0
        credit_card={}
        credit_card=0
        payment_sum = {}
        invoice_no = len(orders)
        for each_payment in payment_ids:
            if each_payment.payment_method_id.name in payment_sum:
                payment_sum[each_payment.payment_method_id.name] += each_payment.amount
            else:
                payment_sum[each_payment.payment_method_id.name] = each_payment.amount
        open_id=self.env['pos.session'].search([('id','=',self.session_ids.ids)])
        opening=open_id.cash_register_balance_start
        closing=open_id.cash_register_balance_end_real
        diff=closing-opening
        var=categ_sum.keys()
        list = [] 
        for key in categ_sum.keys(): 
            list.append(key) 

        
        datas = {'ids': self._ids,
                 'form': self.read()[0],
                 'model': 'wizard.pos.sale.report',
                 'payment':payment_sum,
                 'cash_sale':cash,
                 'credit_card':credit_card,
                 'M':categ_sum,
                 'var':list,
                 'vat': vat_amount,
                 'round':round_amount,
                 'invoice':invoice_no,
                 'total_sale':total_sales,
                 'net_total':paid_amount,
                 'open1':opening,
                 'close1':closing,
                 'diff':diff 
                }

        return self.env.ref('bi_pos_stock_report.report_pos_sales_pdf').report_action(self, data=datas)

  

