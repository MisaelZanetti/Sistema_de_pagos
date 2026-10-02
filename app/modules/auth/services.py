from app.core.base_service import BaseService
from .forms import ROLES
from .models import User

ROLES_VALIDOS = [valor for valor, _ in ROLES]
ROLE_POR_DEFECTO = 'cliente'


class AuthService(BaseService):
    model = User

    @classmethod
    def register(cls, username, password, role=ROLE_POR_DEFECTO):
        if cls.model.query.filter_by(username=username).first():
            return None, 'Ya existe una cuenta con ese nombre.'

        # Solo se aceptan los roles del formulario. Si alguien manipula el
        # POST para mandarse 'admin', se cae al rol por defecto.
        if role not in ROLES_VALIDOS:
            role = ROLE_POR_DEFECTO

        user = User(username=username, role=role)
        user.set_password(password)
        user.save()
        return user, None

    @classmethod
    def authenticate(cls, username, password):
        user = cls.model.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None