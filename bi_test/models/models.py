# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class b3Test(models.Model):
    _name = 'b3.test'
    _description = 'description'
    hobby= fields.Char('hobby')
    kk=fields.Char('hobby2')
class BiTest(models.Model):
    _name = 'bi.test'
    _description = 'description'

    name = fields.Char(string='Name',size=5,help='enter name',required='True')
    salary = fields.Float(string='salary')
    age= fields.Integer('age')
    # vehicle=fields.Binary('vehicle')
    gender=fields.Selection([('male', 'm'),('female','f')])
    # gender=fields.Selection(selection_add=[('k','j'),('j','h')])
    total=fields.Integer(string="age+10",compute='add')
    @api.depends('age')
    def add(self):
        for x in self:
            if (x.age==0):
                x.total=0
            else:    
                x.total=x.age+10
            
    datenow = fields.Datetime('Date current action', required=False, readonly=False, select=True, default=lambda self: fields.datetime.now())        
    one2_ids=fields.One2many('b2.test','details_id')

    # create methord
    def myfun(self):
        for rec in self:
            vals={"salary1":self.salary,"age1":self.age}
            self.env['b2.test'].create(vals)
            # vals={"salary":1001,"age1":10}
            # self.env['b2."test'].create(vals)
            #   vals={"name":"jabi","salary":10,"age":10,"gender":'male'}
    
            #   self.env['bi.test'].create(vals)
    # write function   
    def myfun2(self):
        record_ids = self.env['bi.test'].search([('name', '=', 'dsfd')])
        for record in record_ids:
            record.write({
                'salary': 1000,
                'age': 30,

            })
     
class B2Test(models.Model):
    _name = 'b2.test'
    _description = 'description'

    details_id=fields.Many2one('bi.test')
    salary1 = fields.Float(string='salary1')
    age1= fields.Integer('age1')
    mm=fields.Many2many('b3.test',"school_hobby","student_id","hobby_id")

