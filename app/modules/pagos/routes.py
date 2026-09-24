# app/modules/pagos/routes.py
"""
Rutas del flujo de pago con Mercado Pago. La forma más simple de
empezar es con "Checkout Pro": tu server crea una preferencia y
redirige al usuario al checkout alojado por MP.

Flujo completo (lo vas a armar vos):
  1. GET /pagos/checkout/<pedido_id>
     -> PagosService.crear_preferencia(pedido)
     -> redirigir al init_point que devuelve MP
  2. El usuario paga en el sitio de MP (con tarjetas de PRUEBA).
  3. MP redirige de vuelta a tu back_url: /success | /pending | /failure
     -> renderizar la vista correspondiente (guardar el mp_payment_id)
  4. MP también manda un Webhook POST a /pagos/webhook
     -> verificar/consultar el pago con payment().get() y actualizar la BD

El webhook (paso 4) es el que te deja el estado CORRECTO al final;
el back_url (paso 3) es solo UX para que el usuario vea el resultado.

Ruta de ejemplo para el webhook (adaptala):

    @pagos_bp.route('/webhook', methods=['POST'])
    def webhook():
        data = request.json or {}
        # MP manda: data['type'] == 'payment', data['data']['id'] == payment_id
        if data.get('type') == 'payment':
            payment_id = data['data']['id']
            PagosService.actualizar_estado_desde_mp(payment_id)
        return 'ok', 200   # SIEMPRE responder 200 para que MP no reenvíe

    @pagos_bp.route('/success')
    def success():
        return render_template('pagos/success.html', payment_id=request.args.get('payment_id'))

Para probar en local, los webhooks de MP necesitan una URL pública
(HTTPS). Usá ngrok: "ngrok http 5000" y poné la URL en MP_WEBHOOK_URL (.env).
"""
from flask import render_template, request
from . import pagos_bp

# placeholder: acá agregás las rutas reales. Este endpoint solo
# sirve para que el módulo tenga algo renderizable mientras lo armás.
@pagos_bp.route('/')
def index():
    return render_template('pagos/index.html')