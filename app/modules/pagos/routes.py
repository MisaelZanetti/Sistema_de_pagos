from flask import render_template, request
from . import pagos_bp

# placeholder: acá agregás las rutas reales. Este endpoint solo
# sirve para que el módulo tenga algo renderizable mientras lo armás.
@pagos_bp.route('/')
def index():
    return render_template('pagos/index.html')