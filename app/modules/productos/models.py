from app.core.base_model import BaseModel
from app.extensions import db


class Producto(BaseModel):
    __tablename__ = 'productos'
    # La tabla también la declara el módulo proceso_pedido (ProductoPedido).
    # extend_existing permite las dos declaraciones sin depender del orden
    # en que se importen los módulos.
    __table_args__ = {'extend_existing': True}

    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Producto {self.nombre}>'