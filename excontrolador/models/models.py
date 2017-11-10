# -*- coding: utf-8 -*-

from odoo import models, fields, api
     
class comunity(models.Model):
     _name = 'excontrolador.comunity'

     name = fields.Char()
     country = fields.Many2one('res.country')

class province(models.Model):
     _name = 'excontrolador.province'

     name = fields.Char()
     comunity = fields.Many2one('excontrolador.comunity')

class town(models.Model):
     _name = 'excontrolador.town'

     name = fields.Char()
     province = fields.Many2one('excontrolador.province')

class street(models.Model):
     _name = 'excontrolador.street'

     name = fields.Char()
     town = fields.Many2one('excontrolador.town')


class shipping(models.Model):
     _name = 'excontrolador.shipping'

     name = fields.Char()
     street = fields.Many2one('res.street')
     address = fields.Char()
