from odoo import models, fields, api,_
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
from calendar import monthrange
import string


class AbsenteeXlsx(models.AbstractModel):
    _name = 'report.school_attendance.late_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_resized_image_data(self, byte_stream, bound_width_height):
        im = Image.open(byte_stream)
        im.thumbnail(bound_width_height, Image.ANTIALIAS)  
        im_bytes = io.BytesIO()
        im.save(im_bytes, format='PNG')
        return im_bytes

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("Late Report")
        format1 = workbook.add_format({'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center',})
        format2 = workbook.add_format({'font_size': 10, 'bottom': True, 'right': True, 'left': True, 'top': True,
                                       'align': 'center','font_color':'red',})                               
        format12 = workbook.add_format(
            {'font_size': 12, 'align': 'center', 'right': True, 'left': True, 'bottom': False,
             'top': True, 'bold': True,})
        format5 = workbook.add_format({'font_size': 18, 'bottom': True, 'right': True, 'left': True, 'top': True,
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
        worksheet.merge_range('E1:F5','', format5)
        bound_width_height = (180, 140)
        image_height = 182.0
        dict1={}
        image_width = 140.0
        cell_width = 50.0
        cell_height = 56.0
        x_scale = cell_width/image_width
        y_scale = cell_height/image_height
        row1=8    
        row = 12
        docs = self.env['res.company'].search([('id','=',2)])
        count=0
        for each in docs:
            if each.favicon:
                image_byte_stream = io.BytesIO(base64.b64decode(each.favicon))
                image_data = self.get_resized_image_data(image_byte_stream, bound_width_height)
                worksheet.merge_range('A1:D5', '',format5 )
                worksheet.insert_image('A1:D5', 'Employee Image',{'image_data': image_data,'x_offset':70,'y_offset':11}) 
            worksheet.merge_range('E1:AA5', 'INDIAN SCHOOL AL GHUBRA',format5 )

            if each.logo:
                image_byte_stream = io.BytesIO(base64.b64decode(each.logo))
                image_data = self.get_resized_image_data(image_byte_stream, bound_width_height)
                worksheet.merge_range('AB1:AE5', '',format5 )
                worksheet.insert_image('AB1:AD5', 'Header',{'image_data': image_byte_stream,'x_scale': x_scale, 'y_scale': y_scale})
                
        worksheet.write('A%s' % 11,"COUNT:", format1)
        worksheet.write('A%s' % 7,"CLASS:", format1)
        worksheet.write('B%s' % 7,data['form']['class12'], format1)
        worksheet.write('A%s' % 8,"YEAR:", format1)
        worksheet.write('B%s' % 8,data['form']['year2'], format1)
        worksheet.write('A%s' % 9,"TEACHER:", format1)
        worksheet.write('B%s' % 9,data['form']['teach'], format1)
        worksheet.write('A%s' % 10,"MONTH:", format1)  
        worksheet.write('B%s' % 10,data['form']['month'], format1)
        row1+=1 


        worksheet.merge_range('A6:AE6', 'Late Comers', format12)
        v=13     
        docs1 = self.env['daily.attendance.line'].search([('standard_id.academic_year','=',data['form']['year']),('standard_id.standard_id','=',data['form']['class1'])]).mapped('stud_id')
       
        for each in docs1:
            docs11 = self.env['daily.attendance.line'].search([('stud_id','=',each.id),('standard_id.academic_year','=',data['form']['year']),('standard_id.standard_id','=',data['form']['class1']),('is_late','=',True)])
            
            for each in docs11:
                if each.standard_id.date.month == 1:
                    k='January'
                elif each.standard_id.date.month == 2:
                    k='February'   
                elif each.standard_id.date.month == 3:
                    k='March'  
                elif each.standard_id.date.month == 4:
                    k='April'    
                elif each.standard_id.date.month == 5:
                    k='May'    
                elif each.standard_id.date.month == 6:
                    k='June'    
                elif each.standard_id.date.month == 7:
                    k='July'    
                elif each.standard_id.date.month == 8:
                    k='August'    
                elif each.standard_id.date.month == 9:
                    k='September'    
                elif each.standard_id.date.month == 10:
                    k='October'     
                elif each.standard_id.date.month == 11:
                    k='November'      
                elif each.standard_id.date.month == 12:
                    k='December' 
               
                if k == data['form']['month']:
                    m=2
                    month_obj = each.standard_id.date
                    days = monthrange( month_obj.year, month_obj.month)[1]
                    list2 =[]
                    if days==28:
                        list2 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
                        list21 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28']
                    if days==29:
                        list2 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']  
                        list21 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']                    
                    if days==30:
                        list2 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
                        list21 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30']
                    if days==31:
                        list2 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
                        list21 =['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
                   
                   
                    name1=each.stud_id.name
                    l_time=each.late_time
                else:
                    list21=[]    
                
                for s in list21:            
                    if name1 not in dict1:
                        if s == str(each.standard_id.date.day):
                            dict1[name1]= { s :l_time  }
                        else:    
                            dict1[name1]= { s :'0' }
                        
                        
                    else:
                        if s in dict1[name1]:
                            if s == str(each.standard_id.date.day):
                                dict1[name1][str(s)]=l_time 
                            
                        else:
                            if s == str(each.standard_id.date.day):
                                dict1[name1][str(s)]=l_time 
                            else:        
                
                               dict1[name1][s]='0' 

        if len(dict1) != 0:        
            n2=2
            h=12
            worksheet.write('A%s' % 12, 'SL NO', format1)
            worksheet.write('B%s' % 12, 'NAME', format1)
            worksheet.set_column('B:B', 25)
           
            if len(list2) >= 26:
                alphabets = list(string.ascii_uppercase)
                letters = list(string.ascii_uppercase)
                for a in alphabets:
                    for b in alphabets:
                        letters.append('%s%s' % (a, b))
            else:
                letters = list(string.ascii_uppercase)             
            for k in list2:
                worksheet.write('%s%s' %(letters[n2],h),k, format2)
                n2+=1
                

            sl=1
            row1=13
            for z in dict1:
                tot=0
                worksheet.write('A%s' % row1, sl, format1)
                worksheet.write('B%s' % row1, z, format1)
                sl+=1
                row1+=1
                for i in dict1[z]:
                    if dict1[z][i]!='0':
                        tot+=dict1[z][i]
                        worksheet.write('%s%s' %(letters[m],v), dict1[z][i],format1)
                    else:
                        worksheet.write('%s%s' %(letters[m],v),'',format1)       
                    m+=1
                if len(list2)==28:
                    worksheet.write('AE%s' % v,tot, format1)
                if len(list2)==29:
                    worksheet.write('AF%s' % v,tot, format1)
                if len(list2)==30:
                    worksheet.write('AG%s' % v,tot, format1)        
                if len(list2)==31:
                    worksheet.write('AH%s' % v,tot, format1)       
                count+=1    
                m=2    
                v+=1
                 
            worksheet.write('B%s' % 11,count, format1) 
            if len(list2)==28:
                worksheet.write('AE%s' % 12,'OVERALL', format1)
            if len(list2)==29:
                worksheet.write('AF%s' % 12,'OVERALL', format1)
            if len(list2)==30:
                worksheet.write('AG%s' % 12,'OVERALL', format1)        
            if len(list2)==31:
                worksheet.write('AH%s' % 12,'OVERALL', format1) 
