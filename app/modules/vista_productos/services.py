# app/modules/vista_productos/services.py
"""
Capa de datos del catálogo público.

Lee los productos reales de la tabla `productos` y los traduce al
formato que espera catalogo.js. El modelo Producto solo tiene nombre,
descripcion, precio y stock, así que la categoría y la marca no se
inventan: el filtrado por categoría y marca queda deshabilitado y solo
precios, stock y búsqueda operate sobre datos ciertos.
"""
from app.modules.productos.services import ProductosService


class CatalogoService:

    @classmethod
    def get_all(cls):
        """Todos los productos listos para el catálogo."""
        return [cls._para_js(p) for p in cls._ordenados(ProductosService.get_all())]

    @classmethod
    def get_por_id(cls, producto_id):
        producto = ProductosService.get_by_id(producto_id)
        return cls._para_js(producto) if producto else None

    @classmethod
    def _ordenados(cls, productos):
        """Primero los que tienen stock, después por más caro."""
        return sorted(productos, key=lambda p: (p.stock <= 0, -float(p.precio)))

    @classmethod
    def _para_js(cls, producto):
        """Traduce un Producto al objeto plano que consume catalogo.js."""
        return {
            'id': producto.id,
            'name': producto.nombre,
            # Sin categoría ni marca en el modelo: se dejan vacías y los
            # filtros correspondientes se muestran deshabilitados.
            'brand': '',
            'category': '',
            'detail': producto.descripcion or '',
            'price': float(producto.precio),
            'previous': None,
            'visual': '',
            'tag': cls._etiqueta(producto),
            'stock': producto.stock > 0,
            'stock_count': producto.stock,
            'specs': [],
        }

    @staticmethod
    def _etiqueta(producto):
        if producto.stock <= 0:
            return 'Sin stock'
        return ''