# See LICENSE file for full copyright and licensing details.

{
    'name': 'Bi Report Card',
    'version': "13.0",
    'author': 'BASSAM INFOTECH',
    'website': '',
    'category': 'School Management',
    'license': "AGPL-3",
    'summary': 'A Module Contains Report Card Printout',
    'complexity': 'easy',
    'depends': ['school','bi_exam','school_attendance',],
    'data': [
            'data/paperformact.xml',
            'report/report_card.xml',
            'report/report.xml',
            'report/wizard.xml',
             ],
    'demo': [],
    'installable': True,
    'application': True,
}
