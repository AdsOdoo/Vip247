# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class employee_loan_type(models.Model):
    _name = 'employee.loan.type'
    _description = 'employee_loan_type'

    name = fields.Char('Nombre', required="1")
    loan_limit = fields.Float('Límite del monto del deducción', default=5000, required="1")
    loan_term = fields.Integer('Plazo de la deducción', default=12, required="1")
    is_apply_interest = fields.Boolean('Aplicar interés', default=False)
    interest_rate = fields.Float('Taza de interés',default=10)
    interest_type = fields.Selection([('liner','Sobre monto total'),('reduce','Sobre saldo pendiente')],string='Tipo de interés',
                                     default='liner')
                                     
    loan_account = fields.Many2one('account.account',string='Cuenta de prestamo')
    interest_account = fields.Many2one('account.account',string='Cuenta de intereses')
    journal_id = fields.Many2one('account.journal',string='Diario')

    periodo_de_pago = fields.Selection([('Semanal','Semanal'), ('Quincenal','Quincenal')], string='Periodo de pago', required="1")
    tipo_deduccion = fields.Selection([('1','Préstamo'), ('2','Descuento periodico 1'), ('3','Descuento periodico 2')], string='Tipo de deducción', required="1")
    
    @api.constrains('is_apply_interest','interest_rate','interest_type')
    def _check_interest_rate(self):
        for loan in self:
            if loan.is_apply_interest:
                if loan.interest_rate <= 0:
                    raise ValidationError("La tasa de interés debe ser mayor de 0.00")
                if not loan.interest_type:
                    raise ValidationError("Por favor seleccione el tipo de interés")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
