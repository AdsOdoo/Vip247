# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
#from tzlocal import get_localzone
from datetime import datetime
from odoo.exceptions import UserError


class RetardoNomina(models.Model):
    _name = 'retardo.nomina'
    _description = 'RetardoNomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha = fields.Date('Fecha')
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='State', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('retardo.nomina') or _('New')
        result = super(RetardoNomina, self).create(vals)
        return result

    
    def action_validar(self):
        self.write({'state':'done'})
        return

    
    def action_cancelar(self):
        self.write({'state':'cancel'})

    
    def action_draft(self):
        self.write({'state':'draft'})

    
    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")