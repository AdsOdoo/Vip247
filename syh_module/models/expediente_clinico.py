# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import logging
import string
from datetime import datetime, timedelta
import time
from odoo import tools
import pytz
_logger = logging.getLogger(__name__)

class ExpendienteClinico(models.Model):
    _name = 'expediente.clinico'

    @api.model
    def _get_hora(self):
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        timezone = self._context.get('tz')
        if not timezone:
           timezone = self.env.user.partner_id.tz or 'UTC'
#         timezone = tools.ustr(timezone).encode('utf-8')

        local = pytz.timezone(timezone)
        naive_from = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
        return local_dt_from.strftime ('%H:%M')

    expediente_clinico = fields.Char("Contratos", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    #PARTE SUPERIOR
    # name = fields.Char("Name", default=lambda self: _('New')) 
    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ])
    #numero_expediente = fields.Integer(string="Número de expediente")
    partner_id = fields.Many2one('res.partner',"Cliente / Paciente", readonly=True,required=False, states={'draft': [('readonly', False)]})
    fecha = fields.Date("Fecha",states={'draft': [('readonly', False)]}, default=fields.Datetime.now)
    time = fields.Char(string="Hora", default=_get_hora)
    observaciones = fields.Text("Observaciones")
    paciente = fields.Many2one('pacientes',"Paciente",required=True)
    nombre_completo = fields.Char(string="Nombre",related='paciente.nombre_completo', store=True)
    edad = fields.Many2one('edad',string="Edad", store=True)

    #ANTECEDENTES HEREDO-FAMILIARES
    
