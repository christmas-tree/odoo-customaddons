# -*- coding: utf-8 -*-
# from odoo import http


# class Test1(http.Controller):
#     @http.route('/warranty/warranty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/warranty/warranty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('warranty.listing', {
#             'root': '/warranty/warranty',
#             'objects': http.request.env['warranty.warranty'].search([]),
#         })

#     @http.route('/warranty/warranty/objects/<model("warranty.warranty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('warranty.object', {
#             'object': obj
#         })
