# -*- coding: utf-8 -*-

{
    'name': "Limite de descuento en ventas",
    'summary': """
            Limite de descuento y readonly
             """,
    'description': """
        Permite agregar limites de descuento y hace readonly campo precio unitario.
    """,
    'author': "IT Admin",
    'website': "www.itadmin.com.mx",
    'license': "AGPL-3",
    'category': 'Sales',
    'version': '12.0.1.0.1',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_discount_limit_view.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'installable': True,
    'post_init_hook': '_fill_sales_discount_limit',
}
