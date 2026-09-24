# app/modules/pagos/services.py
"""
Servicio de Mercado Pago. Toda la lógica de la integración vive acá,
separada de las rutas (así podés testearla sin levantar el server).

El SDK oficial es mercadopago (ya está en requirements.txt):

    import mercadopago

    sdk = mercadopago.SDK(current_app.config['MP_ACCESS_TOKEN'])

    # 1) Crear una PREFERENCIA -> uno o varios items a cobrar
    preference_data = {
        'items': [
            {
                'title': '...',
                'quantity': 1,
                'unit_price': float(precio),   # SIEMPRE en float
            }
        ],
        'external_reference': str(pedido.id),   # tu id para reconocer el pago
        'back_urls': {
            'success': url_absoluta('pagos.success'),
            'pending': url_absoluta('pagos.pending'),
            'failure': url_absoluta('pagos.failure'),
        },
        'auto_return': 'approved',
        'notification_url': current_app.config['MP_WEBHOOK_URL'],
        'payment_methods': {'excluded_payment_types': [{'id': 'ticket'}]},
    }
    response = sdk.preference().create(preference_data)
    init_point = response['response']['init_point']   # URL del Checkout de MP
    preference_id = response['response']['id']

    # 2) Consultar el estado REAL de un pago (usado por el webhook)
    payment = sdk.payment().get(mp_payment_id)
    status = payment['response']['status']      # approved / pending / rejected
    status_detail = payment['response']['status_detail']

IMPORTANTE: el estado real hay que consultarlo con payment().get() —
NUNCA confíes en el webhook tal cual lo manda MP (siempre verificás
consultando el pago). La "preferencia" solo redirige al checkout.
"""