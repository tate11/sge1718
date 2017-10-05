# -*- coding: utf-8 -*-
from odoo import http

# class Modul1(http.Controller):
#     @http.route('/modul1/modul1/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/modul1/modul1/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('modul1.listing', {
#             'root': '/modul1/modul1',
#             'objects': http.request.env['modul1.modul1'].search([]),
#         })

#     @http.route('/modul1/modul1/objects/<model("modul1.modul1"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('modul1.object', {
#             'object': obj
#         })