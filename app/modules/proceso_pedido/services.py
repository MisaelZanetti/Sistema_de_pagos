# app/modules/proceso_pedido/services.py
"""
Capa de datos de la pantalla "Armar pedido".

Habla únicamente con los modelos del propio módulo: ProductoPedido
(productos que se ofrecen) e ItemCarrito (lo que el cliente ya eligió).
"""
from decimal import Decimal

from app.core.base_service import BaseService
from app.extensions import db
from .models import ItemCarrito, ProductoPedido


class ProcesoPedidoService(BaseService):
    model = ProductoPedido

    @classmethod
    def get_disponibles(cls):
        """Productos que se pueden agregar al pedido (con stock)."""
        return [p for p in cls.get_all() if p.stock > 0]

    @classmethod
    def get_carrito(cls, user_id):
        """Filas del carrito del usuario con su producto."""
        items = ItemCarrito.query.filter_by(user_id=user_id).order_by(ItemCarrito.id).all()
        return [{'item': i, 'producto': cls.get_by_id(i.producto_id)} for i in items]

    @classmethod
    def get_resumen(cls, user_id):
        """Todo lo que el aside necesita: filas, cantidades por producto,
        unidades y total."""
        filas = cls.get_carrito(user_id)
        cantidades = {f['item'].producto_id: f['item'].cantidad for f in filas}
        unidades = sum(cantidades.values())
        total = sum(
            (f['producto'].precio * f['item'].cantidad for f in filas),
            Decimal('0.00')
        )
        return filas, cantidades, unidades, total

    @classmethod
    def cambiar(cls, user_id, producto_id, delta):
        """Suma o resta unidades de un producto. Si la cantidad llega a
        cero, el producto sale del carrito."""
        item = ItemCarrito.query.filter_by(user_id=user_id, producto_id=producto_id).first()
        if item:
            item.cantidad += delta
            if item.cantidad <= 0:
                item.delete()
            else:
                db.session.commit()
        elif delta > 0:
            ItemCarrito(user_id=user_id, producto_id=producto_id, cantidad=delta).save()
        return cls.get_by_id(producto_id)

    @classmethod
    def quitar(cls, user_id, producto_id):
        """Saca un producto del carrito."""
        item = ItemCarrito.query.filter_by(user_id=user_id, producto_id=producto_id).first()
        if item:
            item.delete()

    @classmethod
    def vaciar(cls, user_id):
        """Vacía el carrito del usuario."""
        ItemCarrito.query.filter_by(user_id=user_id).delete()
        db.session.commit()