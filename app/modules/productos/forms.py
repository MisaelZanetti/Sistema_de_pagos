# app/modules/productos/forms.py
"""
Formularios del módulo productos. Creá acá un formulario para crear/editar.

    from flask_wtf import FlaskForm
    from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SubmitField
    from wtforms.validators import DataRequired, NumberRange

    class ProductoForm(FlaskForm):
        nombre = StringField('Nombre', validators=[DataRequired()])
        descripcion = TextAreaField('Descripción')
        precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
        stock = IntegerField('Stock', validators=[NumberRange(min=0)])
        submit = SubmitField('Guardar')
"""