#    paciente_id = fields.Many2one('pacientes',string="Paciente")
    padre = fields.Many2many('heredo.familiar', 'id_padre', 'codigo_padre')
    nota_padre = fields.Char(string=" ")
    padre_otro = fields.Boolean(string="Activo", default=False)
    madre = fields.Many2many('heredo.familiar','id_madre','codigo_madre')
    nota_madre = fields.Char(string=" ")
    madre_otro = fields.Boolean(string="Activo", default=False)
    hermanos = fields.Many2many('heredo.familiar', 'id_hermanos', 'codigo_hermanos') 
    nota_hermanos = fields.Char(string=" ")
    hermanos_otro = fields.Boolean(string="Activo", default=False)
    abuelos_paternos = fields.Many2many('heredo.familiar', 'id_abuelos_paternos', 'codigo_abuelos_paternos')
    nota_abuelos_paternos = fields.Char(string=" ")
    abuelos_paternos_otro = fields.Boolean(string="Activo", default=False)
    abuelos_maternos = fields.Many2many('heredo.familiar', 'id_abuelos_maternos','codigo_abuelos_maternos')
    nota_abuelos_maternos = fields.Char(string=" ")
    abuelos_maternos_otro = fields.Boolean(string="Activo", default=False)
    tios_paternos = fields.Many2many('heredo.familiar', 'id_tios_paternos','codigo_tios_paternos')
    nota_tios_paternos = fields.Char(string=" ")
    tios_paternos_otro = fields.Boolean(string="Activo", default=False)
    tios_maternos = fields.Many2many('heredo.familiar', 'id_tios_maternos', 'codigo_tios_maternos')
    nota_tios_maternos = fields.Char(string=" ")
    tios_maternos_otro = fields.Boolean(string="Activo", default=False)
    primos_paternos = fields.Many2many('heredo.familiar', 'id_primos_paternos', 'codigo_primos_paternos')
    nota_primos_paternos = fields.Char(string=" ")
    primos_paternos_otro = fields.Boolean(string="Activo", default=False)
    primos_maternos = fields.Many2many('heredo.familiar', 'id_primos_maternos', 'codigo_primos_maternos') 
    nota_primos_maternos = fields.Char(string=" ")
    primos_maternos_otro = fields.Boolean(string="Activo", default=False)

    #ANTECEDENTES NO PATOLOGICOS
    vivienda = fields.Selection([
        ('01', 'ADECUADO'),
        ('02', 'NO ADECUADO'),
        ])
    nota_vivienda = fields.Text(string=" ")
    higiene = fields.Selection([
        ('01', 'ADECUADO'),
        ('02', 'NO ADECUADO'),
        ])
    nota_higiene = fields.Text(string=" ")
    dieta = fields.Selection([
        ('01', 'ADECUADO'),
        ('02', 'NO ADECUADO'),
        ])
    nota_dieta = fields.Text(string=" ")
    zoonosis = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NO'),
        ])
    nota_zoonosis = fields.Text(string=" ")
    tabaquismo = fields.Selection([
        ('01', 'NEGADO'),
        ('02', 'OCASIONAL'),
        ('03', 'RECURRENTE'),
        ('04', 'OTRO')
        ])
    nota_tabaquismo = fields.Text(string=" ")
    alcoholismo = fields.Selection([
        ('01', 'NEGADO'),
        ('02', 'OCASIONAL'),
        ('03', 'RECURRENTE'),
        ('04', 'OTRO')
        ])
    nota_alcoholismo = fields.Text(string=" ")
    toxicomanias = fields.Selection([
        ('01', 'NEGADO'),
        ('02', 'OCASIONAL'),
        ('03', 'RECURRENTE'),
        ('04', 'OTRO')
        ])
    nota_toxicomanias = fields.Text(string=" ")

    #ANTECEDENTES PATOLOGICOS (DE PATOS JEJE XD)
    e_infectoconta = fields.Many2many('infecto.contagiosas', string="Enfermedades Infecto-Contagiosas")
    nota_e_infectoconta = fields.Text(string=" ")
    
        #BOOLEANOS INFECTOCONTAGIOSAS#
    bool_varicela = fields.Boolean(string="Activo", default=False)
    bool_rubeola = fields.Boolean(string="Activo", default=False)
    bool_sarampion = fields.Boolean(string="Activo", default=False)
    bool_parotiditis = fields.Boolean(string="Activo", default=False)
    bool_hepatitisa = fields.Boolean(string="Activo", default=False)
    bool_hepatitisb = fields.Boolean(string="Activo", default=False)
    bool_tetanos = fields.Boolean(string="Activo", default=False)
    bool_tb = fields.Boolean(string="Activo", default=False)
    bool_vih = fields.Boolean(string="Activo", default=False)
    

        #NOTAS INFECTOCONTAGIOSAS#
    nota_varicela = fields.Text(string="Nota Varicela")
    nota_rubeola = fields.Text(string="Nota Rubeola")
    nota_sarampion = fields.Text(string="Nota Sarampión")
    nota_parotiditis = fields.Text(string="Nota Parotoditis")
    nota_hepatitisa = fields.Text(string="Nota Hepatitis A")
    nota_hepatitisb = fields.Text(string="Nota Hepatitis B")
    nota_tetanos = fields.Text(string="Nota Tétanos")
    nota_tb = fields.Text(string="Nota TB")
    nota_vih = fields.Text(string="Nota VIH")
    e_infectoconta_otro = fields.Boolean(string="Activo", default=False)


    e_cronicodegen = fields.Many2many('cronico.degenerativas', string="Enfermedades Crónico-Degenerativas")
    nota_e_cronicodegen = fields.Text(string=" ")
    e_cronicodegen_otro = fields.Boolean(string="Activo", default=False)

        #BOOLEANOS CRONICODEGEN#
    bool_dm2 = fields.Boolean(string="Activo", default=False)
    bool_has = fields.Boolean(string="Activo", default=False)
    bool_enfcardio = fields.Boolean(string="Activo", default=False)
    bool_iam = fields.Boolean(string="Activo", default=False)
    bool_erc = fields.Boolean(string="Activo", default=False)
    bool_ca = fields.Boolean(string="Activo", default=False)
    bool_enfrespi = fields.Boolean(string="Activo", default=False)

        #NOTAS CRONICODEGEN#
    nota_dm2 = fields.Text(string="Nota DM2")
    nota_has = fields.Text(string="Nota HAS")
    nota_enfcardio = fields.Text(string="Nota Enf. Cardiovascular")
    nota_iam = fields.Text(string="Nota IAM")
    nota_erc = fields.Text(string="Nota ERC")
    nota_ca = fields.Text(string="Nota CA")
    nota_enfrespi = fields.Text(string="Nota Enr. Respiratoria")

    traumatismos = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    nota_traumatismo = fields.Text(string="Nota Traumatismo")
    #quirurgicos = fields.Char(string="Quirurjicos")
    alergias = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    alergias_m2m = fields.Many2many('tipo.alergias', string=" ")
    bool_alimentos = fields.Boolean(string="Activo", default=False)
    bool_medicamentos = fields.Boolean(string="Activo",default=False)
    bool_otros = fields.Boolean(string="Activo",default=False)

    alergia_alimentos = fields.Text(string="Alergias De Alimentos")
    alergia_medicamentos = fields.Text(string="Alergias De Medicamentos")
    alergia_otros = fields.Text(string="Otras Alergias")
    cirugias = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    nota_cirugias = fields.Text(string="Nota Cirugias")
    hospitalizaciones_prev = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    nota_hospitalizaciones = fields.Text(string="Nota Hospitalizaciones")
    transfusiones = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    nota_transfusiones = fields.Text(string="Nota Cirugias")

    esquema_vacunacion = fields.Selection([
        ('01', 'COMPLETO-PRESENTA CARTILLA'),
        ('02', 'COMPLETO-NO PRESENTA CARTILLA'),
        ('03', 'INCOMPLETO-PRESENTA CARTILLA'),
        ('04', 'INCOMPLETO-NO PRESENTA CARTILLA'),
        ])

    #ANTECEDENTES ANDROLÓGICOS O GINERO OBSTÉTRICOS
    #generales = fields.Char(string="Generales")
    andro_especificos = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    nota_andro = fields.Text(string=" ")
    gineco_obstetricos = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'NEGADO')
        ])
    nota_gineco = fields.Text(string=" ")
    #PADECIMIENTO ACTUAL
    motivo_consulta = fields.Text(required=True)
    padecimiento_actual = fields.Text(required=True)
    cardiovascular = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_cardiovasculas = fields.Text('')

    respiratorio = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_respiratorio = fields.Text('') 

    digestivo = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_digestivo = fields.Text('')

    genito_urinario = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_genito_urinario = fields.Text('') 

    endocrino_metabolismo = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_endocrino_metabolismo = fields.Text('') 

    hematico_linfatico = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_hematico_linfatico = fields.Text('')

    nervioso = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_nervioso = fields.Text('')

    musculo_esqueletico = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_musculo = fields.Text('') 
    piel_tegumentos = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_piel_tegumentos = fields.Text('')

    organos_sentidos = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_organos_sentidos = fields.Text('')

    esfera_psiquica = fields.Selection([
        ('01', 'SÍ'),
        ('02', 'PREGUNTADO Y NEGADO'),
        ])
    nota_esfera_psiquica = fields.Text('')

    #SIGNOS VITALES
    ta = fields.Char(string="T/A",required=True)
    temperatura = fields.Char(string="Temperatura °C",required=True)
    fc = fields.Char(string="FC",required=True)
    fr = fields.Char(string="FR",required=True)
    sp02 = fields.Char(string="Sp02",required=True)

    #EXPLORACIÓN FÍSICA POR APARATOS Y SISTEMAS
    habitus_exterior = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_habitus_exterior = fields.Text('')

    cabeza = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_cabeza = fields.Text('')

    cuello = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_cuello = fields.Text('')

    torax = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_torax = fields.Text('')

    abdomen = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_abdomen = fields.Text('')

    genitales = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_genitales = fields.Text('')

    extremidades = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_extremidades = fields.Text('')

    piel = fields.Selection([
        ('01', 'PERSISTENTES POSITIVOS'),
        ('02', 'PERSISTENTES NEGATIVOS'),
        ])
    nota_piel = fields.Text('')

    #ISATOMETRÍA
    peso = fields.Char(string="Peso (kg)")
    talla = fields.Char(string="Talla (cm)")
    imc = fields.Selection([
        ('01', 'BAJA'),
        ('02', 'NORMAL'),
        ('03', 'SOBREPESO'),
        ('04', 'OBESIDAD I'),
        ('05', 'OBESIDAD II'),
        ('06', 'OBESIDAD III'),
        ('07', 'OBESIDAD MORBIDA'),
        ])
    imc_texto = fields.Char(string="IMC")
    circunferencia_cuello = fields.Char(string="Circunferencia De Cuello (cm)")
    circunferencia_cintura = fields.Char(string="Circunferencia De Cintura (cm)")
    glucemia = fields.Char(string="Glucemia")

    #TIPOS TEXTO
    #lab_gab_otros = fields.Text(string="Laboratorio, Gabinete y Otros")
    diagnostico_presuntivo = fields.Many2many('catalogos.cie10','id_diagnostivo_presuntivo','codigo_diagnostico_presuntivo','descripcion_diagnostico_presuntivo',required=True)
    nota_diagnotivo_presuntivo = fields.Text(string="Otro")
    bool_dp = fields.Boolean(string="Activo", default=False)
    nota_dp = fields.Text(string="Otro Diagnóstico")
    bool_df = fields.Boolean(string="Activo", default=False)
    nota_df = fields.Text(string="Otro Diagnóstico")
    estudios_diagnostico = fields.Many2many('estudios.diagnosticos', string="Estudio (s) Diagnóstico (s)")
    bool_ed = fields.Boolean(string="Activo", default=False)
    nota_ed = fields.Text(string="Otros Estudios")
    nota_estudios_diagnostico = fields.Text(string="Nota Estudios Diagnósticos")
    diagnosticos_definitivos = fields.Many2many('catalogos.cie10', 'id_diagnosticos_definitivos', 'codigo_diagnosticos_definitivos', 'descripcion_diagnostivos_definitivos')
    nota_diagnosticos_definitivos = fields.Text(string="Otros")

    #TRATAMIENTO
    farmacologico = fields.Char(string="Farmacológico",required=True)
    no_farmacologico = fields.Selection([
        ('01', 'NINGUNO'),
        ('02', 'CPAP DE SUEÑO'),
        ('03', 'BiPAP DE SUEÑO'),
        ('04', 'OTROS'),
        ],required=True)
    nota_farmacologico = fields.Text(string=" ")

    #ULTIMOS 2 GROUPS DE ESTE MODELO - PRONOSTICO Y SEGUIMIENTO
    pronostico = fields.Selection([
        ('01', 'RESERVADO A EVOLUCIÓN'),
        ('02', 'RESERVADO PARA LA VIDA Y LA FUNCIÓN'),
        ('03', 'BUENO PARA LA VIDA Y LA FUNCIÓN'),
        ('04', 'MALO PARA LA VIDA Y LA FUNCIÓN'),
        ])
    seguimiento_semanal = fields.Date(string="")
    seguimiento_mensual = fields.Date(string="")
    seguimiento_trimestral = fields.Date(string="")
    seguimiento_semestral = fields.Date(string="")
    seguimiento_anual = fields.Date(string="")
    alta = fields.Date(string=" ")

    #adjuntos
    archivos_adjuntos_ids = fields.One2many('expediente.documentos', 'doc_id', 'Adjuntos')

    #adjuntos
    nota_evolucion_ids = fields.One2many('nota.evolucion', 'doc_id', 'Adjuntos')

    #Estados
    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    #Validar
    def validar_expediente(self):
        self.write({'state': 'done'})
        return True



    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('expediente.clinico') or _('New')
        result = super(ExpendienteClinico, self).create(vals)
        return result


    #APP CUADROS DE TEXTO
