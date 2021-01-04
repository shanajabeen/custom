# -*- coding: utf-8 -*-
from odoo import http

# class BiManufacturingReport(http.Controller):
#     @http.route('/bi_manufacturing_report/bi_manufacturing_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bi_manufacturing_report/bi_manufacturing_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bi_manufacturing_report.listing', {
#             'root': '/bi_manufacturing_report/bi_manufacturing_report',
#             'objects': http.request.env['bi_manufacturing_report.bi_manufacturing_report'].search([]),
#         })

#     @http.route('/bi_manufacturing_report/bi_manufacturing_report/objects/<model("bi_manufacturing_report.bi_manufacturing_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bi_manufacturing_report.object', {
#             'object': obj
#         })