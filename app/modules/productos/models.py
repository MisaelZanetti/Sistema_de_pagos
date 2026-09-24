# app/modules/productos/models.py
"""
Modelo del módulo productos. Creá acá la clase Producto.

Sugerencia: heredá de BaseModel (app/core/base_model.py).

    from app.extensions import db
    from app.core.base_model import BaseModel

    class Producto(BaseModel):
        __tablename__ = 'productos'

        nombre = db.Column(db.String(120), nullable=False)
        descripcion = db.Column(db.Text)
        precio = db.Column(db.Numeric(10, 2), nullable=False)  # siempre Decimal
        stock = db.Column(db.Integer, default=0)
        imagen = db.Column(db.String(255), nullable=True)
        activo = db.Column(db.Boolean, default=True)

Nota: usar Numeric (Decimal) para precios, NUNCA Float — los floats
rompen cálculos de dinero.
"""