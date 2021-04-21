# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class bi_inward_rpt(models.Model):
#     _inherit = 'stock.picking'
    
#     first_weight = fields.Float(String="First Weight")
#     second_weight = fields.Float(String="Second Weight")
#     global_port_net_weight = fields.Float(String="Global Port Net Weight")

class bi_inward_rpt_2(models.Model):
    _inherit = 'stock.move'
    
    first_weight = fields.Float(String="First Weight")
    second_weight = fields.Float(String="Second Weight")
    global_port_net_weight = fields.Float(String="Global Port Net Weight")    


