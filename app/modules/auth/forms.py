from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

# Roles que se pueden asignar al registrar. 'admin' no está a propósito:
# solo se concede a mano en la base de datos.
ROLES = [
    ('cliente', 'Cliente'),
    ('empleado', 'Empleado'),
]


class RegisterForm(FlaskForm):
    username = StringField(
        'Nombre',
        validators=[
            DataRequired(message='Ingresá tu nombre.'),
            Length(min=3, max=80, message='El nombre debe tener entre 3 y 80 caracteres.')
        ]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='Ingresá una contraseña.'),
            Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
        ]
    )
    role = SelectField(
        'Rol',
        choices=ROLES,
        validators=[DataRequired(message='Elegí un rol.')]
    )
    submit = SubmitField('Crear cuenta')


class LoginForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired(message='Ingresá tu nombre.')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Ingresá tu contraseña.')])
    submit = SubmitField('Ingresar')