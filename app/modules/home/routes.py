from flask import redirect, render_template, url_for
from flask_login import current_user

from . import home_bp


@home_bp.route('/')
def index():
    # Abierta a todos: los que no tienen sesión ven la pantalla de inicio,
    # los que ya están logueados entran directo al mercado de pagos.
    if current_user.is_authenticated:
        return redirect(url_for('pagos.index'))

    return render_template('home/index.html')
