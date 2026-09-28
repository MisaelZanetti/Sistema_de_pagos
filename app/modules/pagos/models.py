from app.core.base_model import BaseModel
from app.extensions import db


class Pago(BaseModel):
    __tablename__ = 'pagos'

    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    mp_preference_id = db.Column(db.String(64), nullable=True)
    mp_payment_id = db.Column(db.Integer, nullable=True)
    mp_merchant_order_id = db.Column(db.String(64), nullable=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    status_detail = db.Column(db.String(64), nullable=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default='ARS')
    payment_method = db.Column(db.String(30), nullable=True)
    payer_email = db.Column(db.String(120), nullable=True)
    external_reference = db.Column(db.String(64), nullable=True, index=True)

    def __repr__(self):
        return f'<Pago {self.id} - {self.status}>'