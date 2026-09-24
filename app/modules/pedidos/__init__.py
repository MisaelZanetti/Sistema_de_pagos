# app/modules/pedidos/__init__.py
"""
Blueprint del módulo pedidos (orden de compra).
"""
from flask import Blueprint

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')

from . import routes  # importa al final para evitar imports circulares