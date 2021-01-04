# -*- coding: utf-8 -*-
# from odoo import http


# class DisTest(http.Controller):
#     @http.route('/dis_test/dis_test/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dis_test/dis_test/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dis_test.listing', {
#             'root': '/dis_test/dis_test',
#             'objects': http.request.env['dis_test.dis_test'].search([]),
#         })

#     @http.route('/dis_test/dis_test/objects/<model("dis_test.dis_test"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dis_test.object', {
#             'object': obj
#         })
