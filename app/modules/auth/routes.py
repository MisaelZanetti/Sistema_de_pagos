# app/modules/auth/routes.py
"""
Rutas del módulo auth: register, login y logout.
"""
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from . import auth_bp
from .forms import LoginForm, RegisterForm
from .services import AuthService, ROLE_POR_DEFECTO


@auth_bp.route('/')
def index():
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        # Solo un admin puede elegir el rol; el resto se registra como cliente.
        if current_user.is_authenticated and current_user.role == 'admin':
            role = form.role.data
        else:
            role = ROLE_POR_DEFECTO

        user, error = AuthService.register(
            form.username.data.strip(),
            form.password.data,
            role
        )
        if error:
            flash(error, 'danger')
        else:
            flash(f'Cuenta "{user.username}" creada.', 'success')
            return redirect(url_for('home.index'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = AuthService.authenticate(
            form.username.data.strip(),
            form.password.data
        )
        if user:
            login_user(user)
            flash(f'¡Hola de nuevo, {user.username}!', 'success')
            return redirect(url_for('home.index'))
        flash('Nombre o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Cerraste tu sesión.', 'info')
    return redirect(url_for('home.index'))