#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_varicela(self):
        for elementos in self.e_infectoconta:
           if elementos.codigo_ic == 'VARICELA':
              self.bool_varicela = True
              break
           else:
              self.bool_varicela = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_rubeola(self):
        for elementos in self.e_infectoconta:
            if elementos.codigo_ic == 'RUBEOLA':
                self.bool_rubeola = True
                break
            else:
                self.bool_rubeola = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_sarampion(self):
        for elementos in self.e_infectoconta:
            if elementos.codigo_ic == 'SARAMPIÓN':
                self.bool_sarampion = True
                break
            else:
                self.bool_sarampion = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_parotiditis(self):
        for elementos in self.e_infectoconta:
            if elementos.codigo_ic == 'PAROTIDITIS':
                self.bool_parotiditis = True
                break
            else:
                self.bool_parotiditis = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_hepatitisa(self):
        for elementos in self.e_infectoconta:
           if elementos.codigo_ic == 'HEPATITIS A':
              self.bool_hepatitisa = True
              break
           else:
              self.bool_hepatitisa = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_hepatitisb(self):
        for elementos in self.e_infectoconta:
           if elementos.codigo_ic == 'HEPATITIS B':
              self.bool_hepatitisb = True
              break
           else:
              self.bool_hepatitisb = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_tetanos(self):
        for elementos in self.e_infectoconta:
            if elementos.codigo_ic == 'TÉTANOS':
                self.bool_tetanos = True
                break
            else:
                self.bool_tetanos = False
    
