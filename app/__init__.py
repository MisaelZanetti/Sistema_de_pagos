from flask import Flask, redirect, url_for
from app.config import config
from app.extensions import db, login_manager, migrate, csrf


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.modules.auth import auth_bp
    from app.modules.pagos import pagos_bp
    from app.modules.productos import productos_bp
    from app.modules.pedidos import pedidos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(pagos_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(pedidos_bp)

    @app.route('/')
    def index():
        # Mientras no exista el módulo auth, manda directo a pagos.
        # Cuando armes login, acá podés redirigir según autenticación.
        return redirect(url_for('pagos.index'))

    return app