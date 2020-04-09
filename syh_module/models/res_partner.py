# -*- coding:utf-8 -*-


from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    doctor = fields.Boolean(string=_('Doctor'))