# app/modules/pagos/__init__.py
"""
Blueprint del módulo pagos (Mercado Pago).

Vas a registrar acá TODOS los endpoints del flujo de pago:
- /pagos/checkout/<pedido_id>  -> crea la preferencia y redirige a MP
- /pagos/success | /pagos/pending | /pagos/failure -> back_urls de MP
- /pagos/webhook               -> notificaciones de MP (POST)
- /pagos/                      -> listar tus pagos
"""
from flask import Blueprint

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

from . import routes  # importa al final para evitar imports circulares