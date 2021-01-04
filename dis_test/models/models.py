

from odoo import models, fields, api


class SALE_DISCOUNT(models.Model):
    _inherit='sale.order'
    

    discount = fields.Integer()
    value = fields.Integer()
    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
        amt=self.amount_total 
        deduct=(amt*self.discount)/100
        self.value=amt-deduct