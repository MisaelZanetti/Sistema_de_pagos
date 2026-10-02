from flask import Blueprint

proceso_pedido_bp = Blueprint('proceso_pedido', __name__, url_prefix='/proceso_pedido')

from . import models
from . import routes