# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare
from datetime import date, datetime
from datetime import datetime, timedelta

class BiSaleorder1(models.Model):
    _inherit = 'sale.order'

    type_ = fields.Selection([
        ('FT', 'FileOut (FT)'),('JO', 'Joining (JO)'),('MA', 'Maintenance (MA)')
    ], string='Type',required=True)

    emirates = fields.Selection([
        ('DXB', 'Dubai (DXB)'),('SHJ', 'Sharjah (SHJ)'),('AJM', 'Ajman (AJM)'),('AUX', 'Abu Dhabi (AUX)'),('RAK', 'Ras Al Khaimah (RAK)'),('FUJ', 'Fujairah (FUJ)'),('UAQ', 'Umm Al Quawain (UAQ)')
    ], string='Emirates',required=True)

   

    @api.model
    def create(self, vals):
        result = super(BiSaleorder1, self).create(vals)
        for res in result:
            type1 = res.type_
            emirate = res.emirates
            year =date.today().year
            end_code = self.env['ir.sequence'].next_by_code('self.service2')
            res.name = 'PI'+"/"+emirate+"/"+type1+"/"+"Q-"+str(year)+"/"+end_code
        return result