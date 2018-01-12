# -*- coding: utf-8 -*-i

from odoo import models, fields, api
from datetime import datetime, timedelta
     
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
     a = fields.Integer(compute='_a')
     def _a(self):
       for i in sefl:
         i.a=33

class shipping(models.Model):
     _name = 'excontrolador.shipping'

     name = fields.Char()
     street = fields.Many2one('excontrolador.street')
     town = fields.Many2one(related='street.town')
     province = fields.Many2one(related='street.town.province')
     comunity = fields.Many2one(related='street.town.province.comunity')

     townaux = fields.Many2one('excontrolador.town', store=False)
     provinceaux = fields.Many2one('excontrolador.province', store=False)
     comunityaux = fields.Many2one('excontrolador.comunity', store=False)

     address = fields.Char()
     client = fields.Many2one('res.partner')
     driver = fields.Many2one('excontrolador.driver')
     @api.onchange('comunityaux')
     def _filter_province(self):
        print "comunity"
        return { 'domain': {'provinceaux': [('comunity','=',self.comunityaux.id)]} }   

     @api.onchange('provinceaux')
     def _filter_town(self):
        print "province"+str(self.provinceaux.id)
        return { 'domain': {'townaux': [('province','=',self.provinceaux.id)]} }   

     @api.onchange('townaux')
     def _filter_street(self):
        print "town"
        return { 'domain': {'street': [('town','=',self.townaux.id)]} }   


     ######################################################################
     #################Coses en les dates###################################

     ship_date = fields.Datetime(default=lambda self: fields.Datetime.now())
     estimated_time = fields.Integer(string="Estimated time in hours",default=1)
     delivery_date = fields.Datetime(compute='_get_delivery')
     return_date = fields.Datetime()
     days_before_return = fields.Float(compute='_get_days')
          

     @api.depends('ship_date','estimated_time')
     def _get_delivery(self):
       for i in self:
        if i.ship_date != False:
         data=fields.Datetime.from_string(i.ship_date)
         data=data+timedelta(hours=i.estimated_time)
         i.delivery_date=fields.Datetime.to_string(data)

     @api.depends('return_date','estimated_time','delivery_date')
     def _get_days(self):
       for i in self:
        if i.return_date != False:
         delivery_date=fields.Datetime.from_string(i.delivery_date)
         return_date=fields.Datetime.from_string(i.return_date)
         diff=return_date-delivery_date
         i.days_before_return = diff.total_seconds()/60/60/24

<<<<<<< HEAD
class prod(models.Model):
     _name = 'excontrolador.prod'
     product_id = fields.Many2one('product.template','Select a product')
     name = fields.Char(related='product_id.name',required="true",readonly="true")
#     list_price = fields.Float(related='product_id.list_price',readonly="true")
#     standard_price = fields.Float(related='product_id.standard_price',readonly="true")
#     type = fields.Selection(related='product_id.type')
     categ_id = fields.Many2one('product.category','Category')
     image_medium = fields.Binary(related='product_id.image_medium',String="Image")
     #qty_available = fields.Float(related='product_id.qty_available')
=======
    #############################################################################
    ################# Coses de herència #######################################

    ###### Herència de classe #############

class client(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    shippings = fields.One2many('excontrolador.shipping','client')
    alternative_address = fields.Char()


    ########## Herència per prototip #############

class driver(models.Model):
   _name = 'excontrolador.driver'
   _inherit = 'res.partner'

   repartos = fields.One2many('excontrolador.shipping','driver')  
   
    ############ Herència múltiple ###############

class soci(models.Model):
   _name = 'excontrolador.soci'
   _inherits = {'res.partner': 'partner_id'} 

   #partner_id = fields.Many2one('res.partner')
   n_soci = fields.Char()
   descompte = fields.Float()   
>>>>>>> 72979c26d9df0f4058db143876dc41f7a086e648
