# app/modules/pedidos/models.py
"""
Modelos del módulo pedidos (la orden de compra que después se paga).

Sugerencia: heredá de BaseModel (app/core/base_model.py).

    from app.extensions import db
    from app.core.base_model import BaseModel

    class Pedido(BaseModel):
        __tablename__ = 'pedidos'

        # usuario que compra (FK a User) y estado del pedido
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        estado = db.Column(db.String(20), default='pendiente')
        # 'pendiente' | 'pagado' | 'cancelado' | 'error'

        # Total no se calcula en la BD: se arma desde los items
        # y se guarda el total en el momento (Pago.amount lo usa).
        total = db.Column(db.Numeric(10, 2), nullable=False)
        # Si hacés Producto, linkeá con una tabla intermedia detalle:
        #   items = db.relationship('ItemPedido', backref='pedido', lazy=True)

    # La relación con Pago va por FK en 'pagos' (pedido_id) o acá como
    # pedido.pago = db.relationship('Pago', uselist=False, backref='pedido')
"""