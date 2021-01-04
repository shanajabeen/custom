# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WEDGET_TEST(models.Model):
    _name = 'wedget.test'
    _description = 'wedget_test'

    val=fields.Char("hello")