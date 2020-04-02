# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, timedelta

import logging
import string
_logger = logging.getLogger(__name__)

class OtrosDocumentos(models.Model):
    _name = 'otros.documentos'
    _rec_name = "name"
    
    otros_documentos = fields.Char("Otros Documentos", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    store_fname = fields.Char(string="Nombre archivo")
    documento = fields.Binary('Documento Adjunto')
    doc_name = fields.Char('Nombre de archivo')
    description = fields.Char('Descripción')
    paciente = fields.Many2one('pacientes',"Paciente",required=True)
    nombre_completo = fields.Char(string="Nombre",related='paciente.nombre_completo', store=True)

    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True)
    fecha = fields.Date("Fecha", default=fields.Datetime.now)

    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('otros.documentos') or _('New')
        result = super(OtrosDocumentos, self).create(vals)
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
