from flask import render_template
from . import productos_bp


@productos_bp.route('/')
def index():
    return render_template('productos/index.html')