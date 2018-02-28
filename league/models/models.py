# -*- coding: utf-8 -*-

from odoo import models, fields, api

class league(models.Model):
     _name = 'league.league'
     name = fields.Char()
     start_date = fields.Date()
     end_date = fields.Date()
     teams = fields.One2many('league.points','league')
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
     
class points(models.Model):
    _name = 'league.points'
    name = fields.Char(related='team.name', readonly=True)
    league = fields.Many2one('league.league')
    logo = fields.Binary(related='team.logo')
    team = fields.Many2one('league.team')
    points = fields.Integer(compute='_get_points')
    
    @api.depends('team','league')
    def _get_points(self):
      for points in self:
        league = points.league
        team = points.team
        matches = league.matches.filtered(lambda r: r.local.id == team.id or r.visitor.id == team.id)
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
	points = fields.One2many('league.points','team') 
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
    league = fields.Many2one('league.league')
    matches = fields.One2many('league.match','day')
	
class match(models.Model):
    _name = 'league.match'
    name = fields.Char(compute='_get_name')
    @api.depends('local','visitor')
    def _get_name(self):
     for match in self:
       match.name=str(match.local.name)+" vs "+str(match.visitor.name)    
    date = fields.Datetime()
    day = fields.Many2one('league.day')
    league = fields.Many2one(related='day.league', readonly=True)
    local = fields.Many2one('league.team')
    visitor = fields.Many2one('league.team')
    winner = fields.Many2one('league.team', compute='_get_winner')
    local_points = fields.Integer()
    visitor_points = fields.Integer()

    @api.depends('local','visitor','local_points','visitor_points')
    def _get_winner(self):
      for match in self:
       if match.local_points > match.visitor_points:
          match.winner = match.local.id
       elif match.local_points < match.visitor_points:
          match.winner = match.visitor.id
       else: 
          match.winner = False

