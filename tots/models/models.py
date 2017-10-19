# -*- coding: utf-8 -*-

from odoo import models, fields, api

class net(models.Model):
     _name = 'tots.net'

     name = fields.Char()
     mask = fields.Integer()
     net_map = fields.Binary()
     net_class = fields.Selection([('a','A'),('b','B'),('c','C')])
     pcs = fields.One2many('tots.pc','net')
     servers = fields.Many2many('tots.pc',relation='net_servers')          

class pc(models.Model):
     _name = 'tots.pc'

     name = fields.Char()
     ping = fields.Float()
     registered = fields.Date()
     uptime = fields.Datetime()
     net = fields.Many2one('tots.net')
     servers = fields.Many2many('tots.net',relation='net_servers')          
