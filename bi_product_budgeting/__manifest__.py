# -*- coding: utf-8 -*-
{
    'name': "Product Budgeting",
    'summary': "Track Product Bugeting",
    'author': "Bassam Infotech LLP",
    'website': "https://www.bassaminfotech.com",
    'category': 'Product',
    'version': '14.0.1',
    'depends': ['stock','purchase','branch','bi_ptg_calendar','bi_material_transfer'],
    'data': [
        'security/ir.model.access.csv',
        'views/diesel_line.xml',
        'views/bi_product_budgeting.xml',
        'views/purchase_order.xml',
    ],
    'qweb': ['static/src/xml/purchase_order.xml','static/src/xml/diesel_line.xml'],
    'images': [ 
        'static/description/icon.png',
    ],
    'installable': True,
    'auto_install': False,
}