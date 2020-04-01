# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class SolicitudesEstudio(models.Model):
    _name = 'solicitud.estudio'
    _rec_name = "name"

    nota_de_evolucion = fields.Char("Notas", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    paciente = fields.Many2one('pacientes',"Paciente",required=True)
    domicilio = fields.Char(string="Domicilio")
    fecha = fields.Date(string="Fecha: ", default=fields.Datetime.now)
    text_solicitud = fields.Text()
    nombre_completo = fields.Char(string="Nombre",related='paciente.nombre_completo', store=True)

    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True, default='02')

    #Estados
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('solicitud.estudios') or _('New')
        result = super(SolicitudesEstudio, self).create(vals)
        return result

    #Validar
    def validar_estudio(self):
        self.write({'state': 'done'})
        
        return True

#     @api.multi
    @api.onchange('paciente')
    def _set_paciente(self):
        if self.paciente:
           values = {
                  'nombre_completo': self.paciente.nombre_completo,
                  'unidad_medica': self.paciente.unidad_medica,
                  'domicilio': self.paciente.domicilio_actual
           }
           self.update(values)
