from flask import Blueprint

vista_productos_bp = Blueprint('vista_productos', __name__, url_prefix='/productos')

from . import routes
from . import services