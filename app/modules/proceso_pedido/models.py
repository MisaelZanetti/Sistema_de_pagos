# app/modules/proceso_pedido/models.py
"""
Modelos propios del módulo "Armar pedido".

- ProductoPedido: los productos que el index ofrece para armar el pedido.
  Mapea la tabla `productos` (el módulo productos ya la declara, así que
  se reutiliza esa definición) para leer los datos reales sin importar
  el modelo del otro módulo.
- ItemCarrito: lo que el cliente tieneArmando en este momento. Es el
  carrito de la pantalla, separado de los pedidos que gestiona admin.
"""
from app.core.base_model import BaseModel
from app.extensions import db


class ProductoPedido(BaseModel):
    __tablename__ = 'productos'
    __table_args__ = {'extend_existing': True}

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<ProductoPedido {self.nombre}>'


class ItemCarrito(BaseModel):
    __tablename__ = 'items_carrito'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'producto_id', name='uq_items_carrito'),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f'<ItemCarrito user={self.user_id} producto={self.producto_id} x{self.cantidad}>'