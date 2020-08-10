# -*- coding: utf-8 -*-

from odoo import models, api, fields
import time

class ReportGeneralLedger(models.AbstractModel):
    _name = 'report.nomina_cfdi_extras_ee.report_calculo_isr_anual'
    _description = 'ReportGeneralLedger'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'calculo.isr.anual',
            'data': data,
            'docs': self.env['calculo.isr.anual'].browse(docids),
            'time': time,
        }

class CalculoISRAnual(models.TransientModel):
    _name = 'calculo.isr.anual'
    _description = 'CalculoISRAnual'

    ano = fields.Selection([('2019','2019'),('2020','2020'),('2021', '2021')],"Año")
    employee_id =fields.Many2one('hr.employee','Empleado')
    department_id = fields.Many2one('hr.department', 'Departamento')
    
   
    def print_calculo_isr_anual_report(self):
        date_from = self.ano+"-01-01"
        date_to = self.ano+"-12-31"
        domain = [('date_from','>=',date_from), ('date_to', '<=', date_to)]
        domain.append(('state','=', 'done'))
        if self.employee_id:
            domain.append(('employee_id','=',self.employee_id.id))
        elif self.department_id:
            domain.append(('employee_id.department_id','=',self.department_id.id))
        payslips = self.env['hr.payslip'].search(domain)
        all_col_list_seq = []
        search_code = ['TPERG', 'ISR', '201']
        result = {}
        total_by_code = {}
        emp_by_ids = {}
        for line in payslips.mapped('line_ids'):
            if line.code in search_code: #all_col_list_seq:
                if line.code not in all_col_list_seq:
                    all_col_list_seq.append(line.code)
                    total_by_code[line.code] = 0
                total = line.total
                total_by_code[line.code] += total

                employee = line.slip_id.employee_id
                emp_id = employee.id
                if emp_id not in result:
                    result[emp_id] = {}
                    emp_by_ids[emp_id] = employee.name
                if line.code not in result[emp_id]:
                    result[emp_id][line.code] = total
                else:
                    result[emp_id][line.code] = result[emp_id][line.code] + total

        company = self.env.user.company_id
        data = {'emp_by_ids' : emp_by_ids,'result':result,'all_col_list_seq' :all_col_list_seq, 'company_name' : company.name, 'company_rfc' : company.rfc or '', 'total_by_code':total_by_code}
        return self.sudo().env.ref('nomina_cfdi_extras_ee.action_report_calculo_isr_anual').report_action(self, data=data)
