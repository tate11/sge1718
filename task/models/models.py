# -*- coding: utf-8 -*-

from odoo import models, fields, api

class task(models.Model):
     _name = 'task.task'

     name = fields.Char(required=True)
     start_date = fields.Datetime()
     done = fields.Boolean()
     student = fields.Many2one('task.student')
     country= fields.Char(related='student.country.currency_id.name')

class student(models.Model):

     _name = 'task.student'
     name = fields.Char()
     tasks = fields.One2many('task.task','student')
     teachers = fields.Many2many('task.teacher')
     tutors = fields.Many2many('task.teacher',relation='rtutors')     
     country= fields.Many2one('res.country')

class teacher(models.Model):

     _name = 'task.teacher'
     name = fields.Char()
     students = fields.Many2many('task.student')
     tutorands = fields.Many2many('task.student',relation='rtutors')
