# -*- coding: utf-8 -*-

from odoo import fields, models
import odoo.addons.decimal_precision as dp


class SalesDiscountLimit(models.Model):
    """Configuration for Set Sale Discount Limit."""

    _name = "sales.discount.limit"
    _rec_name = "group_id"
    _order = "discount desc"
    _sql_constraints = [
        ('discount', 'check(discount >= 1 and discount <= 100)',
         'El descuento debe ser entre 1 y 100.'),
        ('group_id_uniq', 'unique(group_id)',
            'El grupo ya existe!'),
    ]

    group_id = fields.Many2one(
        'res.groups', "Grupo")
    discount = fields.Float("Descuento (%)",
                            digits=dp.get_precision('Descuento'), default=10.0)
