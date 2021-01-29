
from odoo import models, fields, api
import logging

class bi_tax_report(models.Model):
    _name = 'report.bi_tax_report.my_template'

    # value = fields.Float(string="tax",compute="sales")
    def _get_report_values(self, docids, data):
        docs = self.env['account.move'].browse(docids).sudo()
        
        dict =	{}
        tax=docs.invoice_line_ids.mapped('product_id')

        for val in docs.invoice_line_ids:

            toal_price = val.quantity*val.price_unit
            scheme=(toal_price*val.scheme_discount)/100
            cash=(toal_price*val.cash_discount)/100
            tax_value=toal_price-(val.scheme_discount_amount+val.cash_discount_amount)    
            key=val.product_id.l10n_in_hsn_code
            key2=val.product_id.taxes_id.ids[0]
            final_key = str(key)+str(key2)
            if final_key in dict.keys(): 
               dict[final_key][1] += tax_value 
            else:
                dict[final_key]= [key, tax_value]
                            
        return {
                'docs' : docs,
                'timesheet' : dict,
                }


                
       

      

  