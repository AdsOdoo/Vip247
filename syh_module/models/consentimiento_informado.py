# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
import string
from datetime import datetime

_logger = logging.getLogger(__name__)

class ConsentimientoInformado(models.Model):
    _name = 'consentimiento.informado'
    _rec_name = "name"
    
    consentimiento_informado = fields.Char("Consentimiento", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True, default='02')  

    paciente = fields.Many2one('pacientes',"Paciente", required=True)
    nombre_completo = fields.Char(string="Nombre",related='paciente.nombre_completo', store=True)

    fecha = fields.Date("Fecha", required=True, default=fields.Datetime.now)
    lugar = fields.Char(string="Lugar")
    indicaciones_emergencia = fields.Text(string="Indicaciones En Caso De Emergencia")
    tecnico_somnox = fields.Char(string="Técnico")

    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')
	
    #Estados1
    tipo_consentimiento_syh = fields.Selection([
            ('consentimiento', 'Consentimiento Informado'),
            ('consentimiento_rcp', 'Consentimiento Informado RCP')
            ])
    #Estados2
    tipo_consentimiento_somnox = fields.Selection([
            ('consentimiento', 'Consentimiento Informado'),
            ])

    #BOOLEANS OF CONSENTIMIENTO INFORMADO SYH

    no_acepto_ci = fields.Boolean(string="No acepto el procedimiento, bajo mi responsabilidad")

    si_acepto_ci = fields.Boolean(string="Acepto procedimiento")

    bool_paciente_ci = fields.Boolean(string="Paciente")

    bool_familiar_responsable_ci = fields.Boolean(string="Familiar responsable")

    bool_cuidador_ci = fields.Boolean(string="Cuidador")

    bool_representante_legal_ci = fields.Boolean(string="Representante legal")

    #BOOLEANS OF CONSENTIMIENTO INFORMADO RCP

    no_acepto_rcp = fields.Boolean(string="No acepto el procedimiento de RCP, bajo mi responsabilidad")

    si_acepto_rcp = fields.Boolean(string="Acepto procedimiento RCP")

    bool_paciente_rcp = fields.Boolean(string="Paciente")

    bool_familiar_responsable_rcp = fields.Boolean(string="Familiar responsable")

    bool_cuidador_rcp = fields.Boolean(string="Cuidador")

    bool_representante_legal_rcp = fields.Boolean(string="Representante legal")

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('consentimiento.informado') or _('New')
        result = super(ConsentimientoInformado, self).create(vals)
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
                  'nombre_completo': self.paciente.nombre_completo,
                  'unidad_medica': self.paciente.unidad_medica
                  }
           self.update(values)
