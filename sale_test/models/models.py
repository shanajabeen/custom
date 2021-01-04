# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SALES_TEST(models.Model):
    _inherit='sale.order'
    
    _description = 'sale_test.sale_test'

    submit=fields.Char("submit")
    newsale = fields.Char(string="newsale")
    newsale1 = fields.Char(string="newsale")
    mydata = fields.Char(string="mydata")
    check = fields.Boolean(default=False)
    def print(self):
        print("True")
    
    def okfun(self):
        if self.check:
            self.check = False
        else:
            self.check = True
    def hello (self):
        print("True")     