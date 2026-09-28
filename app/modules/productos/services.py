from app.core.base_service import BaseService
from .models import Producto


class ProductosService(BaseService):
    model = Producto