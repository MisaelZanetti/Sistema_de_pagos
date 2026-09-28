from decimal import Decimal

from app.core.base_service import BaseService
from app.extensions import db
from app.modules.productos.services import ProductosService
from .models import ItemPedido, Pedido


class PedidosService(BaseService):
    model = Pedido

    @classmethod
    def get_items(cls, pedido_id):
        return ItemPedido.query.filter_by(pedido_id=pedido_id).order_by(ItemPedido.id).all()

    @classmethod
    def recalcular_total(cls, pedido_id):
        items = cls.get_items(pedido_id)
        total = sum((item.precio_unitario * item.cantidad for item in items), Decimal('0.00'))
        pedido = cls.get_by_id(pedido_id)
        pedido.total = total
        db.session.commit()
        return pedido

    @classmethod
    def agregar_item(cls, pedido_id, producto_id, cantidad):
        item = ItemPedido.query.filter_by(pedido_id=pedido_id, producto_id=producto_id).first()
        if item:
            item.cantidad += cantidad
        else:
            producto = ProductosService.get_by_id(producto_id)
            item = ItemPedido(
                pedido_id=pedido_id,
                producto_id=producto_id,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )
            db.session.add(item)
        db.session.commit()
        return cls.recalcular_total(pedido_id)

    @classmethod
    def eliminar_item(cls, pedido_id, item_id):
        item = ItemPedido.query.get_or_404(item_id)
        item.delete()
        cls.recalcular_total(pedido_id)