# -*- coding: utf-8 -*-

from odoo import models, fields, api

class installment_line(models.Model):
    _name = 'installment.line'
    _order = 'date,name'
    _description = 'installment_line'

    name = fields.Char('Nombre')
    employee_id = fields.Many2one('hr.employee',string='Empleado')
    loan_id = fields.Many2one('employee.loan',string='Deducción',required="1", ondelete='cascade')
    date = fields.Date('Fecha')
    is_paid = fields.Boolean('Pagado')
    amount = fields.Float('Monto de la deducción')
    interest = fields.Float('Interés total')
    ins_interest = fields.Float('Interés')
    installment_amt = fields.Float('Cantidad a plazos')
    total_installment = fields.Float('Total',compute='get_total_installment')
    payslip_id = fields.Many2one('hr.payslip',string='Boleta de pago')
    is_skip = fields.Boolean('Skip Installment')
    tipo_deduccion = fields.Selection([('1','Préstamo'), ('2','Descuento periodico 1'), ('3','Descuento periodico 2')], string='Tipo de deducción')

    @api.depends('installment_amt','ins_interest')
    def get_total_installment(self):
        for line in self:
            line.total_installment = line.ins_interest + line.installment_amt
            
            
        
   
    def action_view_payslip(self):
        if self.payslip_id:
            return {
                'view_mode': 'form',
                'res_id': self.payslip_id.id,
                'res_model': 'hr.payslip',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                
            }
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
