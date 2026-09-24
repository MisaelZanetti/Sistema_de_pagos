# app/modules/pedidos/services.py
"""
Servicios del módulo pedidos. Acá va la lógica de crear un pedido:
calcular el total desde los productos, chequear stock, cambiar de
estado cuando el pago se aprueba (desde el webhook de pagos).

    from app.core.base_service import BaseService
    from .models import Pedido

    class PedidoService(BaseService):
        model = Pedido

        # @classmethod
        # def crear_desde_productos(cls, user_id, items):  # [(producto_id, cantidad)]
        #     # validar stock, calcular total, crear Pedido y sus items

        # @classmethod
        # def marcar_pagado(cls, pedido_id, ..., method_fee, total_paid):
        #     # estado = 'pagado', descontar stock, etc.
"""