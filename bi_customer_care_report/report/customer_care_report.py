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
    _name = 'report.bi_customer_care_report.test_report_id_xlx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("INVOICE REPORT 1")
        format1 = workbook.add_format({'font_size': 12, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center'})
        format12 = workbook.add_format(
            {'font_size': 16, 'align': 'center', 'right': True, 'left': True, 'bottom': False,
             'top': True, 'bold': True,})
        format5 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center',})
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
        if data['form']['date_from']:
            date_from = datetime.strptime(data['form']['date_from'], '%Y-%m-%d').date()
            worksheet.write('A%s' % filter_row, 'Date From', boldc)
            worksheet.write('B%s' % filter_row, str(date_from.strftime("%d-%m-%Y")), boldc)
        if data['form']['date_to']:
            date_to = datetime.strptime(data['form']['date_to'], '%Y-%m-%d').date()
            worksheet.write('D%s' % filter_row, 'Date To', boldc)
            worksheet.write('E%s' % filter_row, str(date_to.strftime("%d-%m-%Y")), boldc)
            
        row = 6
        new_row = row + 1
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 20)

       
        domain=[]
        
        
        if data['form']['date_from']:
            domain.append(('service_date', '>=', data['form']['date_from']))
        if data['form']['date_to']:
            domain.append(('service_date', '<=', data['form']['date_to']))
        if data['form']['employee_id']:
            domain.append(('emp_id', '=', data['form']['employee_id']))
            
       
               
        sl_no = 1
        record = self.env['bi.complaint.registration'].search(domain)
        dic={}
        for each in record:
            if each.type:
                key=each.type
                if key in dic.keys():
                    dic[key] += 1
                else:
                    dic[key] = 1    
       
        worksheet.merge_range('A1:E1', 'CUSTOMER CARE STAFF', format5)
        worksheet.write('A%s' % row, 'SL NO', format1)
        worksheet.write('B%s' % row, 'REGISTERED COUNTS', format1)
        worksheet.write('C%s' % row, 'INQUIRY', format1)
        worksheet.write('D%s' % row, 'INSTALLATION', format1)
        worksheet.write('E%s' % row, 'WARRANTY REGISTRATION', format1)
        worksheet.write('F%s' % row, 'FEEDBACK CALLS', format1)
        worksheet.write('G%s' % row, 'TOTAL', format1)
    

        val = []
        val=len(record)
        count=0
        for each in record:
            if each.type:
                count=count+1

        for each in record:  
            worksheet.write('A%s' % new_row, sl_no, center)
            worksheet.write('B%s' % new_row, val) 
            worksheet.write('C%s' % new_row, count) 
            if 'installation' in dic.keys(): 
                worksheet.write('D%s' % new_row, dic['installation']) 
            if  'warranty' in dic.keys():    
                worksheet.write('E%s' % new_row, dic['warranty'])      
            # new_row+=1
            # sl_no+=1