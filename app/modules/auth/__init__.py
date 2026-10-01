from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/admin/auth')

from . import routes
from . import models