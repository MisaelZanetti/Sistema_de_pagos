# app/modules/productos/routes.py
"""
Rutas del módulo productos (CRUD del catálogo).
"""
from flask import render_template
from . import productos_bp


@productos_bp.route('/')
def index():
    return render_template('productos/index.html')