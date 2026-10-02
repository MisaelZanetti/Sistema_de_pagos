# app/modules/vista_productos/routes.py
"""
Vista pública del catálogo: muestra los productos sin pedir sesión.
El alta y la edición de productos viven en el módulo productos (/admin/productos).
"""
from flask import jsonify, render_template

from . import vista_productos_bp
from .services import CatalogoService


@vista_productos_bp.route('/')
def index():
    productos = CatalogoService.get_all()
    precio_max = max((p['price'] for p in productos), default=0)
    return render_template(
        'vistas_productos/index.html',
        productos=productos,
        total=len(productos),
        precio_max=int(precio_max)
    )