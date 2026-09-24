{
    'name': 'Usend Delivery Integration',
    'version': '18.0.1.0.0',
    'summary': 'Integración con la API de Usend Chile (cotización y etiquetas)',
    'description': """
        Módulo que extiende delivery.carrier para cotizar envíos y generar
        etiquetas/OT a través de la API REST de Usend Chile.

        Servicios cubiertos (por prioridad):
        - Cotizador (cotizarenvio)
        - Etiquetas (ge)
        - Tracking            # TODO: fase posterior
        - Logística Inversa   # TODO: fase posterior, sin confirmar con Usend
    """,
    'author': 'TODO: tu nombre / Siembra Chile SpA',
    'website': 'TODO: si aplica',
    'category': 'Inventory/Delivery',
    'license': 'TODO: definir (LGPL-3 es el default de Odoo)',

    # TODO: confirmar si necesitas 'sale' o 'stock' además de 'delivery'
    # (delivery ya arrastra stock como dependencia transitiva)
    'depends': [
        'delivery',
    ],

    'data': [
        # TODO: agregar aquí los .xml de security/views a medida que existan
        # 'security/ir.model.access.csv',
        # 'views/delivery_carrier_views.xml',
    ],

    'installable': True,
    'application': False,
}
