# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class HojaEnfermeria(models.Model):
    _name = 'hoja.enfermeria'
    _rec_name = "name"

    causamuerte = fields.Char("Traslado", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))


    paciente = fields.Many2one('pacientes',"Paciente",required=True)
    fecha_nacimiento = fields.Date(string="Fecha De Nacimiento", required=True,compute='paciente_compute',readonly=False)
    edad = fields.Many2one('edad',string="Edad", required=True, compute='paciente_compute',readonly=False)
    genero = fields.Selection([
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO')
        ],required=True, compute='paciente_compute',readonly=False)
    domicilio_actual = fields.Char(string="Domicilio Actual", required=True, compute='paciente_compute',readonly=False)
    fecha = fields.Date("Fecha",states={'draft': [('readonly', False)]}, default=fields.Datetime.now, required=True)
    unidad_medica = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True,required=True)
#    hora = fields.Char(string="Hora",required=True)
 #   campo_detalles = fields.Text(string="Campo detalles",required=True)

    #CAMPOS HOJA DE ENFERMERÍA
#    impresion_diagnostica = fields.Text(string="Impresión Diagnóstica",required=True)
#    indicaciones_medicas = fields.Text(string="Indicaciones Médicas",required=True)
#    motivo_consulta = fields.Text(string="Motivo De Consulta",required=True)
#    alergias = fields.Selection([
#            ('01', 'SÍ'),
#            ('02', 'NO'),
#            ],required=True)
#    nota_alergia = fields.Text(string="Alergias",required=True)


    #Estados
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')


    @api.depends('paciente')
    def paciente_compute(self):
        self.fecha_nacimiento = self.paciente.fecha_nacimiento
        self.edad = self.paciente.edad
        self.genero = self.paciente.genero
        self.domicilio_actual = self.paciente.domicilio_actual
        self.unidad_medica = self.paciente.unidad_medica
        return

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

    #Validar
    def validar_estudio(self):
        self.write({'state': 'done'})
        
        return True

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hoja.enfermeria') or _('New')
        result = super(HojaEnfermeria, self).create(vals)
        return result