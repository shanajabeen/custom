# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
import xlsxwriter

class BiPackingSlipReport(models.AbstractModel):
    _name = 'report.bi_packing_slip.report_template_packing_slip'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self,workbook,data,lines):
        ws = workbook.add_worksheet('Packing Slip Report')

        format_header=workbook.add_format({'bold':True,'font_name':'Calibri Light','font_size':14,'align':'center','valign':'vcenter','bg_color':'92D050','border':1})
        format_sub_header=workbook.add_format({'bold':True,'font_name':'Calibri Light','font_size':11,'align':'center','valign':'vcenter','border':1})
        format_column_header=workbook.add_format({'bold':True,'font_name':'Calibri Light','font_size':12,'align':'center','valign':'vcenter','border':1})
        format_content=workbook.add_format({'bold':False,'font_name':'Calibri Light','font_size':12,'align':'center','valign':'vcenter','border':1})
        format_sum_total=workbook.add_format({'bold':True,'font_name':'Calibri Light','font_size':12,'align':'center','valign':'vcenter','border':1,'bg_color':'92D050'})
        ws.set_default_row(40)
        ws.set_column('C:C',50)
        ws.set_column('D:D',10)
        ws.set_column('E:E',10)
        ws.set_column('F:F',20)
        ws.set_column('G:G',30)

        
        rec_id=self.env['bi.packing.slip'].browse(data['id'])
        
        ws.write('B3','',format_header)
        ws.merge_range('C3:E3','PACKING SLIP',format_header) 
        ws.merge_range('F3:G3',rec_id.sequence_id,format_header) if rec_id.sequence_id else ws.merge_range('F3:G3','',format_header)
        ws.merge_range('B4:G4',rec_id.heading,format_header) if rec_id.heading else ws.merge_range('B4:G4','',format_header)
        ws.merge_range('B5:C5',rec_id.picking_id.name,format_header) if rec_id.picking_id.name else ws.merge_range('B5:C5','',format_header)
        ws.merge_range('D5:G5','SALE ORDER : %s'%rec_id.picking_id.sale_id.name,format_header)
        if rec_id.type == 'transport':
            ws.merge_range('B6:C6','VEHICLE NO : %s'%rec_id.vehicle_no,format_sub_header) if rec_id.vehicle_no else ws.merge_range('B6:C6','VEHICLE NO:',format_sub_header)
            ws.merge_range('F6:G6','DRIVER MOB : %s'%rec_id.driver_mob,format_sub_header) if rec_id.driver_mob else ws.merge_range('F6:G6','DRIVER MOB:',format_sub_header)
            ws.merge_range('D6:E6','DATE : %s'%rec_id.date.strftime("%d.%m.%Y"),format_sub_header) if rec_id.date else ws.merge_range('D6:E6','DATE:',format_sub_header)   
        else:
            ws.merge_range('B6:C6','LR NO : %s'%rec_id.lr_no,format_sub_header) if rec_id.lr_no else ws.merge_range('B6:C6','LR NO:',format_sub_header)
            ws.merge_range('D6:G6','DATE : %s'%rec_id.date.strftime("%d.%m.%Y"),format_sub_header) if rec_id.date else ws.merge_range('D6:E6','DATE:',format_sub_header)   
           
        ws.write('B7','SL NO',format_column_header)
        ws.write('C7','ITEM',format_column_header)
        ws.write('D7','KG',format_column_header)
        ws.write('E7','NOS',format_column_header)
        ws.write('F7','BUNDLES',format_column_header)
        ws.write('G7','',format_column_header)

        row=8
        sl_no=1
        kg_sum=0.0
        nos_sum=0
        bundles_sum=0

        for line in rec_id.packing_slip_ids:
            ws.write('B%s'%row,sl_no,format_content)
            ws.write('C%s'%row,line.product_id.name,format_content)
            ws.write('D%s'%row,line.kg,format_content)
            ws.write('E%s'%row,line.nos,format_content)
            ws.write('F%s'%row,line.bundles,format_content)
            ws.write('G%s'%row,line.description,format_content) if line.description else ws.write('G%s'%row,'',format_content)
            kg_sum=kg_sum+float(line.kg)
            nos_sum=nos_sum+float(line.nos)
            bundles_sum=bundles_sum+float(line.bundles)
            row=row+1
            sl_no=sl_no+1

        ws.write('B%s'%row,'',format_content)
        ws.write('C%s'%row,'',format_content)
        ws.write('D%s'%row,kg_sum,format_sum_total)
        ws.write('E%s'%row,nos_sum,format_sum_total)
        ws.write('F%s'%row,bundles_sum,format_sum_total)
        ws.write('G%s'%row,'',format_content)