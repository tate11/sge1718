# -*- coding: utf-8 -*-
from odoo import http

# class Tots(http.Controller):
#     @http.route('/tots/tots/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tots/tots/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tots.listing', {
#             'root': '/tots/tots',
#             'objects': http.request.env['tots.tots'].search([]),
#         })

#     @http.route('/tots/tots/objects/<model("tots.tots"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tots.object', {
#             'object': obj
#         })