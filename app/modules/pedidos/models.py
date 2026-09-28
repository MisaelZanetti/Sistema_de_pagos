from app.core.base_model import BaseModel
from app.extensions import db


class Pedido(BaseModel):
    __tablename__ = 'pedidos'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    total = db.Column(db.Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f'<Pedido {self.id} - {self.estado}>'


class ItemPedido(BaseModel):
    __tablename__ = 'item_pedido'
    __table_args__ = (
        db.UniqueConstraint('pedido_id', 'producto_id', name='uq_item_pedido'),
    )

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    def subtotal(self):
        return self.precio_unitario * self.cantidad

    def __repr__(self):
        return f'<ItemPedido {self.producto_id} x{self.cantidad}>'