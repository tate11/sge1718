# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
from dateutil.relativedelta import *
from openerp.exceptions import ValidationError
from datetime import timedelta, datetime

class cinema(models.Model):
     _name = 'cine.cinema'

     name = fields.Char()
     country = fields.Many2one('res.country', string='Country')
     address = fields.Char(string='Address')
     description = fields.Text()
     theaters = fields.One2many('cine.theater','cinema',string='Theaters')
     employees = fields.Many2many('hr.employee',string='Employees') 
     billboard = fields.Many2many('cine.movie',compute='_get_billbera',string='Billboard') 
     sessions = fields.Many2many('cine.session',compute='_get_billbera',string='Sessions') 
     current_projections = fields.Many2many('cine.session',compute='_get_billbera',string='Current Projections') 
     #programacio (queda la vista i mostrar progrés)
     @api.multi
     def _get_billbera(self):
      today = fields.date.today()
      now = fields.datetime.now()
      today7 = fields.date.today()+relativedelta(days=+7)
      for cine in self:
       billb = self.env['cine.session'].search([('theater.cinema.id','=',cine.id),('day','>=',today),('day','<',today7)])
       sessions = self.env['cine.session'].search([('theater.cinema.id','=',cine.id),('day','=',today)])
       current_projections = self.env['cine.session'].search([('theater.cinema.id','=',cine.id),('day','=',today)])
       aux_list = []
       for p in current_projections:
         if p.projectantse(p.id):
           aux_list.append(p.id)
       cine.billboard=billb.mapped('movie.id')
       cine.sessions=sessions.ids
       cine.current_projections=aux_list


class theater(models.Model):
     _name = 'cine.theater'

     name = fields.Char()
     cinema = fields.Many2one('cine.cinema',string='Cinema',ondelete='cascade')
     seats = fields.One2many('cine.seat','theater',string='Seats')

class session(models.Model):
     _name = 'cine.session'
     _inherits = {'pos.session' : 'pos_session_id'}
     pos_session_id = fields.Many2one('pos.session')
     tpv = fields.Many2one(related="pos_session_id.config_id", readonly=True)
     name = fields.Char(compute='_get_day',store=True)
     theater = fields.Many2one('cine.theater',string='Theater',ondelete='set null')
     cinema = fields.Many2one('cine.cinema',store=False,string='Select a Cinema',help="Select a Cinema to filter the theaters")
     cinema_aux = fields.Many2one('cine.cinema',related='theater.cinema',string='Cinema',readonly=True,store=True)
     hour = fields.Datetime('Hour')
     day = fields.Date(compute='_get_day',store=True,string='Day')
     duration = fields.Float(related='movie.duration',string='Duration')
     movie = fields.Many2one('cine.movie',string='Movie',ondelete='restrict')
     movie_poster = fields.Binary(related='movie.poster',string='Movie poster')
     tickets = fields.One2many('pos.order.line','session', string='Tickets')
     orders = fields.One2many('pos.order',related='pos_session_id.order_ids', string='Orders')
     current_projections = fields.Boolean(compute='_get_current_projections',store=False, string='Projection')
     percent_current_projections = fields.Float(compute='_get_current_projections',store=False, string='% Projection')

     @api.onchange('cinema')
     def _filter_theater(self):
      #print self.cinema
      return { 'domain': {'theater': [('cinema','=',self.cinema.id)]} }     


     @api.depends('theater','hour','movie')
     def _get_day(self):
       for r in self:
         name="aun sin name"
         if r.theater and r.movie and r.hour:
           name=r.theater.name+" / "+r.movie.name+" / "+str(r.hour)
         r.name=name
         if r.hour:
           r.day=r.hour
         r.name=name

     @api.depends('hour')
     def _get_current_projections(self):
      for p in self:
        pro=self.projectantse(p.id)
        p.current_projections=pro
        if pro==True:
         fmt = '%Y-%m-%d %H:%M:%S'
         d1 = datetime.strptime(p.hour, fmt)
         d2 = datetime.strptime(fields.Datetime.now(), fmt)
         print str(d1)+"-----"+str(d2)

         minsDiff = (d2-d1).seconds/60
         print minsDiff
         percent=tools.float_round((minsDiff/(p.movie.duration*60))*100,precision_rounding=0.01)
        else:
         percent=0
        p.percent_current_projections = percent
        

     def projectantse(self,id):
       p = self.env['cine.session'].browse(id);
       if p.hour:
        fin = fields.Datetime.from_string(p.hour)+timedelta(hours=p.movie.duration)
        #print type(fields.Datetime.from_string(p.hour))
        #print type(datetime.now())
        if fields.Datetime.from_string(p.hour) <= datetime.now() and fin >= datetime.now():
       	 return True
        else:
         return False
       else:
        return False
     
