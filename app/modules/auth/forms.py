from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


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
    submit = SubmitField('Crear cuenta')


class LoginForm(FlaskForm):
    username = StringField('Nombre', validators=[DataRequired(message='Ingresá tu nombre.')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Ingresá tu contraseña.')])
    submit = SubmitField('Ingresar')