# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class Empleado(models.Model):
    _inherit = "hr.employee"

    paciente_count = fields.Integer('Paciente', compute='_compute_paciente')
    paciente_ids = fields.One2many('pacientes', 'employee_id', 'Paciente')

    def _compute_paciente(self):
        for pacient in self:
            pacient.paciente_count = len(pacient.paciente_ids)

    def action_view_paciente(self):
        pacientes = self.mapped('paciente_ids')
        action = self.env.ref('syh_module.action_pacientes_tree').read()[0]
        if len(pacientes) > 1:
            action['domain'] = [('id', 'in', pacientes.ids)]
        elif len(pacientes) == 1:
            action['views'] = [(self.env.ref('syh_module.view_expediente_clinico_form').id, 'form')]
            action['res_id'] = pacientes.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action