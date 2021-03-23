import time
from odoo import api, models
from odoo.exceptions import UserError
import datetime
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from itertools import groupby
from operator import itemgetter
from dateutil import parser
import itertools
import base64
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from xlwt import Workbook
import xlwt
from PIL import Image
import io
import os
from num2words import num2words 


class BiPayrollOrder(models.AbstractModel):
    _name = 'report.bi_employee_payslip.report_payslip_report_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_resized_image_data(self, byte_stream, bound_width_height):
        # get the byte stream of image and resize it
        im = Image.open(byte_stream)
        im.thumbnail(bound_width_height, Image.ANTIALIAS)  # ANTIALIAS is important if shrinking

        # stuff the image data into a bytestream that excel can read
        im_bytes = io.BytesIO()
        im.save(im_bytes, format='PNG')
        return im_bytes

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("Employee Payslip")
        # obj = self.env['bi.payslip.report'].search([])[-1]
        format1 = workbook.add_format({'font_size': 14, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'center'})
        format4 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True,
                                       'top': True, 'bottom': True, 'right': True, 'left': True,
                                       'border_color': '000000', 'border': 2})
        format5 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})
        format6 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True, 'bg_color': '#cccccc',
                                       'top': True, 'bottom': True, 'right': True, 'left': True,
                                       'border_color': '#000000'})
        format8 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True,
                                       'top': True, 'bottom': True, 'right': True, 'left': True,
                                       'border_color': '000000'})
        format9 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True,
                                       'top': True, 'bottom': True, 'right': 2, 'left': True,
                                       'border_color': '000000'})
        format7 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True, 'bg_color': '#cccccc',
                                       'top': True, 'bottom': True, 'right': True, 'left': True,
                                       'border_color': '000000', 'border': 2})
        format11 = workbook.add_format({'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': True,
                                        'top': True, 'bold': True})
        formatred = workbook.add_format({'bg_color': '#ff0000'})
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,'align': 'center',})
        justify1 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,'align': 'center','bold':True})
        justify2 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12,'align': 'center','bold':True})
        justify3 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,'align': 'center'})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        boldc = workbook.add_format({'bold': True, 'align': 'center',})
        boldr = workbook.add_format({'bold': True, 'align': 'right'})
        boldl = workbook.add_format({'bold': True, 'align': 'left'})
        boldl.set_font_color('white')
        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center','font_size': 8,})
        right = workbook.add_format({'align': 'right'})
        left = workbook.add_format({'align': 'left',})
        boldcolor = workbook.add_format({'bold': True,'align': 'center', 'bg_color': '#8FBC8F','border_color': 'black','bottom': True, 'top': True, 'right': True, 'left': True,})
        left_qty = workbook.add_format({'align': 'left', 'bg_color': '#a0a5a6'})
        bound_width_height = (180, 160)
        worksheet.merge_range('A1:D4', ' ' , center)
        worksheet.merge_range('F1:J1', 'KGM APPLIANCES LLP' , boldc)
        worksheet.merge_range('F2:J2', 'PTS TOWER, CALICUT ROAD, THURAKKAL' , boldc)
        worksheet.merge_range('F3:J3', 'MANJERI, MALAPPURAM DT, KERALA 676121' , boldc)
        worksheet.merge_range('A5:J5', 'PAY SLIP' , boldcolor)
        worksheet.merge_range('A6:B6', 'EMPLOYEE ID' , justify)
        worksheet.merge_range('F6:G6', 'REF NO.' , justify)
        worksheet.merge_range('A7:B7', 'EMPLOYEE NAME' , justify)
        worksheet.merge_range('F7:G7', 'PAYMONTH' , justify)
        worksheet.merge_range('A8:B8', 'DESIGNATION' , justify)
        worksheet.merge_range('F8:G8', 'EPF A/C NO.' , justify)
        worksheet.merge_range('A9:B9', 'COST CENTRE' , justify)
        worksheet.merge_range('F9:G9', 'UAN NO.' , justify)
        worksheet.merge_range('A10:B10', 'EMPLOYEE PAN' , justify)
        worksheet.merge_range('F10:G10', 'ESI IP NO.' , justify)
        worksheet.merge_range('A11:B11', 'WORKING DAYS' , justify)
        worksheet.merge_range('E11:F11', 'PRESENT' , justify3)
        worksheet.write('I11', 'LOP DAYS' , justify)
        worksheet.merge_range('A12:B12', 'CASUAL LEAVES' , justify)
        worksheet.merge_range('E12:F12', 'TOTAL CL AVAILED' , justify3)
        worksheet.write('I12', 'TA WORKS' , justify)
        worksheet.merge_range('A13:J13', 'PAYMENT DETAILS' , boldcolor)

        record=self.env['hr.payslip'].browse(data['id'])

        worksheet.write('A14','SL NO' , justify1)
        worksheet.merge_range('B14:D14', 'EARNINGS' , justify1)
        worksheet.write('E14', 'AMOUNT' , justify1)
        worksheet.write('F14', 'SL NO' , justify1)
        worksheet.merge_range('G14:I14', 'DEDUCTIONS' , justify1)
        worksheet.write('J14', 'AMOUNT' , justify1)
        slno = 1
        slno1 = 1
        new = 15
        new_row = new 
        for each in record:
            total_alw = 0
            total_ded = 0
            net_amount = 0
            if each.employee_id.company_id.logo:
                image_byte_stream = io.BytesIO(base64.b64decode(each.employee_id.company_id.logo))
                image_data = self.get_resized_image_data(image_byte_stream, bound_width_height)
                worksheet.insert_image('A1:D4', 'Header',{'image_data': image_data,'x_offset':50,'y_offset':2})
            worksheet.merge_range('C6:E6', each.employee_id.employeeid, justify)
            worksheet.merge_range('C9:E9', each.employee_id.department_id.name, justify)
            worksheet.merge_range('C10:E10', each.employee_id.pan_no, justify)
            for line in each.worked_days_line_ids:
                if line.code =='TD100':
                    worksheet.merge_range('C11:D11', line.number_of_days, justify3)
                if line.code == 'WORK100':
                    worksheet.merge_range('G11:H11', line.number_of_days, justify3)
            worksheet.merge_range('C7:E7', each.employee_id.name , justify)
            worksheet.merge_range('C8:E8', each.employee_id.job_id.name if each.employee_id.job_id else '' , justify)
            aw = str(each.date_to.strftime("%B-%Y"))
            worksheet.merge_range('H7:J7', aw, justify)
            worksheet.merge_range('H6:J6', each.number, justify)
            worksheet.merge_range('H8:J8', each.employee_id.epf_account_no, justify)
            worksheet.merge_range('H9:J9', each.employee_id.epf_uan_no, justify)
            worksheet.merge_range('H10:J10', each.employee_id.esi_ip_no, justify)
            values = self.env['hr.leave'].search([('employee_id', '=', each.employee_id.name)])
            value = self.env['hr.leave.allocation'].search([('employee_id', '=', each.employee_id.name)])
            total = 0
            total_paid = 0
            for data in values:
                if each.date_from <= data.request_date_from and each.date_to >= data.request_date_to: 
                    if data.holiday_status_id.name == 'Unpaid':
                        total += data.number_of_days
                    if data.holiday_status_id.name == 'Paid Time Off':
                        total_paid += data.number_of_days
                worksheet.write('J11', total , justify3)
                worksheet.merge_range('G12:H12', total_paid, justify3)
            for i in value:
                if i.holiday_status_id.name == 'Paid Time Off':
                    worksheet.merge_range('C12:D12', i.number_of_days, justify3)
            total_work = 0
            field_obj = self.env['bi.complaint.registration'].search([('user_id.name', '=', each.employee_id.name),('purchase_date','>=',each.date_from),('purchase_date','<=',each.date_to)])
            total_work = len(field_obj)
            worksheet.write('J12', total_work , justify3)


            for val in each.line_ids:
                if val.category_id.code== 'BASIC' or val.category_id.code == 'ALW':
                    worksheet.write('A%s' %new, slno , justify3)
                    slno += 1
                    worksheet.merge_range('B%s:D%s'  %(new, new), val.name,justify)
                    worksheet.write('E%s' %new, val.total , justify)
                    total_alw += val.total
                    new += 1
                elif val.category_id.code == 'DED':
                    worksheet.write('F%s' %new_row, slno1 , justify3)
                    slno1 += 1
                    worksheet.merge_range('G%s:I%s'  %(new_row, new_row), val.name,justify)
                    worksheet.write('J%s' %new_row, val.total,justify)
                    total_ded += val.total
                    new_row += 1
            new = new_row 
            worksheet.merge_range('A%s:D%s'  %(new_row, new_row), 'TOTAL COST TO COMPANY',justify1)
            worksheet.write('E%s' %new_row, total_alw , justify1)
            worksheet.merge_range('F%s:I%s'  %(new_row, new_row), 'TOTAL DEDUCTIONS',justify1)
            worksheet.write('J%s' %new_row, total_ded, justify1)
            new_row+=2
            net_amount = total_alw - total_ded
            net_amount = round(net_amount,2)
            worksheet.merge_range('A%s:D%s'  %(new_row, new_row+1), 'NET PAYABLE AMOUNT INR',justify2)
            worksheet.merge_range('E%s:F%s'  %(new_row, new_row+1), net_amount ,justify1)
            worksheet.merge_range('G%s:H%s'  %(new_row, new_row), 'MODE OF PAYMENT',justify)
            worksheet.merge_range('I%s:J%s'  %(new_row, new_row), each.contract_id.journal_id.name,justify)
            new_row+=1
            worksheet.merge_range('G%s:H%s'  %(new_row, new_row), 'BANK NAME',justify)
            worksheet.merge_range('I%s:J%s'  %(new_row, new_row), each.employee_id.bank_name,justify)
            new_row+=1
            worksheet.merge_range('A%s:F%s'  %(new_row, new_row+1), num2words(net_amount).title()+ ' only',justify1)
            worksheet.merge_range('G%s:H%s'  %(new_row, new_row), 'BANK ACCOUNT No.',justify)
            worksheet.merge_range('I%s:J%s'  %(new_row, new_row), each.employee_id.bank_account_no,justify)
            new_row+=1
            worksheet.merge_range('G%s:H%s'  %(new_row, new_row), 'PAYMENT DATE',justify)
            worksheet.merge_range('I%s:J%s'  %(new_row, new_row), str(each.create_date.strftime("%d-%m-%Y")),justify)
            new_row+=4
            worksheet.merge_range('A%s:D%s'  %(new_row, new_row), 'For KGM APPLIANCES LLP',boldc)
            new_row+=1
            worksheet.merge_range('G%s:H%s'  %(new_row, new_row), 'DATE',center)
            worksheet.write('I%s' %new_row,  str(each.create_date.strftime("%d-%m-%Y")), center)
            new_row+=1
            worksheet.merge_range('G%s:H%s'  %(new_row, new_row), 'PLACE',center)
            worksheet.write('I%s' %new_row,  each.employee_id.company_id.street, center)
            new_row+=2
            worksheet.merge_range('A%s:J%s'  %(new_row, new_row), 'This is a System Generated Pay Slip',center)
            new_row+=2
            worksheet.merge_range('A%s:J%s'  %(new_row, new_row), 'Website:'+ each.employee_id.company_id.website +'    Email:'+ each.employee_id.company_id.email,center)






