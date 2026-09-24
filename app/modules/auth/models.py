# app/modules/auth/models.py
"""
Modelos del módulo auth.

User hereda de BaseModel (id + timestamps) y de UserMixin (flask_login),
que le da las propiedades que Flask-Login necesita (is_authenticated,
is_active, is_anonymous, get_id).

El user_loader se registra acá para que Flask-Login sepa cómo cargar
un usuario a partir del id guardado en la sesión. Sin esto, cualquier
página que renderice una plantilla (que expone current_user) tira
"Missing user_loader or request_loader".
"""
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.core.base_model import BaseModel
from app.extensions import db, login_manager


class User(BaseModel, UserMixin):
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), default='cliente')

    def set_password(self, password):
        """Hashea y guarda la contraseña (nunca guardar en texto plano)."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Compara la contraseña contra el hash guardado."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la sesión; user_id viene como str del cookie."""
    return db.session.get(User, int(user_id))