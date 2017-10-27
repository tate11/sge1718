# -*- coding: utf-8 -*-
from odoo import http

# class Productdata(http.Controller):
#     @http.route('/productdata/productdata/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/productdata/productdata/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('productdata.listing', {
#             'root': '/productdata/productdata',
#             'objects': http.request.env['productdata.productdata'].search([]),
#         })

#     @http.route('/productdata/productdata/objects/<model("productdata.productdata"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('productdata.object', {
#             'object': obj
#         })