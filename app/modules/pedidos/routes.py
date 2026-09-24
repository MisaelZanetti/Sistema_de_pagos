from flask import render_template
from . import pedidos_bp


@pedidos_bp.route('/')
def index():
    return render_template('pedidos/index.html')