class movie(models.Model):
     _name = 'cine.movie'
     name = fields.Char()
     director = fields.Char()
     premiere = fields.Date('Release')
     poster = fields.Binary()
     sessions = fields.One2many('cine.session','movie')
     price = fields.Float(default=7,string='Price') 
     duration = fields.Float('Duration')
     enbillb = fields.Boolean('Billboard') 
     # La manera poc elegant però efectiva de poder buscar en fields computed 
     enbillb2 = fields.Boolean(compute='_get_enbillb',store=False,string='Billboard')

     def _get_enbillb(self):
      for p in self:
       sessionn_posteriors=self.env['cine.session'].search_count([('hour','>',fields.Datetime.now()),('movie','=',p.id)])
       #print sessionn_posteriors.mapped('name'))
       c =  (sessionn_posteriors > 0)
       p.write({'enbillb':c})
       p.enbillb2 = c      

class seat(models.Model):
     _name = 'cine.seat'
     
     name = fields.Char(string="Position", compute='_get_position',store=True)
     row = fields.Integer('Row')
     seat = fields.Integer('Seat')
     theater = fields.Many2one('cine.theater',string='Theater',ondelete='cascade')
     @api.depends('row','seat')
     def _get_position(self):
       for r in self:
         if  r.row and r.seat:
           r.name="Fila: "+str(r.row)+", Butaca: "+str(r.seat)

class ticket(models.Model):
      #_name = 'pos.order.line'
      _inherit = 'pos.order.line'
      name = fields.Char(string="Identification", compute='_get_id')
      seat = fields.Many2one('cine.seat',string='Seat', ondelete='set null')
      session = fields.Many2one('cine.session',string='Session')
      day = fields.Date(related='session.day',string='Dia', store=True) # per al graph
      aux_cinema = fields.Many2one('cine.cinema',store=False,string='Cinema')
      aux_theater = fields.Many2one('cine.theater',store=False,string='Theater')
      theater = fields.Many2one('cine.theater',related='session.theater',store=True,readonly=True,string='Theater')
      cinema = fields.Many2one('cine.cinema',related='session.theater.cinema',store=True,readonly=True,string='Cinema')
      movie = fields.Many2one('cine.movie',related='session.movie',store=True,readonly=True,string='Movie')
      price_graph = fields.Float(related='movie.price', string='recaptacio' ,store=True) # per al graph
      price_unit = fields.Float('Price',compute="_get_price",search='_search_price',inverse='_set_price') 
      state = fields.Selection([
        ('creada', "Created"),
        ('reservada', "Reserved"),
        ('pagada', "Paid"),
      ], default='creada')
      discount = fields.Selection([
        (0, "None"),
        (10, "Carnet Jove"),
        (20, "< 6 years"),
        (30, "Bonus"),
      ], default=0)

      @api.depends('seat','session')
      def _get_id(self):
       for r in self:
         if r.session and r.seat:
          r.name=r.seat.theater.name+" "+r.seat.name+": "+str(r.session.hour)

      @api.depends('movie','discount')
      def _get_price(self):
        for r in self:
          price = r.movie.price
          price = price - (price*r.discount/100)
          r.price_unit = price

      def _search_price(self,operator,value): # De moment aquest search sols és per a ==
       prices = self.search([]).mapped(lambda e: [e.id , e.movie.price - (e.movie.price*e.discount/100)]) # Un bon exemple de mapped en lambda
       print prices
       p = [ num[0] for num in prices if num[1] == value]  # condició if en una aux_list python sense fer un for (list comprehension)
       # també es pot provar en un filter() de python
       print p
       # p és una aux_list de les id que ja compleixen la condició, per tant sols cal fer que la id estiga en la aux_list.
       return [('id','in',p)]

      def _set_price(self):
       self.movie.price = self.price  # Açò és un exemple, però està mal, ja que modifiques el price de la peli en totes les sessions


      @api.constrains('seat','session')
      def _check_repeticions(self):
        for r in self:
          if self.search_count([('seat.id','=',r.seat.id),('session.id','=',r.session.id)]) > 1:
            raise ValidationError("Repetida")
          if r.seat.theater.id != r.session.theater.id:
            raise ValidationError("La seat no és de la theater")

      @api.onchange('aux_cinema')
      def _filter_cinema(self):
        return { 'domain': {'aux_theater': [('cinema','=',self.aux_cinema.id)]} }     
      @api.onchange('aux_theater')
      def _filter_theater(self):
        return { 'domain': {'session': [('theater','=',self.aux_theater.id)]} }     
      @api.onchange('session')
      def _filter_session(self):
       # seats=self.env['cine.seat'].search([('theater','=',self.session.theater.id)])
       # print seats 
       # libres=[]
      #   for i in seats:
      #   tickets=self.search_count([('seat','=',i.id),('session','=',self.session.id)])
      #   if tickets == 0:
      #    libres.append(i.id)
      #  print libres
        libres = (self.session.theater.seats - self.search([('session','=',self.session.id)]).mapped('seat')).ids
        print libres   
        return { 'domain': {'seat': [('id', 'in' , libres)]} } 
    
      @api.multi
      def change_state(self):
       for r in self:
        if r.state == 'creada':
          r.write({'state':'reservada'})
        elif r.state == 'reservada':
          r.write({'state':'pagada'})
        elif r.state == 'pagada':
          r.write({'state':'creada'})
            

