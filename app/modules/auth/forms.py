# app/modules/auth/forms.py
"""
Formularios del módulo auth. Creá acá LoginForm y RegisterForm.

    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, SubmitField
    from wtforms.validators import DataRequired, Email, Length, EqualTo

    class LoginForm(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        password = PasswordField('Contraseña', validators=[DataRequired()])
        submit = SubmitField('Ingresar')
"""