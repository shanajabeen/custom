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
from PIL import Image
import io


class AbsenteeXlsx(models.AbstractModel):
    _name = 'report.school_attendance.absentee_xls'
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
        worksheet = workbook.add_worksheet("ABSENTEE REPORT 1")
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
        
        worksheet.merge_range('A1:B5','', format5)
        worksheet.merge_range('F1:G5','', format5)
        
        image_height = 182.0

        image_width = 140.0
        cell_width = 50.0
        cell_height = 56.0

        x_scale = cell_width/image_width
        y_scale = cell_height/image_height

        
        row1=10    
        row = 12
        worksheet.write('A%s' % row1,"DATE:", center)  
        worksheet.write('B%s' % row1,data['form']['date'], center)  
        new_row = row + 1
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 25)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 25)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 25)
        worksheet.set_column('G:G', 25)
        bound_width_height = (180, 140)
        domain=[]
        
        docs = self.env['res.company'].search([('id','=',2)])
        for each in docs:
            if each.favicon:
                image_byte_stream = io.BytesIO(base64.b64decode(each.favicon))
                image_data = self.get_resized_image_data(image_byte_stream, bound_width_height)
                worksheet.insert_image('A3:B5', 'Employee Image',{'image_data': image_data,'x_offset':70,'y_offset':11}) 
            worksheet.merge_range('C1:E5', 'INDIAN SCHOOL AL GHUBRA',format5 )

            if each.logo:
                image_byte_stream = io.BytesIO(base64.b64decode(each.logo))
                image_data = self.get_resized_image_data(image_byte_stream, bound_width_height)
                worksheet.insert_image('G2:H2', 'Header',{'image_data': image_byte_stream,'x_scale': x_scale, 'y_scale': y_scale})
                
            

        count=0
        sl_no = 1
        worksheet.merge_range('A8:G8', 'ABSENTEE REPORT', format5)
        worksheet.write('A%s' % row, 'SL NO', format1)
        worksheet.write('B%s' % row, 'Student Name', format1)
        worksheet.write('C%s' % row, 'Representing School', format1)
        worksheet.write('D%s' % row, 'GR#', format1)
        worksheet.write('E%s' % row, 'Academic Class', format1)
        worksheet.write('F%s' % row, 'Parent Name', format1)
        worksheet.write('G%s' % row, ' Mobile', format1)
        docs = self.env['daily.attendance'].search([('date', '=',data['form']['date'])])
        for each in docs: 
            for i in each.student_ids:
                if i.is_absent==True:
                    worksheet.write('A%s' % new_row, sl_no, center)
                    worksheet.write('B%s' % new_row, i.stud_id.name, center)
                    if i.is_representing_school == True:
                                rep = 'YES'
                    if i.is_representing_school == False:
                                rep = ' ' 
                    worksheet.write('C%s' % new_row,rep, center)
                    worksheet.write('D%s' % new_row,i.stud_id.student_code, center)
                    worksheet.write('E%s' % new_row,each.standard_id.name, center) 
                    worksheet.write('F%s' % new_row,i.stud_id.father_name, center)
                    worksheet.write('G%s' % new_row,i.stud_id.contact_mobile, center) 
                    new_row+=1
                    sl_no+=1   
                    count= count+1
        worksheet.write('F%s' % new_row,"count", center)    
        worksheet.write('G%s' % new_row, count, format1)     





       

