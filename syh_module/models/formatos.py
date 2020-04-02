# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, timedelta

import logging
import string
_logger = logging.getLogger(__name__)

class VariosFormatos(models.Model):
    _name = 'varios.formatos'
    _rec_name = "name"
    
    formatos = fields.Char("Formatos", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    archivos_adjuntos_ids = fields.One2many('tabla.formatos', 'doc_id', 'Adjuntos')
    descripcion = fields.Char('Tipo de formatos')

    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('varios.formatos') or _('New')
        result = super(VariosFormatos, self).create(vals)
        return result

    #Validar
    def validar_nota(self):
        self.write({'state': 'done'})
        return True

class TablaFormatos(models.Model):
    _name = "tabla.formatos"
	
    documento = fields.Binary('Documento Adjunto')
    doc_name = fields.Char('Nombre de archivo')
    description = fields.Char('Descripción')
    doc_id = fields.Many2one('varios.formatos', 'Adjuntos')
