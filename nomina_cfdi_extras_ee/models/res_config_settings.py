# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    numoer_de_retardos_x_falta = fields.Integer("Numoer de retardos x falta")
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            numoer_de_retardos_x_falta=int(params.get_param('nomina_cfdi_extras_ee.numoer_de_retardos_x_falta', 0))
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('nomina_cfdi_extras_ee.numoer_de_retardos_x_falta', self.numoer_de_retardos_x_falta)
    