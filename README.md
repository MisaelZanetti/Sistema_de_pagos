# Sistema_de_pagos

Simulador de pagos con Mercado Pago. Flask + Blueprints, estructura basada en `aula_virtual`.

## Estructura

```
Sistema_de_pagos/
├── run.py                  # Punto de entrada: python run.py
├── requirements.txt
├── .env                    # SECRET_KEY, DATABASE_URL, credenciales MP
└── app/
    ├── __init__.py         # create_app(): registra config, extensions y blueprints
    ├── config.py           # Config por entorno + variables de Mercado Pago
    ├── extensions.py       # db, login_manager, migrate, csrf
    ├── core/
    │   ├── base_model.py   # BaseModel: id + created_at/updated_at + save()/delete()
    │   ├── base_service.py # BaseService: get_by_id, get_all, create, update, delete
    │   └── utils.py        # helpers reutilizables (vacíos por ahora)
    ├── modules/
    │   ├── auth/           # Blueprint /auth  (models, forms, services, routes)
    │   ├── pagos/          # Blueprint /pagos -> MERCADO PAGO
    │   ├── productos/      # Blueprint /productos
    │   └── pedidos/        # Blueprint /pedidos
    ├── static/             # CSS/JS/imágenes
    └── templates/          # base.html + una carpeta por módulo
```

Cada módulo tiene 4 archivos: `models.py`, `forms.py`, `services.py`, `routes.py`.
Están vacíos a propósito: se completan en el desarrollo.

## Arrancar

1. Creá la base de datos MySQL `sistema_pagos` (una sola vez).
2. Completá `.env` (DATABASE_URL, SECRET_KEY, credenciales de MP de prueba).
3. Instalá dependencias:
   ```
   venv\Scripts\pip install -r requirements.txt
   ```
4. Migraciones (una vez tenés modelos escritos):
   ```
   venv\Scripts\flask db init
   venv\Scripts\flask db migrate -m "mensaje"
   venv\Scripts\flask db upgrade
   ```
5. Levantá:
   ```
   python run.py
   ```

## Flujo de trabajo (Models -> Services -> Routes -> Templates)

- **models.py**: definen las tablas (User, Producto, Pedido, Pago). Heredan de `BaseModel`.
- **services.py**: lógica de negocio (registrar usuario, armar pedido, hablar con Mercado Pago). Las rutas NUNCA usan `db.session` directo.
- **routes.py**: reciben el request de la URL, validan con el form, llaman al service y renderizan el template o redirigen.
- **forms.py**: validan y limpian la entrada del usuario (WTForms).
- **templates/**: HTML que el navegador renderiza (Jinja2).

Ciclo de una petición: `URL -> route -> form -> service -> model -> db -> template -> HTML`.

## Mercado Pago (modo test / Checkout Pro)

1. Credenciales en `https://developers.mercadopago.com` -> **Tu integración -> Credenciales de prueba** (`TEST-...`). Pegalas en `.env`.
2. El backend crea una **preferencia** (items, `external_reference`, `back_urls`, `notification_url`) con el access token.
3. MP devuelve un `init_point` -> redirigís al usuario.
4. El usuario paga en el sitio de MP con **tarjetas de prueba** (ver más abajo). Nunca se cobra de verdad.
5. MP devuelve al usuario a tu `success/pending/failure` Y manda un **webhook** (`POST /pagos/webhook`) a `notification_url`.
6. En el webhook consultás el pago real con `sdk.payment().get(id)` y actualizás la BD.

Para recibir webhooks en local usá `ngrok http 5000` y poné la URL en `MP_WEBHOOK_URL`.

### Tarjetas de prueba (Argentina, mastercard/visa)

| Resultado | Nro de tarjeta | Código | Nombre del titular |
|---|---|---|---|
| Aprobado | `5031 7554 7040 7308` | `123` | APRO |
| Pendiente | `5031 7554 7040 7308` | `123` | CONT |
| Rechazado | `5031 7554 7040 7308` | `123` | OTHE |

Cualquier fecha de vencimiento futura, DNI del titular `12345678`.