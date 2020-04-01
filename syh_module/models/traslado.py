# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)

class Traslado(models.Model):
    _name = 'referencia.traslado'
    _rec_name = "name"

    traslado = fields.Char("Traslado", default=lambda self: _('New'))
    name = fields.Char("Folio", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    establecimiento_envia = fields.Char(string="Establecimiento Que Envía", required=True)
    establecimiento_receptor = fields.Char(string="Establecimiento Receptor", required=True)
    motivo_de_envio = fields.Char(string="Motivo De Envío", required=True)
    impresion_diagnostica = fields.Char(string="Impresión Diagnóstica", required=True)
    terapeutica_empleada = fields.Char(string="Terapéutica Empleada", required=True)
    adjuntar_archivo = fields.Binary(string="Adjuntar Archivo")
    store_fname = fields.Char(string="Nombre archivo")
    unidad_medica = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True,required=True)

    #Estados
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')



    #Validar
    def validar_estudio(self):
        self.write({'state': 'done'})
        
        return True

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('traslado') or _('New')
        result = super(Traslado, self).create(vals)
        return result