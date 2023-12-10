# -*- coding: utf-8 -*-
{
    'name': "Custom Purchase  Order",

    'summary': """
        Custom Field, penambahan menu cara pembayaran, custom print out purchase order""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Fajar - 081268888199",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchases',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',

        'report/purchase_order_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}