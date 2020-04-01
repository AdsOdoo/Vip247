# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
_logger = logging.getLogger(__name__)

class Pacientes(models.Model):
    _name = 'pacientes'
    _rec_name = "nombre_completo"

    expediente_clinico = fields.Char("Contratos", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    #PARTE SUPERIOR
    #name = fields.Char("Name", default=lambda self: _('New')) 
    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ],required=True)

    apellido_paterno = fields.Char(string="Apellido Paterno", required=True)
    apellido_materno = fields.Char(string="Apellido Materno", required=True)
    nombres = fields.Char(string="Nombre (s)",required=True)
    nombre_completo =  fields.Char(string="Nombre completo", store=True)
    genero = fields.Selection([
        ('M', 'MASCULINO'),
        ('F', 'FEMENINO')
        ])
    edad = fields.Many2one('edad',string="Edad", required=True)
    dias = fields.Boolean(string="Activo", default=False)
    nota_dias = fields.Char(string=" ")
    meses = fields.Boolean(string="Activo", default=False)
    nota_meses = fields.Char(string=" ")
    lugar_origen = fields.Char(string="Lugar De Origen")
    lugar_residencia = fields.Char(string="Lugar De Residencia", required=True)
    fecha_nacimiento = fields.Date(string="Fecha De Nacimiento", required=True)
    estado_civil = fields.Selection([
        ('01', 'SOLTERO'),
        ('02', 'CASADO'),
        ('03', 'DIVORCIADO'),
        ('04', 'UNIÓN LIBRE'),
        ('05', 'VÍUDO'),
        ])
    ocupacion_actual = fields.Char(string="Ocupación Actual")
    escolaridad = fields.Selection([
        ('01', 'NULO'),
        ('02', 'PRE-ESCOLAR'),
        ('03', 'PRIMARIA'),
        ('04', 'SECUNDARIA'),
        ('05', 'BACHILLERATO'),
        ('06', 'LICENCIATURA'),
        ('07', 'MAESTRÍA'),
        ('08', 'DOCTORADO')
        ])
    religion = fields.Selection([
        ('01', 'CATÓLICA'),
        ('02', 'CRISTIANA'),
        ('03', 'JUDÍA'),
        ('04', 'PROTESTANTE'),
        ('05', 'NINGUNA'),
        ('06', 'OTROS')
        ])
    nota_religion = fields.Char(string=" ")
    grupo_etnico = fields.Selection([
        ('01', 'HISPANO'),
        ('02', 'CAUCÁSICO'),
        ('03', 'ASIÁTICO'),
        ('04', 'AFRICANO'),
        ('05', 'OTRO'),
        ])
    nota_grupo_etnico = fields.Text(string=" ")
    domicilio_actual = fields.Char(string="Domicilio Actual", required=True)
    familiar_responsable = fields.Char(string="Familiar Responsable", required=True)
    parentesco = fields.Selection([
        ('01', 'PADRE'),
        ('02', 'MADRE'),
        ('03', 'ABUELOS'),
        ('04', 'TÍOS'),
        ('05', 'PRIMOS'),
        ('06', 'CÓNYUGE'),
        ('07', 'OTROS')
        ],required=True)
    nota_parentesco = fields.Char(string=" ")
    tipo_interrogatorio= fields.Selection([
        ('DI', 'DIRECTO'),
        ('IN', 'INDIRECTO'),
        ('MI', 'MIXTO'),
        ])
    telefono= fields.Char(string="Teléfono", required=True)
    correo_electronico= fields.Char(string="Correo Electrónico")
    
    expediente_clinico_count = fields.Integer('Count Expediente clinico', compute='_compute_expediente_clinico')
    expediente_clinico_ids = fields.One2many('expediente.clinico', 'paciente', 'Expendiente Clinico')
    
    notas_de_evolucion_count = fields.Integer('Count Notas de evolucion', compute='_compute_notas_de_evolucion')
    notas_de_evolucion_ids = fields.One2many('notas.evolucion', 'paciente', 'Notas de evolucion')
	
    citas_count = fields.Integer('Conteo de Citas', compute='_compute_citas')
    citas_ids = fields.One2many('citas.salud', 'paciente', 'Citas')

    recetas_count = fields.Integer('Conteo de Recetas', compute='_compute_recetas')
    recetas_ids = fields.One2many('recetas', 'paciente', 'Recetas')

    estudios_count = fields.Integer('Conteo de Solicitudes De Estudio', compute='_compute_estudios')
    estudios_ids = fields.One2many('solicitud.estudio', 'paciente', 'Solicitudes De Estudio')

    documentos_count = fields.Integer('Conteo de Solicitudes De Otros Documentos', compute='_compute_documentos')
    documentos_ids = fields.One2many('otros.documentos', 'paciente', 'Otros Documentos')

    interconsulta_count = fields.Integer('Conteo de Solicitudes De Interconsulta', compute='_compute_interconsulta')
    interconsulta_ids = fields.One2many('solicitud.interconsulta', 'paciente', 'Interconsulta')

    consentimiento_count = fields.Integer('Conteo de Solicitudes De Consentimientos Informados', compute='_compute_consentimientos')
    consentimiento_ids = fields.One2many('consentimiento.informado', 'paciente', 'Consentimientos Informados')

    traslado_count = fields.Integer('Conteo de Notas de Referencia Traslado', compute='_compute_traslados')
