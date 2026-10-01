from flask import Blueprint

pedidos_bp = Blueprint('pedidos', __name__, url_prefix='/admin/pedidos')

from . import routes
from . import models