

from odoo import models, fields, api


class bi_ecomerce(models.Model):
    _name = 'bi.ecomerce'
#     _description = 'bi_ecomerce.bi_ecomerce'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
