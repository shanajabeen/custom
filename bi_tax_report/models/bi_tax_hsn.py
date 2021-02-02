
from odoo import models, fields, api
import logging
from num2words import num2words 

class bi_tax_report(models.Model):
    _name = 'report.bi_tax_report.my_template'

    # value = fields.Float(string="tax",compute="sales")
    def _get_report_values(self, docids, data):
        docs = self.env['account.move'].browse(docids).sudo()
        
        dict =	{}
        igst_val=0
        igst_val_1=0
        kfc = 0
        tax_tot=0
        for val in docs.invoice_line_ids:

            toal_price = val.quantity*val.price_unit
            scheme=(toal_price*val.scheme_discount)/100
            cash=(toal_price*val.cash_discount)/100
            tax_value = round(toal_price-(val.scheme_discount_amount+val.cash_discount_amount),2)    
            key=val.product_id.l10n_in_hsn_code
            key2=val.product_id.taxes_id.ids[0]
            final_key = str(key)+str(key2)
            if final_key in dict.keys(): 
               dict[final_key][1] += tax_value 
            else:
                dict[final_key]= [key, tax_value]

            igst_val = val.price_total - val.price_subtotal-val.kfc_tax
            igst_val_1 +=igst_val
            kfc += val.kfc_tax
            total_price=val.quantity*val.price_unit
            scheme=val.scheme_discount_amount
            cash=val.cash_discount_amount
            tax=total_price-(scheme+cash)
            tax_tot= tax_tot+tax
        igst_val_2 = {'amt':igst_val_1}      
        kf_val_tot = {'amt':kfc}
        
       
        y=round(igst_val_1+(igst_val_1/2)+(igst_val_1/2)+kfc+tax_tot,2)
        x= num2words(y).title()
        words = {'amt':x}
        return {
                'docs' : docs,
                'timesheet' : dict,
                'igst' : igst_val_2,
                'kfc' : kf_val_tot,
                'words' : words
                }


                
       

      

  