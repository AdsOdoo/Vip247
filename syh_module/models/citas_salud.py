# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from datetime import datetime, timedelta
import pytz, babel
from odoo import tools
import logging
import string
_logger = logging.getLogger(__name__)
from .tzlocal import get_localzone
from pytz import timezone


# class CalendarEvent(models.Model):
#     _inherit = 'calendar.event'
#      
#     @api.model_create_multi
#     def create(self,vals):
#         res = super(CalendarEvent, self).create(vals)
#         return res

class CitasSalud(models.Model):
    _name = 'citas.salud'
    _rec_name = "name"
    
    citas_salud = fields.Char("Cita", default=lambda self: _('New'))
    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    unidad_medica = genero = fields.Selection([
        ('01', 'SOMNOX'),
        ('02', 'SALUD Y HOGAR EXPRESS')
        ], store=True)  

    paciente = fields.Many2one('pacientes',"Paciente", required=True)
    nombre_completo = fields.Char(string="Nombre",related='paciente.nombre_completo', store=True)
    doctor = fields.Many2one('res.partner', string='Doctor(a)', required=True,domain="[('doctor', '=', True)]") 

    fecha = fields.Date("Fecha",readonly=True,required=True)
    hora = fields.Float("Hora",readonly=True,required=True)

    state = fields.Selection([
            ('draft', 'Borrador'),
            ('done', 'Validado')
            ],default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('citas.salud') or _('New')
        result = super(CitasSalud, self).create(vals)
        return result
    
    @api.model
    def _get_date_formats(self):
        """ get current date and time format, according to the context lang
            :return: a tuple with (format date, format time)
        """
        lang = self._context.get("lang")
        lang_params = {}
        if lang:
            record_lang = self.env['res.lang'].search([("code", "=", lang)], limit=1)
            lang_params = {
                'date_format': record_lang.date_format,
                'time_format': record_lang.time_format
            }

        # formats will be used for str{f,p}time() which do not support unicode in Python 2, coerce to str
        format_date = lang_params.get("date_format", '%B-%d-%Y').encode('utf-8')
        format_time = lang_params.get("time_format", '%I-%M %p').encode('utf-8')
        return (format_date, format_time)
    
#     @api.multi
    def get_interval(self, interval, tz=None):
        """ Format and localize some dates to be used in email templates
            :param string interval: Among 'day', 'month', 'dayname' and 'time' indicating the desired formatting
            :param string tz: Timezone indicator (optional)
            :return unicode: Formatted date or time (as unicode string, to prevent jinja2 crash)
        """
        self.ensure_one()
        date = fields.Datetime.from_string(self.fecha)

        if tz:
            timezone = pytz.timezone(tz or 'UTC')
            date = date.replace(tzinfo=pytz.timezone('UTC')).astimezone(timezone)

        if interval == 'day':
            # Day number (1-31)
            result = date.day

        elif interval == 'month':
            # Localized month name and year
            result = babel.dates.format_date(date=date, format='MMMM y', locale=self._context.get('lang') or 'en_US')

        elif interval == 'dayname':
            # Localized day name
            result = babel.dates.format_date(date=date, format='EEEE', locale=self._context.get('lang') or 'en_US')

        elif interval == 'time':
            result = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(self.hora) * 60, 60))
            # Localized time
            #dummy, format_time = self._get_date_formats()
            #result = tools.ustr(date.strftime(format_time + " %Z"))

        return result
    
    #Validar
    def validar_nota(self):
        self.write({'state': 'done'})
        hora_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(float(self.hora) * 60, 60))
        fecha = datetime.strftime(self.fecha, '%Y-%m-%d')
        
        date_time = fecha + " " + hora_time

        timezone = self._context.get('tz')
        if not timezone:
            timezone = self.env.user.partner_id.tz or 'UTC'
#         timezone = tools.ustr(timezone).encode('utf-8')

#         local = pytz.timezone(timezone)
#         naive_from = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
#         local_dt_from = naive_from.replace(tzinfo=pytz.UTC).astimezone(local)
#         date_from = local_dt_from.strftime ("%Y-%m-%d %H:%M")
        
        local = get_localzone()
        naive_from = datetime.strptime(date_time, '%Y-%m-%d %H:%M')
        local_dt_from = local.localize(naive_from, is_dst=None)
        utc_dt_from = local_dt_from.astimezone (pytz.utc)
        date_from = utc_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
        
#         cld_event = self.env['calendar.event']
#         event = {
#                 'name' : 'Cita ' + (self.nombre_completo or ''),
#                 'start_datetime': datetime.strptime(date_from,  "%Y-%m-%d %H:%M"), #datetime.now(),
#                 'partner_ids': [(6,0,[self.doctor.id])],
#                 'duration': 60,
#                 'description': 'Cita ' + (self.nombre_completo or ''),
#                 'start': datetime.strptime(date_from,  "%Y-%m-%d %H:%M") or datetime.now(),
#                 'stop': datetime.strptime(date_from,  "%Y-%m-%d %H:%M") + timedelta(minutes=60)
#                 }
#         print(event)
#         
#         evento = cld_event.create(event)

        evento = self.env['calendar.event'].create({
                                            'name' : 'Cita ' + (self.nombre_completo or ''),
                                            'start_datetime': date_from,
                                            'stop_datetime' : (datetime.strptime(date_from,  "%Y-%m-%d %H:%M:%S") + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S'),
                                            'partner_ids': [(6,0,[self.doctor.id])],
                                            'duration': 60,
                                            'description': 'Cita ' + (self.nombre_completo or ''),
                                            'start': date_from or datetime.now().strftime('%Y-%m-%d %H:%M:%S'), #(datetime.strptime(date_from,  "%Y-%m-%d %H:%M:%S")
                                            'stop': (datetime.strptime(date_from,  "%Y-%m-%d %H:%M:%S") + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
                                            })
        
        if self.paciente and self.paciente.correo_electronico:
            if self.unidad_medica == '01':
                template = self.env.ref('syh_module.calendar_template_meeting_invitation_somnox',False)
            else:
                template = self.env.ref('syh_module.calendar_template_meeting_invitation_syh',False)
            if template:
            #   value = self.env['mail.compose.message'].onchange_template_id(template.id, '', self._name, self.id)['value']
            #   mail = self.env['mail.mail'].create(value)
                template.send_mail(self.id, force_send=True,email_values={'email_to':self.paciente.correo_electronico})

#             mail = self.env['mail.mail'].create({
#                                           'subject' : 'Cita '+(self.fecha or ''),
#                                           'body_html' : "<p>Hola, " + (self.nombre_completo or '') +" este es un recordatorio de su cita para el día " + (self.fecha or '') + " con el Dr.(a) " + (self.doctor.name or '') + " el día " + (self.fecha or '') +" .</p>",
#                                           'email_to' : self.paciente.correo_electronico
#                                           })
            #  mail.send()
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
            
    def save_cita_deseguimiento_citas(self):
        
        return True