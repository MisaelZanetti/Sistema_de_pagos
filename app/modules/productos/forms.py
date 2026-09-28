from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message='Ingresá el nombre.'),
            Length(max=120, message='El nombre no puede superar los 120 caracteres.')
        ]
    )
    descripcion = TextAreaField(
        'Descripción',
        validators=[Length(max=2000, message='La descripción es demasiado larga.')]
    )
    precio = DecimalField(
        'Precio',
        places=2,
        validators=[
            DataRequired(message='Ingresá el precio.'),
            NumberRange(min=0, message='El precio no puede ser negativo.')
        ]
    )
    stock = IntegerField(
        'Stock',
        default=0,
        validators=[NumberRange(min=0, message='El stock no puede ser negativo.')]
    )
    submit = SubmitField('Guardar')