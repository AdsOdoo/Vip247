# -*- coding: utf-8 -*-
##############################################################################
#                 @author IT Admin
#
##############################################################################

{
    'name': 'Reporte de Logistica',
    'version': '13.1',
    'description': ''' Agrega un reporte de logistica
    ''',
    'category': 'project',
    'author': 'Sergio Medrano',
    'website': 'www.saludyhogar.mx',
    'depends': [
        'base','project',
    ],
    'data': [
        #'views/sale_rental_view.xml',
        'report/report_folio_logistica.xml',
    ],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',	
}
