# -*- coding: utf-8 -*-
from odoo import http

# class League(http.Controller):
#     @http.route('/league/league/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/league/league/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('league.listing', {
#             'root': '/league/league',
#             'objects': http.request.env['league.league'].search([]),
#         })

#     @http.route('/league/league/objects/<model("league.league"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('league.object', {
#             'object': obj
#         })