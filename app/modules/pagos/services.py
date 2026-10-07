import mercadopago
from flask import current_app, url_for
from decimal import Decimal
from app.modules.pedidos.services import PedidosService
from app.extensions import db
from .models import Pago


def url_absoluta(endpoint):
    """Arma la URL pública completa a partir del endpoint de Flask."""
    base = current_app.config['APP_BASE_URL'].rstrip('/')
    return base + url_for(endpoint)


class PagosService:

    @staticmethod
    def _sdk():
        return mercadopago.SDK(current_app.config['MP_ACCESS_TOKEN'])

    @classmethod
    def crear_preferencia(cls, pedido, items):
        """
        items: lista de dicts [{'title': str, 'quantity': int, 'unit_price': Decimal}]
        Devuelve (init_point, pago) y deja un Pago 'pending' guardado.
        """
        preference_data = {
            'items': [
                {
                    'title': i['title'],
                    'quantity': int(i['quantity']),
                    'unit_price': float(i['unit_price']),
                    'currency_id': 'ARS',
                }
                for i in items
            ],
            'external_reference': str(pedido.id),
            'back_urls': {
                'success': url_absoluta('pagos.exito'),
                'pending': url_absoluta('pagos.pendiente'),
                'failure': url_absoluta('pagos.fallo'),
            },
            'auto_return': 'approved',
            'notification_url': current_app.config['MP_WEBHOOK_URL'],
            'payment_methods': {'excluded_payment_types': [{'id': 'ticket'}]},
        }

        respuesta = cls._sdk().preference().create(preference_data)
        if respuesta['status'] not in (200, 201):
            raise RuntimeError(f"Error de Mercado Pago: {respuesta['response']}")

        data = respuesta['response']
        pago = Pago(
            pedido_id=pedido.id,
            mp_preference_id=data['id'],
            amount=pedido.total,
            external_reference=str(pedido.id),
        )
        pago.save()
        return data['init_point'], pago

    @classmethod
    def consultar_pago(cls, mp_payment_id):
        """Estado REAL del pago, consultado a MP (lo usa el webhook)."""
        respuesta = cls._sdk().payment().get(mp_payment_id)
        if respuesta['status'] != 200:
            return None
        return respuesta['response']

    @classmethod
    def registrar_retorno(cls, external_reference, payment_id, merchant_order_id):
        """
        Guarda los ids que MP manda en la back_url. Es solo para UX:
        NO cambia el estado, eso lo hace el webhook.
        """
        if not external_reference:
            return None
        pago = (Pago.query
                .filter_by(external_reference=external_reference)
                .order_by(Pago.id.desc())
                .first())
        if not pago:
            return None
        if payment_id and payment_id.isdigit() and not pago.mp_payment_id:
            pago.mp_payment_id = int(payment_id)
        if merchant_order_id and not pago.mp_merchant_order_id:
            pago.mp_merchant_order_id = merchant_order_id
        db.session.commit()
        return pago

    @classmethod
    def actualizar_estado_desde_mp(cls, mp_payment_id):
        """
        Consulta el pago real a MP y actualiza el Pago y el Pedido locales.
        Es idempotente: MP puede avisar varias veces del mismo pago.
        """
        datos = cls.consultar_pago(mp_payment_id)
        if not datos:
            return None

        referencia = datos.get('external_reference')  # = id del pedido
        if not referencia:
            return None

        pago = (Pago.query.filter_by(mp_payment_id=int(mp_payment_id)).first()
                or Pago.query.filter_by(external_reference=referencia)
                .order_by(Pago.id.desc()).first())
        if not pago:
            return None

        estado_mp = datos.get('status')
        pago.mp_payment_id = int(mp_payment_id)
        pago.status = estado_mp
        pago.status_detail = datos.get('status_detail')
        pago.payment_method = datos.get('payment_method_id')
        pago.payer_email = (datos.get('payer') or {}).get('email')
        db.session.commit()

        pedido = PedidosService.get_by_id(int(referencia))

        if estado_mp == 'approved' and pedido.estado == 'pendiente':
            monto = Decimal(str(datos.get('transaction_amount', 0)))
            if monto == pedido.total:
                PedidosService.update(pedido.id, estado='pagado')
            else:
                PedidosService.update(pedido.id, estado='error')
        elif estado_mp == 'cancelled' and pedido.estado == 'pendiente':
            PedidosService.update(pedido.id, estado='cancelado')

        return pago