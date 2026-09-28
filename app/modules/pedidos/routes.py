from decimal import Decimal

from flask import flash, redirect, render_template, url_for
from app.modules.auth.services import AuthService
from app.modules.productos.services import ProductosService

from . import pedidos_bp
from .forms import EstadoForm, ItemPedidoForm, PedidoForm
from .services import PedidosService


@pedidos_bp.route('/')
def index():
    pedidos = PedidosService.get_all()
    filas = [{'pedido': p, 'usuario': AuthService.get_by_id(p.user_id).username} for p in pedidos]
    return render_template('pedidos/index.html', filas=filas)


@pedidos_bp.route('/nuevo', methods=['GET', 'POST'])
def crear():
    form = PedidoForm()
    form.usuario.choices = [(u.id, u.username) for u in AuthService.get_all()]
    if form.validate_on_submit():
        PedidosService.create(
            user_id=form.usuario.data,
            estado=form.estado.data,
            total=Decimal('0.00')
        )
        flash('Pedido creado.', 'success')
        return redirect(url_for('pedidos.index'))
    return render_template('pedidos/form.html', form=form)


@pedidos_bp.route('/<int:pedido_id>')
def detalle(pedido_id):
    pedido = PedidosService.get_by_id(pedido_id)
    items = [
        {'item': item, 'producto': ProductosService.get_by_id(item.producto_id)}
        for item in PedidosService.get_items(pedido_id)
    ]
    item_form = ItemPedidoForm()
    item_form.producto.choices = [(p.id, p.nombre) for p in ProductosService.get_all()]
    estado_form = EstadoForm()
    estado_form.estado.data = pedido.estado
    return render_template(
        'pedidos/detalle.html',
        pedido=pedido,
        items=items,
        item_form=item_form,
        estado_form=estado_form
    )


@pedidos_bp.route('/<int:pedido_id>/agregar_item', methods=['POST'])
def agregar_item(pedido_id):
    form = ItemPedidoForm()
    form.producto.choices = [(p.id, p.nombre) for p in ProductosService.get_all()]
    if form.validate_on_submit():
        PedidosService.agregar_item(pedido_id, form.producto.data, form.cantidad.data or 1)
        flash('Item agregado al pedido.', 'success')
    return redirect(url_for('pedidos.detalle', pedido_id=pedido_id))


@pedidos_bp.route('/<int:pedido_id>/estado', methods=['POST'])
def cambiar_estado(pedido_id):
    form = EstadoForm()
    if form.validate_on_submit():
        PedidosService.update(pedido_id, estado=form.estado.data)
        flash('Estado actualizado.', 'success')
    return redirect(url_for('pedidos.detalle', pedido_id=pedido_id))


@pedidos_bp.route('/<int:pedido_id>/item/<int:item_id>/eliminar', methods=['POST'])
def eliminar_item(pedido_id, item_id):
    PedidosService.eliminar_item(pedido_id, item_id)
    flash('Item eliminado.', 'info')
    return redirect(url_for('pedidos.detalle', pedido_id=pedido_id))


@pedidos_bp.route('/<int:pedido_id>/eliminar', methods=['POST'])
def eliminar(pedido_id):
    PedidosService.delete(pedido_id)
    flash('Pedido eliminado.', 'info')
    return redirect(url_for('pedidos.index'))