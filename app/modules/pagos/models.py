# app/modules/pagos/models.py
"""
Modelo del módulo pagos. Acá guardás el registro local de cada pago.

Sugerencia: heredá de BaseModel (app/core/base_model.py).

    from app.extensions import db
    from app.core.base_model import BaseModel

    class Pago(BaseModel):
        __tablename__ = 'pagos'

        pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
        mp_preference_id = db.Column(db.String(64))   # id de la preferencia en MP
        mp_payment_id = db.Column(db.Integer)         # id del payment real en MP
        mp_merchant_order_id = db.Column(db.String(64))  # id de la orden en MP
        status = db.Column(db.String(20), default='pending')  # pending/approved/rejected...
        status_detail = db.Column(db.String(64))
        amount = db.Column(db.Numeric(10, 2), nullable=False)
        currency = db.Column(db.String(3), default='ARS')
        payment_method = db.Column(db.String(30))
        payer_email = db.Column(db.String(120))
        external_reference = db.Column(db.String(64), index=True)  # con esto identificás el pago

        # podés sumar relación: pedido = db.relationship('Pedido', backref='pagos')

Nota: "external_reference" es CLAVE para el webhook: MP la devuelve
en cada notificación y te permite mapear el pago a tu Pago/Pedido local.
"""