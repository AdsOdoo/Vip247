# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import Warning, UserError
import pytz
from odoo import tools
from .tzlocal import get_localzone

class VacacionesNomina(models.Model):
    _name = 'vacaciones.nomina'
    _description = 'VacacionesNomina'

    name = fields.Char("Name", required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    employee_id = fields.Many2one('hr.employee', string='Empleado')
    fecha_inicial = fields.Date('Fecha inicial')
    dias = fields.Integer('Días')
    dias_de_vacaciones_disponibles = fields.Integer("Dias de vacaciones disponibles")
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Hecho'), ('cancel', 'Cancelado')], string='Estado', default='draft')
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            contract = self.employee_id.contract_id
            if contract:
                self.dias_de_vacaciones_disponibles = sum(vacacione.dias for vacacione in contract.tabla_vacaciones)
        
    @api.onchange('dias')
    def _onchange_dias(self):
        if self.dias and self.dias > self.dias_de_vacaciones_disponibles:
            raise Warning("No tiene suficientes dias de vacaciones")
            
        
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vacaciones.nomina') or _('New')
        result = super(VacacionesNomina, self).create(vals)
        return result
    
    
    def action_validar(self):
        leave_type = self.env.ref('nomina_cfdi_extras_ee.hr_holidays_status_vac', False)
        if self.fecha_inicial:
            date_from = self.fecha_inicial
            date_to = date_from + relativedelta(days=self.dias - 1)
            date_from = date_from.strftime("%Y-%m-%d") + ' 00:00:00'
            date_to = date_to.strftime("%Y-%m-%d") +' 23:59:59'
        else:
            date_from = datetime.today().strftime("%Y-%m-%d")
            date_to = date_from + ' 20:00:00'
            date_from += ' 06:00:00'
        
        timezone = self._context.get('tz')
        if not timezone:
            timezone = self.env.user.partner_id.tz or 'UTC'
        #timezone = tools.ustr(timezone).encode('utf-8')

        local = pytz.timezone(timezone) #get_localzone()
        naive_from = datetime.strptime (date_from, "%Y-%m-%d %H:%M:%S")
        local_dt_from = local.localize(naive_from, is_dst=None)
        utc_dt_from = local_dt_from.astimezone (pytz.utc)
        date_from = utc_dt_from.strftime ("%Y-%m-%d %H:%M:%S")
 
        naive_to = datetime.strptime (date_to, "%Y-%m-%d %H:%M:%S")
        local_dt_to = local.localize(naive_to, is_dst=None)
        utc_dt_to = local_dt_to.astimezone (pytz.utc)
        date_to = utc_dt_to.strftime ("%Y-%m-%d %H:%M:%S")

        nombre = 'Vacaciones_'+self.name
        registro_falta = self.env['hr.leave'].search([('name','=', nombre)], limit=1)
        if registro_falta:
           registro_falta.write({'date_from' : date_from,
                   'date_to' : date_to,
                   'employee_id' : self.employee_id.id,
                   'holiday_status_id' : leave_type and leave_type.id,
                   'state': 'validate',
                   })
        else:
           holidays_obj = self.env['hr.leave']
           vals = {'date_from' : date_from,
               'holiday_status_id' : leave_type and leave_type.id,
               'employee_id' : self.employee_id.id,
               'name' : 'Vacaciones_'+self.name,
               'date_to' : date_to,
               'state': 'confirm',}

           holiday = holidays_obj.new(vals)
           holiday._onchange_employee_id()
           holiday._onchange_leave_dates()
           vals.update(holiday._convert_to_write({name: holiday[name] for name in holiday._cache}))
           #holidays_obj.create(vals)
           vals.update({'holiday_status_id' : leave_type and leave_type.id,})
           vacacion = self.env['hr.leave'].create(vals)
           vacacion.action_validate()
        self.write({'state':'done'})

        dias = self.dias
        if self.employee_id and dias:
            contract = self.employee_id.contract_id
            if contract:
                for vac in contract.tabla_vacaciones.sorted(key=lambda object1: object1.ano):
                    if dias <= vac.dias:
                        vac.write({'dias':vac.dias-dias})
                        break
                    elif dias > vac.dias:
                        dias = dias-vac.dias
                        vac.write({'dias':0})
        return True

    
    def action_cancelar(self):
        self.write({'state':'cancel'})
        nombre = 'Vacaciones_'+self.name
        registro_falta = self.env['hr.leave'].search([('name','=', nombre)], limit=1)
        if registro_falta:
           registro_falta.action_refuse() #.write({'state':'cancel'})

        contract = self.employee_id.contract_id
        if contract:
           vac = contract.tabla_vacaciones.sorted(key=lambda object1: object1.ano)
           saldo_ant = vac[0].dias + self.dias
           vac[0].write({'dias':saldo_ant})

    
    def action_draft(self):
        self.write({'state':'draft'})

    
    def unlink(self):
        raise UserError("Los registros no se pueden borrar, solo cancelar.")