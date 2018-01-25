# -*- coding: utf-8 -*-

from odoo import models, fields, api

# Herència simple
class clients(models.Model):
     _inherit = 'res.partner'
     _name = 'res.partner'

     altura = fields.Float()
     peso = fields.Float()
     imc = fields.Float()
     is_cliente = fields.Boolean()

"""     @api.model
     def create(self,values):
        new = super(clients,self).create(values)
        print new
        print new.name
        self.env['h.socis'].create({'name':new.name,'client':new.id})
"""
# Herència per prototip
class socis(models.Model):
     _inherit = 'res.partner'
     _name = 'h.socis'

     client = fields.Many2one('res.partner')

# Herència múltiple
class multiple(models.Model):
     _inherits = {'res.partner':'partner_id'}
     _name = 'h.multiple'

     socis = fields.Many2many('h.socis')
