# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Reporte de renta',
    'version': '13.1',
    'description': ''' Agrega un reporte a los pedidos de renta
    ''',
    'category': 'Sales',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'base','sale','sale_renting',
    ],
    'data': [
        #'views/sale_rental_view.xml',
        'report/sale_rental_templates.xml',
    ],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',	
}
