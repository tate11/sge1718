# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
from datetime import datetime
from datetime import timedelta

class league(models.Model):
     _name = 'league.league'
     name = fields.Char()
     start_date = fields.Date()
     end_date = fields.Date()
     teams = fields.One2many('league.points','league')
     n_teams = fields.Integer(compute='_get_n_teams')
     @api.depends('teams')
     def _get_n_teams(self):
      for league in self:
       league.n_teams = len(league.teams)
     days = fields.One2many('league.day','league')
     classification = fields.Many2many('league.points', compute='_get_classification')     

     @api.depends('teams','days')
     def _get_classification(self):
       for league in self:
         teams = league.teams.sorted(key=lambda r: r.points, reverse=True)
         league.classification = teams.ids 

     matches = fields.Many2many('league.match', compute='_get_matches')
    
     @api.depends('days')
     def _get_matches(self):
       for league in self:
         league.matches = league.days.mapped('matches').ids

     @api.one
     def create_calendar(self):
       self.days.unlink() # Esborra totes les jornades i partits (ondelete="cascade")     

       data = fields.Datetime.from_string(self.start_date)
       teams = self.teams.mapped('team').ids
       print teams
       random.shuffle(teams)
       print teams
       for i in range(1,len(teams)):
        day = self.env['league.day'].create({'sequence':i,'league':self.id})
        day2 = self.env['league.day'].create({'sequence':i+len(teams)-1,'league':self.id})
          
        for j in range(0,len(teams)/2): # Primera volta
           if i%2 == 0:     # alternar en casa o visitant
            team_a = teams[j]
            team_b = teams[len(teams)-1-j]
           else:
            team_b = teams[j]
            team_a = teams[len(teams)-1-j]
           self.env['league.match'].create({
					'day':day.id,
					'local':team_a,
					'visitor':team_b,
					'date':fields.Datetime.to_string(data)
					})
           data = data + timedelta(days=7)
        for j in range(0,len(teams)/2): # Segona volta
           if i%2 == 0:     # alternar en casa o visitant
            team_a = teams[j]
            team_b = teams[len(teams)-1-j]
           else:
            team_b = teams[j]
            team_a = teams[len(teams)-1-j]
           self.env['league.match'].create({
					'day':day2.id,
					'visitor':team_a,
					'local':team_b,
					'date':fields.Datetime.to_string(data)
					})
           data = data + timedelta(days=7)
        aux=[]
        aux.append(teams[0])
        aux.append(teams[len(teams)-1])
        aux.extend(teams[1:len(teams)-1])
        print aux
        teams = aux
        
     @api.one
     def random_score(self):
      for match in self.matches:
          match.write({'local_points':random.randint(0,5),'visitor_points':random.randint(0,5),'played':True}) 

class wizPoints(models.TransientModel):
    _name='league.wiz_points'
    def _default_league(self):
      return self.env['league.league'].browse(self._context.get('active_id'))
    league = fields.Many2one('league.league',default=_default_league)
    teams = fields.Many2many('league.team')
    
    @api.multi
    def assign(self):
     for w in self:
      now_teams = w.league.teams.mapped('team')
      new_teams = w.teams - now_teams     # Evitar equips duplicats
      for i in new_teams:
        self.env['league.points'].create({'league':w.league.id,'team':i.id})
      return {
            'type': 'ir.actions.client',
            'tag': 'reload',
             }
     
class points(models.Model):
    _name = 'league.points'
    name = fields.Char(related='team.name', readonly=True)
    league = fields.Many2one('league.league', ondelete="cascade")
    logo = fields.Binary(related='team.logo')
    team = fields.Many2one('league.team', ondelete="cascade")
    points = fields.Integer(compute='_get_points')
    
    @api.depends('team','league')
    def _get_points(self):
      for points in self:
        league = points.league
        team = points.team
        matches = league.matches.filtered(lambda r: (r.local.id == team.id or r.visitor.id == team.id) and r.played == True)
        #print matches.mapped('name')
        p = 0 
        for m in matches:
         if m.winner.id == False:
            p = p + 1
         elif m.winner.id == team.id:
            p = p + 3 
        points.points = p  

        
    
class team(models.Model):
	_name = 'league.team'
	name = fields.Char()
	logo = fields.Binary()
	points = fields.One2many('league.points','team', readonly=True)
	players = fields.One2many('league.player','team')
	
class player(models.Model):
	_name = 'league.player'
	name = fields.Char()
	photo = fields.Binary()
	team = fields.Many2one('league.team')
	
class day(models.Model):
    _name = 'league.day'
    name = fields.Char(compute='_get_name')
    @api.depends('sequence','league')
    def _get_name(self):
     for day in self:
       day.name=str(day.sequence)+"-"+str(day.league.name)
    sequence = fields.Integer()
    league = fields.Many2one('league.league',ondelete='cascade')
    matches = fields.One2many('league.match','day')
	
class match(models.Model):
    _name = 'league.match'
    name = fields.Char(compute='_get_name')
    @api.depends('local','visitor')
    def _get_name(self):
     for match in self:
       #match.name=u''+str(match.local.name)+" vs "+str(match.visitor.name)    
       match.name=u''.join((match.local.name,' vs ',match.visitor.name)).encode('utf-8')    
    date = fields.Datetime()
    day = fields.Many2one('league.day',ondelete='cascade')
    league = fields.Many2one(related='day.league', readonly=True)
    local = fields.Many2one('league.team')
    visitor = fields.Many2one('league.team')
    winner = fields.Many2one('league.team', compute='_get_winner')
    local_points = fields.Integer()
    visitor_points = fields.Integer()
    played = fields.Boolean(default=False)

    @api.depends('local','visitor','local_points','visitor_points')
    def _get_winner(self):
      for match in self:
       if match.local_points > match.visitor_points:
          match.winner = match.local.id
       elif match.local_points < match.visitor_points:
          match.winner = match.visitor.id
       else: 
          match.winner = False

