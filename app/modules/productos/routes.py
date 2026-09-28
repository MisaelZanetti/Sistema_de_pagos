from flask import flash, redirect, render_template, url_for
from flask_login import login_required
from . import productos_bp
from .forms import ProductoForm
from .services import ProductosService


@productos_bp.route('/')
@login_required
def index():
    productos = ProductosService.get_all()
    return render_template('productos/index.html', productos=productos)


@productos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear():
    form = ProductoForm()
    if form.validate_on_submit():
        ProductosService.create(
            nombre=form.nombre.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            precio=form.precio.data,
            stock=form.stock.data if form.stock.data is not None else 0
        )
        flash('Producto creado.', 'success')
        return redirect(url_for('productos.index'))
    return render_template('productos/form.html', form=form, titulo='Nuevo producto')


@productos_bp.route('/<int:producto_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(producto_id):
    producto = ProductosService.get_by_id(producto_id)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        ProductosService.update(
            producto_id,
            nombre=form.nombre.data.strip(),
            descripcion=form.descripcion.data.strip() if form.descripcion.data else None,
            precio=form.precio.data,
            stock=form.stock.data if form.stock.data is not None else 0
        )
        flash('Producto actualizado.', 'success')
        return redirect(url_for('productos.index'))
    return render_template('productos/form.html', form=form, titulo='Editar producto')


@productos_bp.route('/<int:producto_id>/eliminar', methods=['POST'])
@login_required
def eliminar(producto_id):
    ProductosService.delete(producto_id)
    flash('Producto eliminado.', 'info')
    return redirect(url_for('productos.index'))