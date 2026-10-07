from flask import render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
from app.extensions import csrf
from app.modules.pedidos.services import PedidosService
from app.modules.productos.services import ProductosService
from . import pagos_bp
from .services import PagosService


@pagos_bp.route('/')
@login_required
def index():
    return render_template('pagos/index.html')

@pagos_bp.route('/checkout/<int:pedido_id>')
@login_required
def checkout(pedido_id):
    pedido = PedidosService.get_by_id(pedido_id)

    # Solo el dueño del pedido puede pagarlo
    if pedido.user_id != current_user.id:
        abort(403)

    if pedido.estado != 'pendiente':
        flash('Este pedido ya no está pendiente de pago.', 'warning')
        return redirect(url_for('pedidos.index'))

    # Armamos los items para Mercado Pago desde los ItemPedido
    items = []
    for item in PedidosService.get_items(pedido_id):
        producto = ProductosService.get_by_id(item.producto_id)
        items.append({
            'title': producto.nombre,
            'quantity': item.cantidad,
            'unit_price': item.precio_unitario,
        })

    if not items:
        flash('El pedido no tiene productos.', 'warning')
        return redirect(url_for('pedidos.index'))

    try:
        init_point, _pago = PagosService.crear_preferencia(pedido, items)
    except RuntimeError as error:
        flash(str(error), 'danger')
        return redirect(url_for('pedidos.index'))

    return redirect(init_point)

def _retorno(template):
    """Lee lo que MP manda por query string y renderiza la vista."""
    payment_id = request.args.get('payment_id')
    pago = PagosService.registrar_retorno(
        request.args.get('external_reference'),
        payment_id,
        request.args.get('merchant_order_id'),
    )
    return render_template(template, pago=pago, payment_id=payment_id)


@pagos_bp.route('/exito')
def exito():
    return _retorno('pagos/exito.html')


@pagos_bp.route('/pendiente')
def pendiente():
    return _retorno('pagos/pendiente.html')


@pagos_bp.route('/fallo')
def fallo():
    return _retorno('pagos/fallo.html')

@pagos_bp.route('/webhook', methods=['POST'])
@csrf.exempt
def webhook():
    data = request.get_json(silent=True) or {}
    tipo = data.get('type') or request.args.get('type') or request.args.get('topic')
    payment_id = ((data.get('data') or {}).get('id')
                or request.args.get('data.id')
                or request.args.get('id'))

    if tipo == 'payment' and payment_id:
        try:
            PagosService.actualizar_estado_desde_mp(payment_id)
        except Exception:
            current_app.logger.exception('Error procesando webhook de MP')

    return 'ok', 200   # SIEMPRE 200 para que MP no reenvíe sin parar