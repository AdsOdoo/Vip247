# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle 
#
##############################################################################

from odoo import models, fields, api, _
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'
    
    installment_ids = fields.Many2many('installment.line',string='Pŕestamos')
    installment_amount = fields.Float('Monto Pŕestamo',compute='get_installment_amount')
    installment_int = fields.Float('Interés Péstamo',compute='get_installment_amount')
    descuento1_amount = fields.Float('Monto descuento 1',compute='get_descuento1_amount')
    descuento1_int = fields.Float('Interés descuento 1',compute='get_descuento1_amount')
    descuento2_amount = fields.Float('Monto descuento 2',compute='get_descuento2_amount')
    descuento2_int = fields.Float('Interés descuento 2',compute='get_descuento2_amount')
    rp_dias_completos = fields.Float('dias completos', compute='get_dias_completos')
    rp_dias_laborados = fields.Float('dias laborados', compute='get_dias_laborados')
    rp_dias_periodo = fields.Float('dias periodo', compute='get_dias_periodo')
    rp_gravado = fields.Float('gravado', compute='get_gravado')
    rp_limite_inferior = fields.Float('rp_limite_inferior', compute='get_tablas_values')
    rp_cuota_fija = fields.Float('rp_cuota_fija', compute='get_tablas_values')
    rp_porcentaje = fields.Float('rp_porcentaje', compute='get_tablas_values')
    rp_subsidio = fields.Float('rp_subsidio', compute='get_tablas_values')
    retardo = fields.Boolean(string=_('Retardo'), compute='_get_retardo', default = False)

    
    def compute_sheet(self):
        for data in self:
            installment_ids = self.env['installment.line'].search(
                    [('employee_id', '=', data.employee_id.id), ('loan_id.state', '=', 'done'),
                     ('is_paid', '=', False),('date','<=',data.date_to)])
            if installment_ids:
                data.installment_ids = [(6, 0, installment_ids.ids)]
        return super(hr_payslip,self).compute_sheet()
    
#    
#    def compute_sheet(self):
#        installment_ids = self.env['installment.line'].search(
#                [('employee_id', '=', self.employee_id.id), ('loan_id.state', '=', 'done'),
#                 ('is_paid', '=', False),('date','<=',self.date_to)])
#        if installment_ids:
#            self.installment_ids = [(6, 0, installment_ids.ids)]
#        return super(hr_payslip,self).compute_sheet()
        

    @api.depends('installment_ids')
    def get_installment_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '1':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.installment_amount = amount
            payslip.installment_int = int_amount

    @api.depends('installment_ids')
    def get_descuento1_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '2':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento1_amount = amount
            payslip.descuento2_int = int_amount

    @api.depends('installment_ids')
    def get_descuento2_amount(self):
        for payslip in self:
            amount = 0
            int_amount = 0
            if payslip.installment_ids:
                for installment in payslip.installment_ids:
                    if not installment.is_skip and installment.tipo_deduccion == '3':
                        amount += installment.installment_amt
                        int_amount += installment.ins_interest
            payslip.descuento2_amount = amount
            payslip.descuento2_int = int_amount

    @api.onchange('employee_id')
    def onchange_employee(self):
        if self.employee_id:
            installment_ids = self.env['installment.line'].search(
                [('employee_id', '=', self.employee_id.id), ('loan_id.state', '=', 'done'),
                 ('is_paid', '=', False),('date','<=',self.date_to)])
            if installment_ids:
                self.installment_ids = [(6, 0, installment_ids.ids)]

    @api.onchange('installment_ids')
    def onchange_installment_ids(self):
        if self.employee_id:
            installment_ids = self.env['installment.line'].search(
                [('employee_id', '=', self.employee_id.id), ('loan_id.state', '=', 'done'),
                 ('is_paid', '=', False), ('date', '<=', self.date_to)])
            if installment_ids:
                self.installment_ids = [(6, 0, installment_ids.ids)]

    
    def action_payslip_done(self):
        res = super(hr_payslip, self).action_payslip_done()
        if self.installment_ids:
            for installment in self.installment_ids:
                #if not installment.is_skip:
                installment.is_paid = True
                installment.payslip_id = self.id

