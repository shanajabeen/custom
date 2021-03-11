# -*- coding: utf-8 -*-


from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'product.template'

    discount = fields.Boolean(string="applay discount")
