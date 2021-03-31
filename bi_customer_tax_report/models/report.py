from odoo import models, fields, api
from odoo.tools.misc import xlwt
from odoo.exceptions import UserError, AccessError
import io
import base64
import operator
from PIL import Image
import itertools
import time
from datetime import datetime,timedelta,date
import xlsxwriter


class REPORT5Xlsx(models.AbstractModel):
    _name = 'report.bi_customer_tax_report.tax_report_id_xlx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("PRODUCT_TAX")
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center', 'bold': True})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12,'align': 'center'})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12,'bold':True,'align':'center'})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        center = workbook.add_format({'align':'center'}) 
            
        row = 4
        new_row = row 
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
      
       
        worksheet.merge_range('A1:D1', 'TAX REPORT',format3)
        worksheet.write('A%s' % row, 'SALE', format3)
        worksheet.write('B%s' % row, '', format3)
        worksheet.write('C%s' % row, '', format3)
        worksheet.write('D%s' % row, '', format3)
        
        query_one = """ select fp.name as fp_name,sl.price_total as price,
                        ac.name as t_name from sale_order_line sl 
                        join sale_order so on so.id=sl.order_id 
                        join account_tax_sale_order_line_rel asr on sl.id=asr.sale_order_line_id 
                        join account_tax ac on ac.id=asr.account_tax_id 
                        join product_template po on po.id =sl.product_id 
                        join account_fiscal_position fp on fp.id=so.fiscal_position_id
                        where so.date_order >='"""+str(data['form']['date_from'])+"""' 
                        and so.date_order <= '"""+str(data['form']['date_to'])+"""' 
                        and so.state='done'
                        ORDER BY fp_name
                    """

        self.env.cr.execute(query_one)
        docs_two = self.env.cr.dictfetchall()
        dict1={'0':0}
        for each in docs_two:
            if each['fp_name'] not in dict1:
                dict1[each['fp_name']]={each['t_name']:each['price']}
            else:
                if each['t_name'] not in dict1[each['fp_name']]: 
                    dict1[each['fp_name']][each['t_name']]=each['price']
                else:
                    dict1[each['fp_name']][each['t_name']]+=each['price']        
        if '0' in dict1:
            del dict1['0']
        new_row+=1
        for each in dict1:
            worksheet.write('A%s' % new_row, '', center)
            worksheet.write('B%s' % new_row, each, center)
            for k in dict1[each]:
                tax_value = k.split(' ')
                tax_column = tax_value[-1] + " TAXABLE"
                worksheet.write('C%s' % new_row,tax_column, center)
                worksheet.write('D%s' % new_row, dict1[each][k], center)
                new_row+=1
       

        query_s = """ select pl.price_total as price,fp.name as fp_name,
                        ac.name as t_name from purchase_order_line pl 
                        join purchase_order pa on pa.id=pl.order_id 
                        join account_tax_purchase_order_line_rel apr on pl.id=apr.purchase_order_line_id 
                        join account_tax ac on ac.id=apr.account_tax_id
                        join product_template po on po.id =pl.product_id
                        join account_fiscal_position fp on fp.id=pa.fiscal_position_id 
                        where pa.date_order >='"""+str(data['form']['date_from'])+"""' 
                        and pa.date_order <= '"""+str(data['form']['date_to'])+"""' 
                        and pa.state='done'
                        ORDER BY fp_name  
                    """
        self.env.cr.execute(query_s)
        docs_s = self.env.cr.dictfetchall()

        dict2={'0':0}
        for each in docs_s:
            if each['fp_name'] not in dict2:
                dict2[each['fp_name']]={each['t_name']:each['price']}
            else:
                if each['t_name'] not in dict2[each['fp_name']]: 
                    dict2[each['fp_name']][each['t_name']]=each['price']
                else:
                    dict2[each['fp_name']][each['t_name']]+=each['price']        
        if '0' in dict2:
            del dict2['0']

        new_row+=1
        worksheet.write('A%s' % new_row, 'PURCHASE', format3)
        worksheet.write('B%s' % new_row, '', format3)
        worksheet.write('C%s' % new_row, '', format3)
        worksheet.write('D%s' % new_row, '', format3)
        new_row+=1
        for each in dict2:
            worksheet.write('A%s' % new_row, '', center)
            worksheet.write('B%s' % new_row, each, center)
            for k in dict2[each]:
                tax_value = k.split(' ')
                tax_column = tax_value[-1] + " TAXABLE"
                worksheet.write('C%s' % new_row,tax_column, center)
                worksheet.write('D%s' % new_row, dict2[each][k], center)
                new_row+=1

        query_h = """ select fp.name as fp_name,bsl.price_total as price,
                        ac.name as t_name from bi_sale_return_line bsl 
                        join bi_sale_return bs on bs.id=bsl.return_id 
                        join account_tax_bi_sale_return_line_rel assr on bsl.id=assr.bi_sale_return_line_id 
                        join account_tax ac on ac.id=assr.account_tax_id
                        join product_template po on po.id =bsl.product_id
                        join account_fiscal_position fp on fp.id=bs.fiscal_position_id 
                        where  bs.date_order >='"""+str(data['form']['date_from'])+"""' 
                        and bs.date_order <= '"""+str(data['form']['date_to'])+"""' 
                        and bs.state='done'
                        ORDER BY fp_name  
                    """
        self.env.cr.execute(query_h)
        docs_h = self.env.cr.dictfetchall()

        dict3={'0':0}
        for each in docs_h:
            if each['fp_name'] not in dict3:
                dict3[each['fp_name']]={each['t_name']:each['price']}
            else:
                if each['t_name'] not in dict3[each['fp_name']]: 
                    dict3[each['fp_name']][each['t_name']]=each['price']
                else:
                    dict3[each['fp_name']][each['t_name']]+=each['price']        
        if '0' in dict3:
            del dict3['0']

        new_row+=1
        worksheet.write('A%s' % new_row, 'SALES RETURN', format3)
        worksheet.write('B%s' % new_row, '', format3)
        worksheet.write('C%s' % new_row, '', format3)
        worksheet.write('D%s' % new_row, '', format3)
        new_row+=1
        for each in dict3:
            worksheet.write('A%s' % new_row, '', center)
            worksheet.write('B%s' % new_row, each, center)
            for k in dict3[each]:
                tax_value = k.split(' ')
                tax_column = tax_value[-1] + " TAXABLE"
                worksheet.write('C%s' % new_row,tax_column, center)
                worksheet.write('D%s' % new_row, dict3[each][k], center)
                new_row+=1