{
    'name': 'Dispatch Management',
    'version': '1.0',
    'category': 'Inventory',
    'depends': ['stock', 'sale', 'purchase', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/dispatch_view.xml',
    ],
    'installable': True,
    'application': True,
}
