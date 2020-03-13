# -*- coding: utf-8 -*-
##############################################################################
#                 @author Duvan Zavaleta
#
##############################################################################

{
    'name': 'Hide Parent Address',
    'version': '13.1',
    'description': ''' Hide the parent address in the invoice report
    ''',
    'category': 'Accounting',
    'author': 'IT Admin',
    'website': 'www.itadmin.com.mx',
    'depends': [
        'sale','account',
    ],
    'data': [
        #'report/hide_shipping_address.xml',
        'report/hide_invoice_address.xml',
    ],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',	
}
