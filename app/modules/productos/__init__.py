from flask import Blueprint

productos_bp = Blueprint('productos', __name__, url_prefix='/admin/productos')

from . import routes
from . import models