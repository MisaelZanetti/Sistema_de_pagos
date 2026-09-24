# app/modules/auth/routes.py
"""
Rutas del módulo auth. Las rutas (o "vistas") solo:
  1. reciben el request,
  2. validan con el formulario,
  3. delegan en el Service,
  4. redirigen o renderizan el template.

Agregá tus rutas con decoradores @auth_bp.route(...), por ejemplo:
  '/login'  -> GET/POST, valida LoginForm, AuthService.authenticate, login_user
  '/register' -> GET/POST, valida RegisterForm, AuthService.register
  '/logout' -> @login_required, logout_user
"""
from flask import render_template
from . import auth_bp


@auth_bp.route('/')
def index():
    return render_template('auth/index.html')