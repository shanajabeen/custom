# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class ManufacturingOrderReport(models.TransientModel):
    _name = 'manufacturing.order.report.wizard'
    
    def _check_dates(self, date_from, date_to):
        if date_from > date_to:
            raise UserError("Start-date must be lower than End-date")
        return True

    date_from = fields.Date("Date From")
    date_to = fields.Date("Date To")
    

    def export_xls(self):
        self._check_dates(self.date_from, self.date_to)
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'account.move'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('bi_manufacturing_report.view_manufacturing_order_report').report_action(self, data=datas,
                                                                                                     config=False)

                                                                                                     
