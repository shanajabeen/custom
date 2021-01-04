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


class REPORT5Xlsx1(models.AbstractModel):
    _name = 'report.project_test.test_report_id_xlx1'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("PROJECT REPORT 1")
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center', 'bold': True})
        format12 = workbook.add_format(
            {'font_size': 16, 'align': 'center', 'right': True, 'left': True, 'bottom': False,
             'top': True, 'bold': True,})
        format3 = workbook.add_format({'bold':True,'bottom': True, 'top': True, 'font_size': 12,'align': 'center'})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12,'bold':True,'align':'center'})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        boldc = workbook.add_format({'bold':True,'align':'center'})
        center = workbook.add_format({'align':'center'})

        filter_row = 3
        filter_row1 = 5
       
        row = 6
        new_row = row + 1
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 20)

       

        worksheet.merge_range('A1:E1', 'PROJECT REPORT', format3)
        worksheet.write('A%s' % row, 'SL NO', format3)
        worksheet.write('B%s' % row, 'CUSTOMER', format3)
        worksheet.write('C%s' % row, 'PRODUCT', format3)
        worksheet.write('D%s' % row, 'PRICE', format3)
    
      
        domain =[]
       
        if data['form']['customer_id1']:
            domain.append(('partner_id', '=', data['form']['customer_id1'])) 
               
        sl_no = 1
        record = self.env['sale.order'].search(domain)
    
        for each in record:
            for line in each.order_line:
                worksheet.write('A%s' % new_row, sl_no, center)
                worksheet.write('B%s' % new_row, each.partner_id.name,center)
                worksheet.write('C%s' % new_row, line.product_id.name,center) 
                worksheet.write('D%s' % new_row, line.price_unit,center)     
                new_row+=1
                sl_no+=1