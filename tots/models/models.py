# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError

class net(models.Model):
     _name = 'tots.net'

     name = fields.Char()
     net_ip = fields.Char()
     mask = fields.Integer()
     net_map = fields.Binary()
     net_class = fields.Selection([('a','A'),('b','B'),('c','C')])
     pcs = fields.One2many('tots.pc','net')
     servers = fields.Many2many('tots.pc',relation='net_servers')          

class pc(models.Model):
     _name = 'tots.pc'

     name = fields.Char(default="PC")
     number = fields.Integer()
     ip = fields.Char(compute='_get_ip')
     ping = fields.Float()

     def _get_date(self):
       print self
       return fields.Date.today()


     registered = fields.Date(default=_get_date)
     uptime = fields.Datetime(default=lambda self: fields.Datetime.now())
     net = fields.Many2one('tots.net')
     servers = fields.Many2many('tots.net',relation='net_servers')  

     @api.depends('number','net')
     def _get_ip(self):
       print self
       for pc in self:
         print pc
         pc.ip=str(pc.net.net_ip)+str(pc.number)

     @api.constrains('number')
     def _check_number(self):
       for pc in self:
        if pc.number > 254:
            raise ValidationError("The IP must be under 254: %s" % pc.number)        
