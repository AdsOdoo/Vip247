# -*- coding: utf-8 -*-

from odoo import models, api, fields,_
from datetime import datetime
from datetime import date

import time
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)

class GeneraLiquidaciones(models.TransientModel):
    _name = 'calculo.liquidaciones'
    _description = 'GeneraLiquidaciones'

    fecha_inicio = fields.Date(string='Fecha inicio último periodo')
    fecha_liquidacion = fields.Date(string='Fecha liquidacion')
    employee_id =fields.Many2one("hr.employee",'Employee')
    dias_base = fields.Float('Días base', default='90')
    dias_x_ano = fields.Float('Días por cada año trabajado', default='20')
    dias_totales = fields.Float('Total de días', store=True)
    indemnizacion = fields.Boolean("Pagar indemnización")
    antiguedad = fields.Boolean("Pagar antiguedad")
    dias_pendientes_pagar = fields.Float('Días de nómina a pagar', store=True)
    dias_vacaciones = fields.Float('Días de vacaciones')
    dias_aguinaldo = fields.Float('Días aguinaldo')
    dias_prima_vac = fields.Float('Días prima vacacional')
    fondo_ahorro = fields.Float('Fondo ahorro', compute="get_fondo_ahorro", store=True)
    pago_separacion = fields.Float("Pago por separación")
    contract_id = fields.Many2one('hr.contract', string='Contrato')
    antiguedad_anos = fields.Float('Antiguedad', store=True)

    monto_prima_antiguedad = fields.Float('Prima antiguedad', store=True)
    monto_indemnizacion = fields.Float('Indemnizacion', store=True)
    tipo_de_baja = fields.Selection([('01','Separación voluntaria'),
                                      ('02','Baja')], string='Tipo de baja')
    sueldo_calculo = fields.Selection([('01','Sueldo diario'),
                                      ('02','Sueldo diario integrado')], string='Sueldo para cálculos')
    sueldo_calculo_monto  = fields.Float('Sueldo calculo monto')
    tope_prima = fields.Selection([('01','Sueldo diario'),
                                      ('02','UMA')], string='Para calculo topado usar')
    tope_prima_monto  = fields.Float('Tope prima monto')
    estructura  = fields.Many2one('hr.payroll.structure', string='Estructura ordinaria')
    prima_vac = fields.Float('Días aguinaldo prima vacacional')

    def calculo_create(self):
        employee = self.employee_id
        if not employee:
            raise Warning("Seleccione primero al empleado.")
        payslip_batch_nm = 'Liquidacion ' +employee.name
        date_from = self.fecha_inicio
        date_to = self.fecha_liquidacion
        batch = self.env['hr.payslip.run'].create({
            'name' : payslip_batch_nm,
            'date_start': date_from,
            'date_end': date_to,
            'periodicidad_pago': self.contract_id.periodicidad_pago,
            'no_nomina': '1',
            'tipo_nomina': 'E',
            'fecha_pago' : date_to,
            })
        # batch
        payslip_obj = self.env['hr.payslip']
        payslip_onchange_vals = payslip_obj.default_get(payslip_obj.fields_get())
       
        #Creación de nomina ordinaria
        payslip_vals = {**payslip_onchange_vals.get('value',{})} #TO copy dict to new dict. 
        
        structure = self.estructura #self.env['hr.payroll.structure'].search([('name','=','Liquidación - Ordinario')], limit=1)
        if structure: 
            payslip_vals['struct_id'] = structure.id
        
        contract_id = self.contract_id.id
        if not contract_id:
            contract_id = payslip_vals.get('contract_id')
        else:
            payslip_vals['contract_id'] = contract_id 
        
        if not contract_id:
            contract_id = employee.contract_id.id
        if not contract_id:
            raise Warning("No se encontró contrato para %s en el periodo de tiempo."%(employee.name))
        
        worked_days = []
        worked_days.append((0,0,{'name' :'Dias aguinaldo', 'code' : 'AGUI', 'contract_id':contract_id, 'number_of_days': self.dias_aguinaldo}))
        worked_days.append((0,0,{'name' :'Dias vacaciones', 'code' : 'VAC', 'contract_id':contract_id, 'number_of_days': self.dias_vacaciones}))
        worked_days.append((0,0,{'name' :'Prima vacacional', 'code' : 'PVC', 'contract_id':contract_id, 'number_of_days': self.dias_prima_vac}))
        worked_days.append((0,0,{'name' :'Dias a pagar', 'code' : 'WORK100', 'contract_id':contract_id, 'number_of_days': self.dias_pendientes_pagar}))
        
        obj_hr_payslip_input_type=self.env['hr.payslip.input.type'].search([('name','=','Fondo ahorro')],limit=1)
        intput_type_id=False
        if obj_hr_payslip_input_type:
            intput_type_id=obj_hr_payslip_input_type.id
        else:
            obj = obj_hr_payslip_input_type.create({'name':'Fondo ahorro','code':'PFA'})
            intput_type_id=obj.id
            
        payslip_vals['input_line_ids']=[(0,0, {'input_type_id':intput_type_id, 'code': 'PFA', 'amount': self.fondo_ahorro, 'contract_id':contract_id})]
        
        payslip_vals.update({
            'employee_id' : employee.id,
            'worked_days_line_ids' : worked_days,
            'tipo_nomina' : 'O',
            'payslip_run_id' : batch.id,
            'date_from': date_from,
            'date_to': date_to,
            'contract_id' : contract_id,
            'no_nomina': '1',
            'fecha_pago' : date_to,
            'mes': str(date_to.month).zfill(2),
            'dias_pagar': self.dias_pendientes_pagar,
            'imss_dias': self.dias_pendientes_pagar,
            'nom_liquidacion': True,
            
             #'input_line_ids': [(0, 0, x) for x in payslip_vals.get('input_line_ids',[])],
            })
        payslip_obj = self.env['hr.payslip'].new(payslip_vals)
        payslip_obj._onchange_employee()
        payslip_vals = payslip_obj._convert_to_write(payslip_obj._cache)
        payslip_vals['input_line_ids']=[(0,0, {'input_type_id':intput_type_id, 'code': 'PFA', 'amount': self.fondo_ahorro, 'contract_id':contract_id})]
        payslip_obj.create(payslip_vals)
        
        #Creación de nomina extraordinaria
        if self.tipo_de_baja == '02':
            payslip_vals2 = {**payslip_onchange_vals.get('value',{})}
            structure = self.env['hr.payroll.structure'].search([('name','=','Liquidación - indemnizacion/finiquito')], limit=1)
            if structure: 
                payslip_vals2['struct_id'] = structure.id

            other_inputs = []
            intput_type_id=False
            obj_hr_payslip_input_type=self.env['hr.payslip.input.type'].search([('name','=','Prima antiguedad')],limit=1)
            if not obj_hr_payslip_input_type:
                obj_hr_payslip_input_type = obj_hr_payslip_input_type.create({'name':'Prima antiguedad','code':'PDA','struct_ids':structure.id})
           
            obj_hr_payslip_input_type_1=self.env['hr.payslip.input.type'].search([('name','=','Indemnizacion')],limit=1)
            if not obj_hr_payslip_input_type_1:
                obj_hr_payslip_input_type_1 = obj_hr_payslip_input_type.create({'name':'Indemnizacion','code':'IND','struct_ids':structure.id})
            
            obj_hr_payslip_input_type_2=self.env['hr.payslip.input.type'].search([('name','=','Pago por separacion')],limit=1)
            if not obj_hr_payslip_input_type_2:
                obj_hr_payslip_input_type_2 = obj_hr_payslip_input_type.create({'name':'Pago por separacion','code':'WORK100','struct_ids':structure.id})
           
            worked_days2 = []
            worked_days2.append((0,0,{'name' :'Dias a pagar', 'code' : 'WORK100', 'contract_id':contract_id, 'number_of_days': 0}))

            payslip_vals2.update({
               'employee_id' : employee.id,
               'tipo_nomina' : 'E',
               'input_line_ids' : other_inputs,
               'payslip_run_id' : batch.id,
               'date_from': date_from,
               'date_to': date_to,
               'contract_id' : contract_id,
               'fecha_pago' : date_to,
               'worked_days_line_ids': worked_days2, #[(0, 0, x) for x in payslip_vals2.get('worked_days_line_ids',[])],
            })
            payslip_obj = self.env['hr.payslip'].new(payslip_vals2)
            payslip_obj._onchange_employee()
            payslip_vals2 = payslip_obj._convert_to_write(payslip_obj._cache)
            other_inputs.append((0,0,{'input_type_id':obj_hr_payslip_input_type.id,'amount': self.monto_prima_antiguedad}))
            other_inputs.append((0,0,{'input_type_id':obj_hr_payslip_input_type_1.id, 'amount': self.monto_indemnizacion}))
            other_inputs.append((0,0,{'input_type_id':obj_hr_payslip_input_type_2.id, 'amount': self.pago_separacion}))
            payslip_vals2['input_line_ids']=other_inputs
            payslip_obj.create(payslip_vals2)
            
        return True
    
    def calculo_liquidacion(self):
        if self.employee_id and self.contract_id:
            #cálculo de conceptos de nómina extraordinaria
            date_start = self.contract_id.date_start
            last_day = self.fecha_liquidacion
            diff_date = last_day - date_start 
            self.antiguedad_anos = diff_date.days /365.0
          
            if self.sueldo_calculo == '01':
                self.sueldo_calculo_monto = self.contract_id.sueldo_diario
            else:
                self.sueldo_calculo_monto = self.contract_id.calculate_sueldo_diario_integrado()

            #calculo de dias a indemnizar
            if self.indemnizacion:
                self.dias_totales = self.antiguedad_anos * self.dias_x_ano + self.dias_base
            else:
                self.dias_totales = 0
            self.monto_indemnizacion = self.dias_totales * self.sueldo_calculo_monto

            # calculo prima antiguedad: 12 días de salario por cada año de servicio.
            if self.antiguedad:
                tope_prima_antiguedad = 2 * self.contract_id.tablas_cfdi_id.salario_minimo
                _logger.info('dias tope_prima_antiguedad %s', tope_prima_antiguedad)
                if self.tope_prima == '01':
                    self.tope_prima_monto = self.contract_id.tablas_cfdi_id.salario_minimo
                else:
                    self.tope_prima_monto = self.contract_id.tablas_cfdi_id.uma

                if self.sueldo_calculo_monto > tope_prima_antiguedad:
                    _logger.info('mayor')
                    self.monto_prima_antiguedad = round(self.antiguedad_anos) * 12 * self.tope_prima_monto * 2
                else:
                    _logger.info('menor')
                    self.monto_prima_antiguedad = round(self.antiguedad_anos) * 12 * self.sueldo_calculo_monto
            else:
                self.monto_prima_antiguedad = 0

            #cálculo de conceptos de nómina ordinaria
            #dias pendientes a pagar en ultima nomina
            delta_dias  = self.fecha_liquidacion - self.fecha_inicio
            self.dias_pendientes_pagar = delta_dias.days + 1

            #Dias de aguinaldo
            year_date_start = self.contract_id.date_start.year
            first_day_date = datetime(date.today().year, 1, 1)
            if year_date_start < date.today().year:
                delta1 = self.fecha_liquidacion - first_day_date.date()
                self.dias_aguinaldo = delta1.days + 1 
            else:
                delta2 = self.fecha_liquidacion - self.contract_id.date_start
                self.dias_aguinaldo = delta2.days + 1

            if self.contract_id.tablas_cfdi_id:
                line = self.env['tablas.antiguedades.line'].search([('form_id','=',self.contract_id.tablas_cfdi_id.id),('antiguedad','<=',self.antiguedad_anos+1)],order='antiguedad desc',limit=1)
                if line:
                    dias_aguinaldo2 = line.aguinaldo
                    self.dias_aguinaldo = (dias_aguinaldo2*self.dias_aguinaldo)/365.0
                    _logger.info('dias %s, dias aguinaldo %s,', self.dias_aguinaldo, dias_aguinaldo2)

            #dias de vacaciones
            vac_pagada = False
            dias_vac = 0
            if date_start:
                date_start = date_start.replace(last_day.year)
                _logger.info('last_day %s, date_start %s', last_day, date_start) 
                if last_day <= date_start:
                    #_logger.info('last_day <= date_start') 
                    #_logger.info('self.antiguedad_ano %s', self.antiguedad_anos) 
                    date_start = date_start.replace(last_day.year-1)
                    tablas_cfdi_lines = self.contract_id.tablas_cfdi_id.tabla_antiguedades.filtered(lambda x: x.antiguedad <= self.antiguedad_anos+1).sorted(key=lambda x:x.antiguedad, reverse=True)
                    if not tablas_cfdi_lines: 
                        return
                    tablas_cfdi_line = tablas_cfdi_lines[0]
                    #_logger.info('dias vacaciones correspondientes %s', tablas_cfdi_line.vacaciones) 
                    #_logger.info('dias a pagar %s', (last_day - date_start).days +1) 
                    self.dias_vacaciones = ((last_day - date_start).days + 1)  / 365.0 * tablas_cfdi_line.vacaciones
                    self.prima_vac = tablas_cfdi_line.prima_vac
                else:
                    #_logger.info('last_day > date_start') 
                    #_logger.info('self.antiguedad_ano %s', self.antiguedad_anos)
                    tablas_cfdi_lines = self.contract_id.tablas_cfdi_id.tabla_antiguedades.filtered(lambda x: x.antiguedad <= self.antiguedad_anos+1).sorted(key=lambda x:x.antiguedad, reverse=True)
                    if not tablas_cfdi_lines: 
                        return
                    tablas_cfdi_line = tablas_cfdi_lines[0]
                    #_logger.info('dias vacaciones correspondientes %s', tablas_cfdi_line.vacaciones) 
                    #_logger.info('dias a pagar %s', (last_day - date_start).days +1) 
                    self.dias_vacaciones = ((last_day - date_start).days + 1) / 365.0 * tablas_cfdi_line.vacaciones
                    self.prima_vac = tablas_cfdi_line.prima_vac


            #dias de vacaciones adicionales entregados y no pagados
            if self.contract_id.tipo_prima_vacacional == '02':
                ano_buscar = 0
                if last_day <= date_start:
                    ano_buscar = last_day.year -1
                else:
                    ano_buscar = last_day.year
                for lineas_vac in self.contract_id.tabla_vacaciones:
                    if lineas_vac.ano == str(ano_buscar):
                        self.dias_vacaciones += lineas_vac.dias

            #prima vacacional liquidacion
            self.dias_prima_vac = self.dias_vacaciones * self.prima_vac / 100.0

            #fondo de ahorro (si hay)
            self.fondo_ahorro = self.get_fondo_ahorro()

            self.refresh()
          
        action = self.env.ref('nomina_cfdi_ee.action_wizard_liquidacion').read()[0]
        action['res_id'] = self.id
        return action

    def genera_nominas(self):
        dias_vacaciones = 0

    def get_fondo_ahorro(self):
        total = 0
        if self.employee_id and self.contract_id.tablas_cfdi_id:
            year_date_start = self.contract_id.date_start.year
            first_day_date = datetime(date.today().year, 1, 1)
            if year_date_start < date.today().year:
                date_start = first_day_date
            else:
                date_start = self.contract_id.date_start
            date_end = self.fecha_liquidacion

            domain=[('state','=', 'done')]
            if date_start:
                domain.append(('date_from','>=',date_start))
            if date_end:
                domain.append(('date_to','<=',date_end))
            domain.append(('employee_id','=',self.employee_id.id))
            rules = self.env['hr.salary.rule'].search([('code', '=', 'D067')])
            payslips = self.env['hr.payslip'].search(domain)
            payslip_lines = payslips.mapped('line_ids').filtered(lambda x: x.salary_rule_id.id in rules.ids)
            employees = {}
            for line in payslip_lines:
                if line.slip_id.employee_id not in employees:
                    employees[line.slip_id.employee_id] = {line.slip_id: []}
                if line.slip_id not in employees[line.slip_id.employee_id]:
                    employees[line.slip_id.employee_id].update({line.slip_id: []})
                employees[line.slip_id.employee_id][line.slip_id].append(line)

            for employee, payslips in employees.items():
                for payslip,lines in payslips.items():
                    for line in lines:
                        total += line.total
        return total
