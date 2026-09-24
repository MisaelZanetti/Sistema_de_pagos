# app/modules/auth/routes.py
"""
Rutas del módulo auth: register, login y logout.
"""
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import auth_bp
from .forms import LoginForm, RegisterForm
from .services import AuthService


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('pagos.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user, error = AuthService.register(
            form.username.data.strip(),
            form.password.data
        )
        if error:
            flash(error, 'danger')
        else:
            login_user(user)
            flash(f'¡Bienvenido, {user.username}! Tu cuenta fue creada.', 'success')
            return redirect(url_for('pagos.index'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('pagos.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate(
            form.username.data.strip(),
            form.password.data
        )
        if user:
            login_user(user)
            flash(f'¡Hola de nuevo, {user.username}!', 'success')
            return redirect(url_for('pagos.index'))
        flash('Nombre o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cerraste tu sesión.', 'info')
    return redirect(url_for('auth.login'))