#    traslado_ids = fields.One2many('referencia.traslado', 'paciente', 'Traslado')

    enfermeria_count = fields.Integer('Conteo de Hoja de Enfermeria', compute='_compute_enfermeria')
    enfermeria_ids = fields.One2many('hoja.enfermeria', 'paciente', 'Hoja de Enfermeria')

    muerte_count = fields.Integer('Conteo de Reporte de Causa Muerte', compute='_compute_muerte')
    muerte_ids = fields.One2many('causamuerte', 'paciente', 'Reporte De Causa Muerte')

    defuncion_count = fields.Integer('Conteo de notas de defuncion', compute='_compute_defuncion')
    defuncion_ids = fields.One2many('notadefuncion', 'paciente', 'Notas de Defunción')

    partner_id = fields.Many2one('res.partner',"Cliente De Odoo")

#     @api.multi
    def _compute_expediente_clinico(self):
        for pacient in self:
            pacient.expediente_clinico_count = len(pacient.expediente_clinico_ids)

#     @api.multi
    def _compute_notas_de_evolucion(self):
        for pacient in self:
            pacient.notas_de_evolucion_count = len(pacient.notas_de_evolucion_ids)

#     @api.multi
    def _compute_citas(self):
        for pacient in self:
            pacient.citas_count = len(pacient.citas_ids)

#     @api.multi
    def _compute_recetas(self):
        for pacient in self:
            pacient.recetas_count = len(pacient.recetas_ids)

#     @api.multi
    def _compute_estudios(self):
        for pacient in self:
            pacient.estudios_count = len(pacient.estudios_ids)

#     @api.multi
    def _compute_documentos(self):
        for pacient in self:
            pacient.documentos_count = len(pacient.documentos_ids)

#     @api.multi
    def _compute_interconsulta(self):
        for pacient in self:
            pacient.interconsulta_count = len(pacient.interconsulta_ids)

#     @api.multi
    def _compute_consentimientos(self):
        for pacient in self:
            pacient.consentimiento_count = len(pacient.consentimiento_ids)

#     @api.multi
    def _compute_enfermeria(self):
        for pacient in self:
            pacient.enfermeria_count = len(pacient.enfermeria_ids)

#     @api.multi
    def _compute_muerte(self):
        for pacient in self:
            pacient.muerte_count = len(pacient.muerte_ids)

#     @api.multi
    def _compute_defuncion(self):
        for pacient in self:
            pacient.defuncion_count = len(pacient.defuncion_ids)

#    @api.multi
#    def _compute_traslados(self):
#        for pacient in self:
#            pacient.traslado_count = len(pacient.traslado_ids)