#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_tb(self):
        for elementos in self.e_infectoconta:
            if elementos.codigo_ic == 'TB':
                self.bool_tb = True
                break
            else:
                self.bool_tb = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_vih(self):
        for elementos in self.e_infectoconta:
           if elementos.codigo_ic == 'VIH':
              self.bool_vih = True
              break
           else:
              self.bool_vih = False

#     @api.multi
    @api.onchange('e_infectoconta')
    def _otros_v(self):
        for elementos in self.e_infectoconta:
           if elementos.codigo_ic == 'OTRAS':
              self.e_infectoconta_otro = True
              break
           else:
              self.e_infectoconta_otro = False


    #NOTAS ESTUDIOS
#     @api.multi
    @api.onchange('estudios_diagnostico')
    def _otros_ed(self):
        for elementos in self.estudios_diagnostico:
           if elementos.codigo_ed == 'OTROS':
              self.bool_ed = True
              break
           else:
              self.bool_ed = False

    #NOTAS CRONICODEGEN
#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_dm2(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'DM2':
              self.bool_dm2 = True
              break
           else:
              self.bool_dm2 = False

#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_has(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'HAS':
              self.bool_has = True
              break
           else:
              self.bool_has = False
    
#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_enfcardio(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'ENF. CARDIOVASCULAR':
              self.bool_enfcardio = True
              break
           else:
              self.bool_enfcardio = False

