from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange

ESTADOS = [
    ('pendiente', 'Pendiente'),
    ('pagado', 'Pagado'),
    ('cancelado', 'Cancelado'),
    ('error', 'Error'),
]


class PedidoForm(FlaskForm):
    usuario = SelectField('Usuario', coerce=int, validators=[DataRequired(message='Elegí un usuario.')])
    estado = SelectField('Estado', choices=ESTADOS, validators=[DataRequired()])
    submit = SubmitField('Crear pedido')


class ItemPedidoForm(FlaskForm):
    producto = SelectField('Producto', coerce=int, validators=[DataRequired(message='Elegí un producto.')])
    cantidad = IntegerField('Cantidad', default=1, validators=[NumberRange(min=1, message='La cantidad mínima es 1.')])
    submit = SubmitField('Agregar al pedido')


class EstadoForm(FlaskForm):
    estado = SelectField('Estado', choices=ESTADOS, validators=[DataRequired()])
    submit = SubmitField('Actualizar estado')