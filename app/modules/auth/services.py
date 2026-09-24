from app.core.base_service import BaseService
from app.extensions import db
from .models import User


class AuthService(BaseService):
    model = User

    @classmethod
    def register(cls, username, password):
        if cls.model.query.filter_by(username=username).first():
            return None, 'Ya existe una cuenta con ese nombre.'

        user = User(username=username)
        user.set_password(password)
        user.save()
        return user, None

    @classmethod
    def authenticate(cls, username, password):
        user = cls.model.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None