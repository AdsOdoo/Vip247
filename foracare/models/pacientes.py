# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import datetime
from datetime import datetime

class ForacarePacientes(models.Model):
    _inherit = 'pacientes'
    
#    @api.model
#    def create(self, vals):
#        if not vals.get('name') or vals['name'] == _('New'):
#            vals['name'] = self.env['ir.sequence'].next_by_code('pacientes') or _('New')
#        return super(ForacarePacientes, self).create(vals)
    
    