#     @api.multi
    def action_view_expediente_clinico(self):
        expediente_clinicos = self.mapped('expediente_clinico_ids')
        action = self.env.ref('syh_module.action_expediente_clinico_tree').read()[0]
        if len(expediente_clinicos) > 1:
            action['domain'] = [('id', 'in', expediente_clinicos.ids)]
        elif len(expediente_clinicos) == 1:
            action['views'] = [(self.env.ref('syh_module.view_expediente_clinico_form').id, 'form')]
            action['res_id'] = expediente_clinicos.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_notas_de_evolucion(self):
        notas_de_evolucions = self.mapped('notas_de_evolucion_ids')
        action = self.env.ref('syh_module.action_notas_de_evolucion_tree').read()[0]
        if len(notas_de_evolucions) > 1:
            action['domain'] = [('id', 'in', notas_de_evolucions.ids)]
        elif len(notas_de_evolucions) == 1:
            action['views'] = [(self.env.ref('syh_module.view_notas_de_evolucion_form').id, 'form')]
            action['res_id'] = notas_de_evolucions.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_interconsultas(self):
        interconsultas = self.mapped('interconsultas_ids')
        action = self.env.ref('syh_module.action_inteconsultas_tree').read()[0]
        if len(interconsultas) > 1:
            action['domain'] = [('id', 'in', interconsultas.ids)]
        elif len(interconsultas) == 1:
            action['views'] = [(self.env.ref('syh_module.view_interconsulta_form').id, 'form')]
            action['res_id'] = interconsultas.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_citas(self):
        citas = self.mapped('citas_ids')
        action = self.env.ref('syh_module.action_citas_tree').read()[0]
        if len(citas) > 1:
            action['domain'] = [('id', 'in', citas.ids)]
        elif len(citas) == 1:
            action['views'] = [(self.env.ref('syh_module.view_citas_form').id, 'form')]
            action['res_id'] = citas.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_recetas(self):
        recetas = self.mapped('recetas_ids')
        action = self.env.ref('syh_module.action_recetas_tree').read()[0]
        if len(recetas) > 1:
            action['domain'] = [('id', 'in', recetas.ids)]
        elif len(recetas) == 1:
            action['views'] = [(self.env.ref('syh_module.view_recetas_form').id, 'form')]
            action['res_id'] = recetas.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_estudios(self):
        citas = self.mapped('estudios_ids')
        action = self.env.ref('syh_module.action_solicitud_estudio_tree').read()[0]
        if len(citas) > 1:
            action['domain'] = [('id', 'in', citas.ids)]
        elif len(citas) == 1:
            action['views'] = [(self.env.ref('syh_module.view_solicitud_estudio_form').id, 'form')]
            action['res_id'] = citas.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_documentos(self):
        docs = self.mapped('documentos_ids')
        action = self.env.ref('syh_module.action_documentos_tree').read()[0]
        if len(docs) > 1:
            action['domain'] = [('id', 'in', docs.ids)]
        elif len(docs) == 1:
            action['views'] = [(self.env.ref('syh_module.view_documentos_form').id, 'form')]
            action['res_id'] = docs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_interconsulta(self):
        docs = self.mapped('documentos_ids')
        action = self.env.ref('syh_module.action_solicitud_interconsulta_tree').read()[0]
        if len(docs) > 1:
            action['domain'] = [('id', 'in', docs.ids)]
        elif len(docs) == 1:
            action['views'] = [(self.env.ref('syh_module.view_solicitud_interconsulta_form').id, 'form')]
            action['res_id'] = docs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_consentimientos(self):
        docs = self.mapped('documentos_ids')
        action = self.env.ref('syh_module.action_consentimientos_tree').read()[0]
        if len(docs) > 1:
            action['domain'] = [('id', 'in', docs.ids)]
        elif len(docs) == 1:
            action['views'] = [(self.env.ref('syh_module.view_consentimiento_form').id, 'form')]
            action['res_id'] = docs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_enfermeria(self):
        docs = self.mapped('enfermeria_ids')
        action = self.env.ref('syh_module.action_hoja_enfermeria_tree').read()[0]
        if len(docs) > 1:
            action['domain'] = [('id', 'in', docs.ids)]
        elif len(docs) == 1:
            action['views'] = [(self.env.ref('syh_module.view_hoja_enfermeria_form').id, 'form')]
            action['res_id'] = docs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_muerte(self):
        docs = self.mapped('muerte_ids')
        action = self.env.ref('syh_module.view_solicitud_causamuerte_form').read()[0]
        if len(docs) > 1:
            action['domain'] = [('id', 'in', docs.ids)]
        elif len(docs) == 1:
            action['views'] = [(self.env.ref('syh_module.action_solicitud_causamuerte_tree').id, 'form')]
            action['res_id'] = docs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#     @api.multi
    def action_view_defuncion(self):
        docs = self.mapped('defuncion_ids')
        action = self.env.ref('syh_module.action_solicitud_notadefuncion_tree').read()[0]
        if len(docs) > 1:
            action['domain'] = [('id', 'in', docs.ids)]
        elif len(docs) == 1:
            action['views'] = [(self.env.ref('syh_module.view_solicitud_notadefuncion_form').id, 'form')]
            action['res_id'] = docs.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

#    @api.multi
#    def action_view_traslado(self):
#        citas = self.mapped('traslado_ids')
#        action = self.env.ref('syh_module.action_solicitud_traslado_tree').read()[0]
#        if len(citas) > 1:
#            action['domain'] = [('id', 'in', citas.ids)]
#        elif len(citas) == 1:
#            action['views'] = [(self.env.ref('syh_module.view_solicitud_traslado_form').id, 'form')]
#            action['res_id'] = citas.ids[0]
#        else:
#            action = {'type': 'ir.actions.act_window_close'}
#        return action

    #Funciones
    
    #EDAD DEL PACIENTE
#     @api.multi
    @api.onchange('edad')
    def _otros_edad(self):
        for elementos in self.edad:
            if elementos.codigo_edad == '12' or elementos.codigo_edad == '11' or elementos.codigo_edad == '10' or elementos.codigo_edad == '9' or elementos.codigo_edad == '8' or elementos.codigo_edad == '7' or elementos.codigo_edad == '6' or elementos.codigo_edad == '5' or elementos.codigo_edad == '4' or elementos.codigo_edad == '3' or elementos.codigo_edad == '2' or elementos.codigo_edad == '1' or elementos.codigo_edad == '0':
                self.dias = True
                self.meses =True
                break
            else:
                self.dias = False
                self.meses =False

    #nombre completo
#     @api.multi
    @api.onchange('apellido_paterno', 'apellido_materno', 'nombres')
    def _nombre_completo(self):
        nombre_completo = ''
        if self.apellido_materno and self.nombres:
            nombre_completo = self.apellido_materno + ', ' + self.nombres
        if self.apellido_paterno and self.nombres:
            nombre_completo = self.apellido_paterno + ' ' + self.nombres
        if self.apellido_paterno and self.apellido_materno and self.nombres:
            nombre_completo = self.apellido_paterno + ' ' + self.apellido_materno + ' ' + self.nombres
        values = {
                'nombre_completo': nombre_completo
                }
        self.update(values)
        _logger.info('nombre_ %s', nombre_completo)
        
        
    def save_paciente_paciente(self):
         
        
        return True 
