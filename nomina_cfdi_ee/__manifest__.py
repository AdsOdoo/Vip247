# -*- coding: utf-8 -*-

{
    'name': 'Nomina Electrónica para México CFDI v1.2 EE',
    'summary': 'Agrega funcionalidades para timbrar la nómina electrónica en México para la versión EE.',
    'description': '''
    Nomina CFDI Module
    ''',
    'author': 'IT Admin',
    'version': '13.0.2',
    'category': 'Employees',
    'depends': [
        'om_hr_payroll',
    ],
    'data': [
#        'data/hr_payroll_data.xml',
        'data/sequence_data.xml',
        'data/cron.xml',
        'data/nomina.otropago.csv',
        'data/nomina.percepcion.csv',
        'data/nomina.deduccion.csv',
        'views/hr_employee_view.xml',
        'views/hr_contract_view.xml',
        'views/hr_salary_view.xml',
        'views/hr_payroll_payslip_view.xml',
        'views/tablas_cfdi_view.xml',
        'views/res_company_view.xml',
        'report/report_payslip.xml',
        'views/res_bank_view.xml',
        'data/mail_template_data.xml',
        'security/ir.model.access.csv',
        'data/res.bank.csv',
        'views/menu.xml',
        'views/horas_extras_view.xml',
        'wizard/wizard_liquidacion_view.xml',
        'wizard/import_nomina_xml.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'AGPL-3',
}
