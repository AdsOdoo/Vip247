# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Cie10(models.Model):
    _name = 'catalogos.cie10'
    _rec_name = "descripcion"

    codigo = fields.Char(string='Código')
    descripcion = fields.Char(string='Descripción')

class tipo_alergias(models.Model):
    _name = 'tipo.alergias'
    _rec_name = 'codigo_al'

    codigo_al = fields.Char(string="Código")
    descripcion_al = fields.Char(string="Descripción")

class heredo_familiar(models.Model):
    _name = 'heredo.familiar'
    _rec_name = 'codigo'

    codigo = fields.Char(string='Código')
    descripcion = fields.Char(string='Descripción')

class infecto_contagiosas(models.Model):
    _name = 'infecto.contagiosas'
    _rec_name = 'codigo_ic'

    codigo_ic = fields.Char(string='Código')
    descripcion_ic = fields.Char(string='Descripción')

class cronico_degenerativas(models.Model):
    _name = 'cronico.degenerativas'
    _rec_name = 'codigo_cd'

    codigo_cd = fields.Char(string='Código')
    descripcion_cd = fields.Char(string='Descripción')

class estudios_diagnosticos(models.Model):
    _name = 'estudios.diagnosticos'
    _rec_name = 'codigo_ed'

    codigo_ed = fields.Char(string='Código')
    descripcion_ed = fields.Char(string='Descripción')

class edad(models.Model):
    _name = 'edad'
    _rec_name = 'codigo_edad'

    codigo_edad = fields.Char(string='Código')
    descripcion_edad = fields.Char(string='Descripción')