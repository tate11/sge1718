# -*- coding: utf-8 -*-

from odoo import models, fields, api

class llista(models.Model):
     _name = 'exone.llista'

     name = fields.Char()
     llista = fields.One2many('exone.elements','llista',copy=True)
     @api.multi
     def duplicar(self):
      for l in self:
       l.copy()


class elements(models.Model):
     _name = 'exone.elements'

     name = fields.Char()
     llista = fields.Many2one('exone.llista')
