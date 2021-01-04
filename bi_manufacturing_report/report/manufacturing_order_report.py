import xlsxwriter
from odoo import api, fields, models
import datetime
from datetime import datetime, timedelta, date
import odoo.addons.decimal_precision as dp
import re
import time
import string
import collections
from odoo.exceptions import UserError


class ManufacturingOrderReportXls(models.AbstractModel):
    _name = 'report.bi_manufacturing_report.report_manufacturing_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        worksheet = workbook.add_worksheet("Production Report")
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
        format3 = workbook.add_format({'bottom': True, 'top': True, 'font_size': 12})
        font_size_8 = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8})
        red_mark = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 8,
                                        'bg_color': 'red'})
        justify = workbook.add_format({'bottom': True, 'top': True, 'right': True, 'left': True, 'font_size': 12})
        format3.set_align('center')
        font_size_8.set_align('center')
        justify.set_align('justify')
        format1.set_align('center')
        red_mark.set_align('center')
        boldc = workbook.add_format({'bold': True, 'align': 'center'})
        boldr = workbook.add_format({'bold': True, 'align': 'right'})
        boldl = workbook.add_format({'bold': True, 'align': 'left'})
        bold = workbook.add_format({'bold': True})
        center = workbook.add_format({'align': 'center'})
        right = workbook.add_format({'align': 'right'})
        left = workbook.add_format({'align': 'left'})
        worksheet.merge_range('A1:I1', 'MANUFACTURING ORDER REPORT', boldc)
        filter_row = 3
        filter_row1 = 4
        if data['form']['date_from']:
            date_from = datetime.strptime(data['form']['date_from'], '%Y-%m-%d').date()
            worksheet.write('A%s' % filter_row, 'Date From', boldl)
            worksheet.write('B%s' % filter_row, str(date_from.strftime("%d-%m-%Y")), left)
        if data['form']['date_to']:
            date_to = datetime.strptime(data['form']['date_to'], '%Y-%m-%d').date()
            worksheet.write('E%s' % filter_row, 'Date To', boldl)
            worksheet.write('F%s' % filter_row, str(date_to.strftime("%d-%m-%Y")), left)
        row = 6
        new_row = row + 1
        qty_row = new_row
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 30)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 12)
        worksheet.set_column('E:E', 12)
        worksheet.set_column('F:F', 12)
        worksheet.write('A%s' % row, 'Order Number', boldl)
        worksheet.write('B%s' % row, 'Product', boldl)
        worksheet.write('C%s' % row, 'Unit Of Measure', boldl)
        worksheet.write('D%s' % row, 'Quantity', boldl)
        worksheet.write('E%s' % row, 'Date', boldl)
        m_order = self.env['mrp.production'].search([('state', 'in', ['progress', 'done','cancel'])])
        for each in m_order:
            for line in each.finished_move_line_ids.filtered(lambda x: x.state == 'done'):
                move_line_date = line.date + timedelta(hours=5, minutes=30)
                move_date = move_line_date.date()
                if (move_date >= date_from) and (move_date <= date_to) and line.qty_done > 0:
                    worksheet.write('A%s' % new_row, each.name, left)
                    worksheet.write('B%s' % new_row, line.product_id.name, left)
                    worksheet.write('C%s' % new_row, line.product_uom_id.name, left)
                    worksheet.write('D%s' % new_row, line.qty_done, right)
                    worksheet.write('E%s' % new_row, str(move_date.strftime("%d-%m-%Y")), left)
                    new_row += 1
                    