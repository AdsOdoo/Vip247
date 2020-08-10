# Copyright 2014 - Vauxoo http://www.vauxoo.com/
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import safe_eval as eval

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    new_date = fields.Datetime(string="Nueva fecha",compute='nueva_fecha')
    
    
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


    
    def nueva_fecha(self):
        if self.date_end:
            end_date = datetime.datetime.strptime(self.date_end, "%Y-%m-%d")
            self.new_date = end_date + datetime.timedelta(days=2) 

    
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
            payslip.move_id.button_cancel()
            payslip.move_id.unlink()
#             else:
#                 payslip.move_id.reverse_moves()
#                 payslip.move_id = False

        return self.write({'state': 'cancel'})
