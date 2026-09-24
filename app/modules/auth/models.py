# app/modules/auth/models.py
"""
Modelos del módulo auth. Creá acá la clase User.

Sugerencia: heredá de BaseModel (app/core/base_model.py) y de
UserMixin (flask_login), y registrá el user_loader:

    from flask_login import UserMixin
    from werkzeug.security import generate_password_hash, check_password_hash
    from app.extensions import db, login_manager
    from app.core.base_model import BaseModel

    class User(BaseModel, UserMixin):
        __tablename__ = 'users'
        # campos: email (único), password_hash, first_name, last_name, role...
        # métodos: set_password(password), check_password(password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
"""