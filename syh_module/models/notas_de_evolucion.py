# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
import string
from datetime import datetime, timedelta
from odoo import tools
import pytz
_logger = logging.getLogger(__name__)

class NotasDeEvolucion(models.Model):
    _name = 'notas.evolucion'
    _rec_name = "nombres"

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

    nota_de_evolucion = fields.Char("Notas", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    unidad_medica = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ])  

    paciente = fields.Many2one('pacientes',"Paciente",required=True)

    #SIGNOS VITALES
    ta = fields.Char(string="T/A")
    temperatura = fields.Char(string="Temperatura °C")
    fc = fields.Char(string="FC")
    fr = fields.Char(string="FR")
    sp02 = fields.Char(string="Sp02")

    peso = fields.Char(string="Peso (kg)")
    talla = fields.Char(string="Talla (cm)")

    fecha = fields.Date("Fecha", default=fields.Datetime.now)
    hora = fields.Char(string="Hora", default=_get_hora) # default=(fields.Datetime.now - timedelta(hours=6)).strftime('%H:%M')
    nota_evolucion = fields.Text(string="Nota de evolución")

    #CAMPOS DE REPORTE
    subjetivo_text = fields.Text(string="Subjetivo")
    objetivo_text = fields.Text(string="Objetivo")
    analisis_text = fields.Text(string="Análisis")
    plan_text = fields.Text(string="Plan")
    cita_text = fields.Text(string="Cita De Seguimiento")


    apellido_paterno = fields.Char(string="Apellido Paterno",related='paciente.apellido_paterno', store=True)
    apellido_materno = fields.Char(string="Apellido Materno",related='paciente.apellido_materno', store=True)
    nombres = fields.Char(string="Nombre (s)",related='paciente.nombres', store=True)
    edad = fields.Many2one('edad',string="Edad",related='paciente.edad', store=True)

    #Campos exta para el reporte
    imc = fields.Char(string="IMC")
    circunferencia_cintura = fields.Integer(string="Cincunferencia De Cintura (cm)")
    circunferencia_cuello = fields.Integer(string="Cincunferencia De Cuello (cm)")
    glucemia = fields.Char(string="Glucemia")

    #Estados
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('notas.de.evolucion') or _('New')
        result = super(NotasDeEvolucion, self).create(vals)
        return result

    
    #Validar
    def validar_nota(self):
        self.write({'state': 'done'})
        
        return True

#     @api.multi
    @api.onchange('paciente')
    def _set_paciente(self):
        if self.paciente:
            values = {
                  'nombres': self.paciente.nombres,
                  'apellido_paterno': self.paciente.apellido_paterno,
                  'apellido_materno': self.paciente.apellido_materno,
                  'edad': self.paciente.edad,
                  'unidad_medica': self.paciente.unidad_medica
                  }
            self.update(values)

    def cita_deseguimiento_citas(self):
        return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'citas.salud',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context':{'expediente_clinico': self.id,'is_new_popup':True,'default_paciente':self.paciente.id}
                }