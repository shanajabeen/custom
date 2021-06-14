from odoo import _, api, fields, models
from datetime import date
from datetime import datetime


class BiProductBudgeting(models.Model):
    _name = 'bi.product.budgeting'
    _description = 'Product Budgeting'
    _rec_name = 'name'

    name = fields.Char(string='')
    branch_id = fields.Many2one('res.branch', string='Branch ID', default=lambda self:self.env.user.branch_id.id)
    year = fields.Selection([
        ('2015', '2015'),
        ('2016', '2016'),
        ('2017', '2017'),
        ('2018', '2018'),
        ('2019', '2019'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028'),
        ('2029', '2029'),
        ('2030', '2030'),
        ('2031', '2031'),
        ('2032', '2032'),
        ('2033', '2033'),
        ('2034', '2034'),
        ('2035', '2035')
    ], string='Year')
    semester = fields.Selection([
        ('s1', 'Semester 1'),
        ('s2', 'Semester 2')
    ], string='Semester')
    line_ids = fields.One2many('bi.product.budgeting.line', 'budgeted_id', string='Product Budget')
        
class BiProductBudgetingLine(models.Model):
    _name = 'bi.product.budgeting.line'
    _description = 'Product Budegting '

    budgeted_id = fields.Many2one('bi.product.budgeting', string='Product Budget')
    product_id = fields.Many2one('product.product', string='Products')
    budgeted_qty = fields.Float(string='Budgeted Quantity')
    last_budgeted_qty = fields.Float(string='Last Year Budgeted Qty',compute='_compute_last_budgeted_qty')
    price = fields.Float(string='Price')
    currency_id = fields.Many2one('res.currency')
    
    @api.depends('product_id')
    def _compute_last_budgeted_qty(self):
        for order in self:
            if order.product_id:
                year = order.budgeted_id.year
                semester = order.budgeted_id.semester
                if semester == 's1':
                    semester = 's2'
                    year = int(year) - 1
                else:
                    semester = 's1'
                ptg_calender = self.env['ptg.calendar.line'].sudo().search([('ptg_calendar_id.year', '=',year),('semester', '=', semester)])
                date_from = []
                date_to = []
                if ptg_calender:
                    for val in ptg_calender:
                        date_from.append(val.date_from)
                        date_to.append(val.date_to)
                    start_date = min(date_from)
                    end_date = max(date_to)
                    my_time = datetime.min.time()
                    start_datetime = datetime.combine(start_date, my_time)
                    end_datetime = datetime.combine(end_date, my_time)
                    purchase_line_id = self.env['purchase.order.line'].search([('date_order', '>=', start_datetime),('date_order', '<=', end_datetime),('state', '=', 'purchase'),('product_id', '=', order.product_id.id)])
                    qty = 0
                    if purchase_line_id:
                        for line in purchase_line_id:
                            qty += line.product_qty
                    year = order.budgeted_id.year
                    semester = order.budgeted_id.semester
                    if semester == 's1':
                        semester = 's2'
                        year = int(year) - 1
                    else:
                        semester = 's1'
                    budgeted_id = self.env['bi.product.budgeting.line'].search([('budgeted_id.year', '=', year),('budgeted_id.semester', '=', semester),('product_id', '=', order.product_id.id)])
                    if budgeted_id:
                        for budget in budgeted_id:
                            order.last_budgeted_qty =  budget.budgeted_qty - qty
                    else:
                        order.last_budgeted_qty =  0
                else:
                    order.last_budgeted_qty =  0
            else:
                order.last_budgeted_qty =  0