#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_iam(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'IAM':
              self.bool_iam = True
              break
           else:
              self.bool_iam = False
    
#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_erc(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'ERC':
              self.bool_erc = True
              break
           else:
              self.bool_erc = False

#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_ca(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'CA':
              self.bool_ca = True
              break
           else:
              self.bool_ca = False

#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_enfrespi(self):
        for elementos in self.e_cronicodegen:
           if elementos.codigo_cd == 'ENF. RESPIRATORIA':
              self.bool_enfrespi = True
              break
           else:
              self.bool_enfrespi = False
    
    #FUNCION DE DIAGNOSTICO PRESUNTIVO
#     @api.multi
    @api.onchange('diagnostico_presuntivo')
    def _otros_dp(self):
        for elementos in self.diagnostico_presuntivo:
           if elementos.descripcion == 'OTROS':
              self.bool_dp = True
              break
           else:
              self.bool_dp = False

    #FUNCION DE DIAGNOSTICO DEFINITIVO
#     @api.multi
    @api.onchange('diagnosticos_definitivos')
    def _otros_df(self):
        for elementos in self.diagnosticos_definitivos:
           if elementos.descripcion == 'OTROS':
              self.bool_df = True
              break
           else:
              self.bool_df = False


    #FUNCION DE ALERGIAS
#     @api.multi
    @api.onchange('alergias_m2m')
    def _otros_alergias_alimentos(self):
        for elementos in self.alergias_m2m:
           if elementos.codigo_al == 'ALIMENTOS':
              self.bool_alimentos = True
              break
           else:
              self.bool_alimentos = False
    
    #FUNCION DE ALERGIAS
#     @api.multi
    @api.onchange('alergias_m2m')
    def _otros_alergias_medicamentos(self):
        for elementos in self.alergias_m2m:
           if elementos.codigo_al == 'MEDICAMENTOS':
              self.bool_medicamentos = True
              break
           else:
              self.bool_medicamentos = False 
    
    #FUNCION DE ALERGIAS
#     @api.multi
    @api.onchange('alergias_m2m')
    def _otros_alergias_otros(self):
        for elementos in self.alergias_m2m:
           if elementos.codigo_al == 'OTROS':
              self.bool_otros = True
              break
           else:
              self.bool_otros = False

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

#     @api.multi
    @api.onchange('padre')
    def _otros_padre(self):
        for elementos in self.padre:
           if elementos.codigo == 'OTROS':
              self.padre_otro = True
              break
           else:
              self.padre_otro = False

#     @api.multi
    @api.onchange('madre')
    def _otros_madre(self):
        for elementos in self.madre:
           if elementos.codigo == 'OTROS':
              self.madre_otro = True
              break
           else:
              self.madre_otro = False

