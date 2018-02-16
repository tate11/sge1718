# -*- coding: utf-8 -*-
from odoo import http

# class Exone(http.Controller):
#     @http.route('/exone/exone/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exone/exone/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exone.listing', {
#             'root': '/exone/exone',
#             'objects': http.request.env['exone.exone'].search([]),
#         })

#     @http.route('/exone/exone/objects/<model("exone.exone"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exone.object', {
#             'object': obj
#         })