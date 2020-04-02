# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
import time
from odoo import tools
import pytz

class Interconsulta(models.Model):
    _name = 'solicitud.interconsulta'
    _rec_name = "name"

    @api.model
    def _get_hora(self):
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        timezone = self._context.get('tz')
        if not timezone:
           timezone = self.env.user.partner_id.tz or 'UTC'
        timezone = tools.ustr(timezone).encode('utf-8')

        local = pytz.timezone(timezone)
        naive_from = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
        return local_dt_from.strftime ('%H:%M')

    interconsulta = fields.Char("Interconsulta", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    paciente = fields.Many2one('pacientes',"Paciente",required=True)
    domicilio = fields.Char(string="Domicilio")
    fecha = fields.Date("Fecha", default=fields.Datetime.now)
    time = fields.Char(string="Hora", default=_get_hora)
    text_solicitud = fields.Text(string="Servicio Que Solicita La Interconsulta",required=True)
    text_motivo = fields.Text(string="Motivo De La Interconsulta",required=True)
    text_servicio = fields.Text(string="Servicio Al Que Se Le Solicita La Interconsulta",required=True)
    medico_solicitante = fields.Char(string="Médico Solicitante",required=True)
    medico_receptor = fields.Char(string="Médico Que Recibe La Solicitud",required=True)
    fecha_recibido = fields.Date(string="Fecha de recibido")
    time_recibido = fields.Char(string="Hora de recibido")
    diagnostico = fields.Text(string="Diagnóstico", required=True)
    edad = fields.Many2one('edad',string="Edad")

    nombre_completo = fields.Char(string="Nombre",related='paciente.nombre_completo', store=True)

    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True, default='02',required=True)

    #Estados
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('solicitud.interconsulta') or _('New')
        result = super(Interconsulta, self).create(vals)
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
                  'domicilio': self.paciente.domicilio_actual,
                  'edad': self.paciente.edad,
           }
           self.update(values)