#     @api.multi
    @api.onchange('hermanos')
    def _otros_hermanos(self):
        for elementos in self.hermanos:
           if elementos.codigo == 'OTROS':
              self.hermanos_otro = True
              break
           else:
              self.hermanos_otro = False

#     @api.multi
    @api.onchange('abuelos_paternos')
    def _otros_abuelos_paternos(self):
        for elementos in self.abuelos_paternos:
           if elementos.codigo == 'OTROS':
              self.abuelos_paternos_otro = True
              break
           else:
              self.abuelos_paternos_otro = False

#     @api.multi
    @api.onchange('abuelos_maternos')
    def _otros_abuelos_maternos(self):
        for elementos in self.abuelos_maternos:
           if elementos.codigo == 'OTROS':
              self.abuelos_maternos_otro = True
              break
           else:
              self.abuelos_maternos_otro = False

#     @api.multi
    @api.onchange('tios_paternos')
    def _otros_tios_paternos(self):
        for elementos in self.tios_paternos:
           if elementos.codigo == 'OTROS':
              self.tios_paternos_otro = True
              break
           else:
              self.tios_paternos_otro = False

#     @api.multi
    @api.onchange('tios_maternos')
    def _otros_tios_maternos(self):
        for elementos in self.tios_maternos:
           if elementos.codigo == 'OTROS':
              self.tios_maternos_otro = True
              break
           else:
              self.tios_maternos_otro = False

#     @api.multi
    @api.onchange('primos_paternos')
    def _otros_primos_paternos(self):
        for elementos in self.primos_paternos:
           if elementos.codigo == 'OTROS':
              self.primos_paternos_otro = True
              break
           else:
              self.primos_paternos_otro = False

#     @api.multi
    @api.onchange('primos_maternos')
    def _otros_primos_maternos(self):
        for elementos in self.primos_maternos:
           if elementos.codigo == 'OTROS':
              self.primos_maternos_otro = True
              break
           else:
              self.primos_maternos_otro = False


#     @api.multi
    @api.onchange('e_cronicodegen')
    def _otros_e_cronicodegen(self):
        for elementos in self.e_cronicodegen:
            if elementos.codigo_cd == 'OTRAS':
                self.e_cronicodegen_otro = True
                break
            else:
                self.e_cronicodegen_otro = False
            if elementos.codigo_cd == 'CA':
                self.e_cronicodegen_otro = True
                break
            else:
                self.e_cronicodegen_otro = False
              
    def crear_paciente_paciente(self):        
        return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'pacientes',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context': {'expediente_clinico': self.id,'is_new_popup':True}
                }
    def cita_deseguimiento_citas(self):
        #ctx = self.env.context.copy()
        #ctx.update({'default_paciente' : self.paciente.id})
        return {
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'citas.salud',
                'target': 'new',
                'type': 'ir.actions.act_window',
                'context':{'expediente_clinico': self.id,'is_new_popup':True,'default_paciente':self.paciente.id, 'default_fecha' : self.fecha}
                }    
#     @api.multi
    @api.onchange('paciente')
    def _set_paciente(self):
        if self.paciente:
            values = {
                  'nombre_completo': self.paciente.nombre_completo,
                  'unidad_medica': self.paciente.unidad_medica,
                  'edad': self.paciente.edad
                  }
            self.update(values)

class DocumentosAdjuntos(models.Model):
    _name = "expediente.documentos"

    docuemnto = fields.Binary('Documento Adjunto')
    doc_name = fields.Char('Nombre de archivo')
    description = fields.Char('Descripción')
    doc_id = fields.Many2one('expediente.clinico', 'Adjuntos')

class NotaEvolucion(models.Model):
    _name = "nota.evolucion"

    doc_id = fields.Many2one('expediente.clinico', 'Nota De Evolución')
    fecha= fields.Date('Fecha')
    hora= fields.Float('Hora')
    peso = fields.Char(string="Peso KG")
    talla = fields.Char(string="Talla CM")
    #SIGNOS VITALES
    ta = fields.Char(string="T/A")
    temperatura = fields.Char(string="Temperatura ℃")
    fc = fields.Char(string="FC")
    fr = fields.Char(string="FR")
    sp02 = fields.Char(string="Sp02")