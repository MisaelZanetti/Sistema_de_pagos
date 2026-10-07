from decimal import Decimal

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.modules.pedidos.services import PedidosService

from . import proceso_pedido_bp
from .services import ProcesoPedidoService


@proceso_pedido_bp.route('/')
@login_required
def index():
    productos = ProcesoPedidoService.get_disponibles()
    carrito, cantidades, unidades, total = ProcesoPedidoService.get_resumen(current_user.id)
    return render_template(
        'proceso_pedido/index.html',
        productos=productos,
        carrito=carrito,
        cantidades=cantidades,
        unidades=unidades,
        total=total
    )


@proceso_pedido_bp.route('/agregar', methods=['POST'])
@login_required
def agregar():
    """Suma (delta 1) o resta unidades de un producto del carrito."""
    producto_id = request.form.get('producto_id', type=int)
    delta = request.form.get('delta', default=1, type=int)
    producto = ProcesoPedidoService.cambiar(current_user.id, producto_id, delta)
    flash(f'{producto.nombre}: {delta:+d} unidad(es) en el pedido.', 'success')
    return redirect(url_for('proceso_pedido.index'))


@proceso_pedido_bp.route('/quitar', methods=['POST'])
@login_required
def quitar():
    producto_id = request.form.get('producto_id', type=int)
    producto = ProcesoPedidoService.get_by_id(producto_id)
    ProcesoPedidoService.quitar(current_user.id, producto_id)
    flash(f'{producto.nombre} quitado del pedido.', 'info')
    return redirect(url_for('proceso_pedido.index'))


@proceso_pedido_bp.route('/vaciar', methods=['POST'])
@login_required
def vaciar():
    ProcesoPedidoService.vaciar(current_user.id)
    flash('Pedido vaciado.', 'info')
    return redirect(url_for('proceso_pedido.index'))


@proceso_pedido_bp.route('/confirmar', methods=['POST'])
@login_required
def confirmar():
    carrito, *_ = ProcesoPedidoService.get_resumen(current_user.id)
    if not carrito:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('proceso_pedido.index'))

    pedido = PedidosService.create(
        user_id=current_user.id,
        estado='pendiente',
        total=Decimal('0.00')
    )

    for fila in carrito:
        PedidosService.agregar_item(
            pedido.id,
            fila['item'].producto_id,
            fila['item'].cantidad
        )

    ProcesoPedidoService.vaciar(current_user.id)

    return redirect(url_for('pagos.checkout', pedido_id=pedido.id))