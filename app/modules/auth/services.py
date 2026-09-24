# app/modules/auth/services.py
"""
Servicios del módulo auth. Las rutas NUNCA tocan User ni db.session
directo: toda la lógica va acá.

    from app.core.base_service import BaseService
    from .models import User

    class AuthService(BaseService):
        model = User

        @classmethod
        def register(cls, first_name, last_name, email, password):
            # validar que el email no exista, crear User, hashear password
            ...

        @classmethod
        def authenticate(cls, email, password):
            # devolver User si la password coincide, si no None
            ...
"""