#    @api.depends('installment_ids')
    def get_dias_laborados(self):
        for payslip in self:
            dias = payslip.imss_dias
            work_lines = payslip.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id)])
            for line in work_lines:
                if line.code == 'FI' or line.code == 'FJS' or line.code == 'FR' or line.code == 'INC_RT' or line.code == 'INC_EG' or line.code == 'INC_MAT':
                    dias -= 1
            payslip.rp_dias_laborados =  dias

    def get_dias_completos(self):
        for payslip in self:
            dias = payslip.imss_dias
            work_lines = payslip.env['hr.payslip.worked_days'].search([('payslip_id','=',payslip.id)])
            for line in work_lines:
                if line.code == 'INC_RT' or line.code == 'INC_EG' or line.code == 'INC_MAT':
                    dias -= 1
            payslip.rp_dias_completos =  dias

    def get_dias_periodo(self):
        for payslip in self:
            dias = 0
            lines = payslip.contract_id.env['tablas.periodo.bimestral'].search([('form_id','=',payslip.contract_id.tablas_cfdi_id.id),('dia_fin','>=',payslip.date_to),('dia_inicio','<=',payslip.date_to)],limit=1)
            if lines:
                dias = lines.no_dias/4
            payslip.rp_dias_periodo =  dias

    def get_gravado(self):
        for payslip in self:
            gravado = 0
            lines = payslip.env['hr.payslip.line'].search([('code','=','TPERG'),('slip_id','=',payslip.id)],limit=1)
            if lines:
                gravado = lines.amount
            payslip.rp_gravado =  gravado

    @api.depends('rp_gravado')
    def get_tablas_values(self):
        grabado_mensual = 0
        for payslip in self:
            if payslip.no_nomina == '2':
                grabado_mensual = payslip.rp_gravado + payslip.acum_per_grav
            else:
                grabado_mensual = payslip.rp_gravado  / payslip.dias_pagar * payslip.contract_id.tablas_cfdi_id.imss_mes

            lines = payslip.contract_id.env['tablas.general.line'].search([('form_id','=',payslip.contract_id.tablas_cfdi_id.id),('lim_inf','<=',grabado_mensual)],order='lim_inf desc',limit=1)
            if lines:
                payslip.rp_limite_inferior =  lines.lim_inf
                payslip.rp_cuota_fija =  lines.c_fija
                payslip.rp_porcentaje =  lines.s_excedente
            lines2 = payslip.contract_id.env['tablas.subsidio.line'].search([('form_id','=',payslip.contract_id.tablas_cfdi_id.id),('lim_inf','<=',grabado_mensual)],order='lim_inf desc',limit=1)
            if lines2:
               payslip.rp_subsidio =  lines2.s_mensual


    @api.onchange('date_to')
    def _get_retardo(self):
        if self.date_to and self.date_from:
            line = self.env['retardo.nomina'].search([('employee_id','=',self.employee_id.id),('fecha','>=',self.date_from),
                                                                    ('fecha','<=',self.date_to),('state','=','done')])
            if line:
                self.retardo = True
            else:
                self.retardo = False

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    
    @api.depends('slip_ids.state','slip_ids.estado_factura')
    def _compute_show_cancelar_button(self):
        for payslip_batch in self:
            show_button = True
            for payslip in payslip_batch.slip_ids:
                if payslip.state != 'done'  or payslip.estado_factura!='factura_correcta':
                    show_button=False
                    break
            payslip_batch.show_cancelar_button = show_button
        
    show_cancelar_button = fields.Boolean('Show Cancelar CFDI/Payslip Button', compute='_compute_show_cancelar_button')
    
    
    def action_cancelar_cfdi(self):
        if hasattr(self.slip_ids, 'action_cfdi_cancel'):
            self.slip_ids.action_cfdi_cancel()
        return True
    
    
    def action_cancelar_nomina(self):
        self.slip_ids.action_payslip_cancel()
        return True
    
    
    
   
    def get_department(self):
        result = {}
        department = self.env['hr.department'].search([])
        for dept in department:
            result[dept.id] = dept.name
        return result

  
    def get_payslip_group_by_department(self):
        result = {}
        for line in self.slip_ids:
            if line.employee_id.department_id.id in result.keys():
                result[line.employee_id.department_id.id].append(line)
            else:
                result[line.employee_id.department_id.id] = [line]
        return result
    
class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    refunded_id = fields.Many2one(
        'hr.payslip',
        string='Refunded Payslip',
        readonly=True
    )
    
    
    def refund_sheet(self):
        res = super(HrPayslip, self).refund_sheet()
        self.write({'refunded_id': eval(res['domain'])[0][2][0] or False})
        return res

    
    def action_payslip_cancel(self):
        for payslip in self:
            if payslip.refunded_id and payslip.refunded_id.state != 'cancel':
                raise ValidationError(_("""To cancel the Original Payslip the
                    Refunded Payslip needs to be canceled first!"""))
                """
                     Change by tushar update_posted not availabel in account.journal
                """
          #  payslip.move_id.button_cancel()
          #  payslip.move_id.unlink()
       
        return self.write({'state': 'cancel'})
