# app/modules/home/routes.py
"""
Rutas de la pantalla de inicio.

Es la primera pantalla de la app (responde en / y en /home) y está
abierta a todos: el navbar se ocupa de ocultar los enlaces que
requieren sesión.
"""
from flask import render_template

from . import home_bp


@home_bp.route('/')
def index():
    return render_template('home/index.html')