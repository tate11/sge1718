# -*- coding: utf-8 -*-
from odoo import http

# class Excontrolador(http.Controller):
#     @http.route('/excontrolador/excontrolador/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/excontrolador/excontrolador/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('excontrolador.listing', {
#             'root': '/excontrolador/excontrolador',
#             'objects': http.request.env['excontrolador.excontrolador'].search([]),
#         })

#     @http.route('/excontrolador/excontrolador/objects/<model("excontrolador.excontrolador"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('excontrolador.object', {
#             'object': obj
#         })