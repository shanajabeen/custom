# See LICENSE file for full copyright and licensing details.

{
    'name': 'BI REPORTS',
    'version': "13.0.1.0.0",
    'author': 'BASSAM INFOTECH',
    'website': '',
    'category': 'School Management',
    'license': "AGPL-3",
    'summary': 'A Module For Exams Management Taken In School',
    'complexity': 'easy',
    'depends': ['school', 'bi_exam'],
    'data': ['report/bi_report_format.xml',
        'report/class_exam_result.xml',
            'report/report_print.xml',
             'wizard/class_result.xml',
             
             
             ],
    'demo': [],
    'installable': True,
    'application': True,
}
