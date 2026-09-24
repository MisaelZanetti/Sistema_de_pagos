# app/modules/productos/__init__.py
"""
Blueprint del módulo productos (catálogo).
"""
from flask import Blueprint

productos_bp = Blueprint('productos', __name__, url_prefix='/productos')

from . import routes  # importa al final para evitar imports circulares