class wizSessions(models.TransientModel):
      _name = 'cine.wiz_sessions'
      def _default_cinema(self):
         return self.env['cine.cinema'].browse(self._context.get('active_id')) 
      cinema=fields.Many2one('cine.cinema',default=_default_cinema)
      pos_session_id = fields.Many2one('pos.session')
      tpv=fields.Many2one('pos.config')
      movies=fields.Many2many('cine.movie')
      day=fields.Date() 
      state = fields.Selection([
        ('pelis', "Movie Selection"),
        ('day', "Day Selection"),
      ], default='pelis')
 
      @api.multi
      def action_pelis(self):
        self.state = 'pelis'
        return { "type": "ir.actions.do_nothing", }

      @api.multi
      def action_day(self):
        self.state = 'day'
        return { "type": "ir.actions.do_nothing", }
      
      @api.multi
      def crear(self):
        theaters=self.cinema.theaters.ids
        n_theaters = len(theaters)
        theater=0
        for i in self.movies:
         if theater<n_theaters:
          session=self.day+' 18:00:00'
          for j in range(0,3):
            s=self.env['cine.session'].create({'movie':i.id,'hour':session,'cinema':self.cinema.id,'theater':theaters[theater],'pos_session_id':self.pos_session_id.id})
            session=(datetime.strptime(session, '%Y-%m-%d %H:%M:%S')+timedelta(hours=i.duration)).strftime('%Y-%m-%d %H:%M:%S')
          theater = theater + 1
        return {}


class wizSessions2(models.TransientModel):
      _name = 'cine.wiz_sessions2'
      def _default_cinema(self):
         return self.env['cine.cinema'].browse(self._context.get('active_id')) 
      def _get_hourinici(self):
        return fields.Date.today()+" 18:00:00"       
      cinema=fields.Many2one('cine.cinema',default=_default_cinema)
      theater=fields.Many2one('cine.theater')
      tpv=fields.Many2one('pos.config')
      movie=fields.Many2one('cine.movie')
      hour_inici=fields.Datetime(default=_get_hourinici) 
      sessions=fields.Many2many('cine.session') # Falta afegir com a referència les sessions d'eixe day en eixa theater.
      
      @api.onchange('theater')
      def lista_sessions(self):
        s=self.env['cine.session'].search([('day','=',self.hour_inici)]).ids
        self.sessions = [(6,0,s)] 

      @api.multi
      def crear(self):
        theater=self.theater.id
        peli=self.movie.id
        s=self.env['cine.session'].create({'movie':peli,'hour':self.hour_inici,'cinema':self.cine.id,'theater':theater})
        self.sessions = [(4,s.id)]
        fmt = '%Y-%m-%d %H:%M:%S'
        h = datetime.strptime(self.hour_inici, fmt)+timedelta(hours=+self.movie.duration)
        self.hour_inici = h.strftime(fmt)
        return { "type": "ir.actions.do_nothing", }

class wizseats(models.TransientModel):
      _name = 'cine.wiz_seats'
      def _default_theater(self):
         return self.env['cine.theater'].browse(self._context.get('active_id')) 
      theater=fields.Many2one('cine.theater',default=_default_theater)

      rows=fields.Integer(default=10)
      seats=fields.Integer(default=10)

      @api.multi
      def crear(self):
        theater=self.theater.id
        for i in range(0,self.rows):
         for j in range(0,self.seats):
            s=self.env['cine.seat'].create({'theater':theater,'row':i+1,'seat':j+1})
        return {}

#TODO
# https://erflow.com/questions/9377402/insert-into-many2many-odoo-former-openerp
#https://www.odoocom/cumentation/9.0/reference/views.html#qweb https://www.odoo.com/es_ES/forum/ayuda-1/question/how-to-create-a-new-view-type-24330
