# app/modules/vista_productos/routes.py
"""
Vista pública del catálogo: muestra los productos sin pedir sesión.
El alta y la edición de productos viven en el módulo productos (/admin/productos).
"""
from flask import render_template

from . import vista_productos_bp


@vista_productos_bp.route('/')
def index():
    return render_template('vistas_productos/index.html')
