from app.core.base_model import BaseModel
from app.extensions import db


class Producto(BaseModel):
    __tablename__ = 'productos'

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Producto {self.nombre}>'