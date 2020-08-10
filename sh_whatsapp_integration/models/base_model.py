# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import models, fields, api

class res_partner(models.Model):
    _inherit="res.partner"
    
class res_users(models.Model):
    _inherit="res.users"
    
    sign = fields.Text('Signature')
    
    