# -*- coding: utf-8 -*-
{
    'name': "Bi Employee Payslip",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Bassam Infotech LLP",
    'website': "http://www.bassaminfotech.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','hr','payroll','bi_payroll_report','report_xlsx'],

    'data': [
        'report/bi_payslip_report.xml',
        'wizard/bi_payslip_wizard.xml',
        
    ],
}