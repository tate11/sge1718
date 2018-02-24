# -*- coding: utf-8 -*-

from odoo import models, fields, api

class league(models.Model):
     _name = 'league.league'
     name = fields.Char()
     start_date = fields.Date()
     end_date = fields.Date()
     teams = fields.One2many('league.points','league')
     days = fields.One2many('league.day','league')
     
class points(models.Model):
	_name = 'league.points'
	name = fields.Char()
	league = fields.Many2one('league.league')
	team = fields.Many2one('league.team')
	points = fields.Integer()
    
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
	name = fields.Char()
	league = fields.Many2one('league.league')
	matches = fields.One2many('league.match','day')
	
class match(models.Model):
	_name = 'league.match'
	name = fields.Char()
	date = fields.Datetime()
	day = fields.Many2one('league.day')
	
