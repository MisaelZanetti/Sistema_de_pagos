# 💳 Sistema de Pagos

> **Simulador de pago y cobro desarrollado con Python y Flask**, con gestión de usuarios, productos, pedidos y pagos mediante Mercado Pago en modo de prueba.

---

## 📌 Descripción

**Sistema de Pagos** es una aplicación web desarrollada con **Python y Flask** cuyo objetivo es simular el proceso completo de compra y pago de productos.

El sistema permite gestionar usuarios, productos y pedidos, además de generar pagos mediante **Mercado Pago en modo de prueba**, permitiendo comprobar diferentes estados de una operación sin realizar cobros reales.

El proyecto fue desarrollado como parte de una actividad práctica de desarrollo web con Flask, aplicando una estructura modular mediante **Blueprints**, separación de responsabilidades y persistencia de datos mediante **MySQL y SQLAlchemy**.

---

## 🎯 Objetivo del proyecto

El objetivo principal es desarrollar un simulador de pago/cobro que permita integrar los principales componentes de un sistema de comercio electrónico:

- 👤 Registro y autenticación de usuarios.
- 📦 Gestión de productos.
- 🛒 Creación y gestión de pedidos.
- 💳 Simulación de pagos.
- 🔄 Actualización del estado de los pedidos.
- 🗄️ Persistencia de información en una base de datos.
- 🔐 Validación y manejo de formularios.
- 🧩 Organización modular del proyecto.
- 💻 Interfaz web utilizando Flask y Jinja2.

---

## 🚀 Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| 🐍 **Python** | Lenguaje principal |
| 🌶️ **Flask** | Framework web |
| 🗄️ **MySQL** | Base de datos |
| 🔗 **SQLAlchemy** | ORM y manejo de modelos |
| 🔄 **Flask-Migrate** | Migraciones de base de datos |
| 🔐 **Flask-Login** | Autenticación de usuarios |
| 📝 **Flask-WTF** | Formularios y validaciones |
| 🎨 **HTML / CSS / JavaScript** | Interfaz de usuario |
| 🧩 **Jinja2** | Renderizado de plantillas |
| 💳 **Mercado Pago** | Simulación del proceso de pago |
| 🔧 **python-dotenv** | Manejo de variables de entorno |

---

# 🏗️ Arquitectura del proyecto

El proyecto utiliza una arquitectura modular basada en **Blueprints**, separando las diferentes responsabilidades de la aplicación.

```text
Sistema_de_pagos/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   │
│   ├── core/
│   │   ├── base_model.py
│   │   ├── base_service.py
│   │   └── utils.py
│   │
│   ├── modules/
│   │   ├── auth/
│   │   │   ├── models.py
│   │   │   ├── forms.py
│   │   │   ├── services.py
│   │   │   └── routes.py
│   │   │
│   │   ├── productos/
│   │   │   ├── models.py
│   │   │   ├── forms.py
│   │   │   ├── services.py
│   │   │   └── routes.py
│   │   │
│   │   ├── pedidos/
│   │   │   ├── models.py
│   │   │   ├── forms.py
│   │   │   ├── services.py
│   │   │   └── routes.py
│   │   │
│   │   └── pagos/
│   │       ├── models.py
│   │       ├── forms.py
│   │       ├── services.py
│   │       └── routes.py
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/
│
├── create_db.py
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### 🔄 Flujo de una petición

El proyecto busca mantener separada la lógica de cada capa:

```text
Usuario
   │
   ▼
URL / Route
   │
   ▼
Form (Flask-WTF)
   │
   ▼
Service
   │
   ▼
Model
   │
   ▼
Base de datos
   │
   ▼
Template / HTML
   │
   ▼
Usuario
```

De esta manera, las rutas se encargan principalmente de recibir las solicitudes y coordinar el proceso, mientras que la lógica de negocio se encuentra en los servicios.

---

# ✨ Funcionalidades

## 👤 Autenticación

El sistema permite:

- Registrar nuevos usuarios.
- Iniciar sesión.
- Cerrar sesión.
- Mantener la sesión del usuario.
- Proteger determinadas rutas mediante autenticación.

La autenticación se implementa utilizando **Flask-Login**.

---

## 📦 Gestión de productos

El sistema cuenta con un módulo destinado a la administración de productos.

Permite:

- Crear productos.
- Consultar productos.
- Modificar productos.
- Eliminar productos.
- Utilizar los productos para generar pedidos.

Los productos forman parte del flujo principal de compra.

---

## 🛒 Sistema de pedidos

Los usuarios pueden generar pedidos a partir de los productos disponibles.

El sistema permite trabajar con el ciclo de vida de un pedido:

```text
Producto
   ↓
Pedido
   ↓
Pago
   ↓
Estado del pedido
```

Los pedidos se encuentran relacionados con los usuarios y los productos correspondientes.

---

# 💳 Simulador de pagos

Una de las funcionalidades principales del proyecto es la integración con **Mercado Pago en modo de prueba**.

El flujo general es:

```text
Usuario
   │
   ▼
Selecciona productos
   │
   ▼
Genera pedido
   │
   ▼
Inicia el pago
   │
   ▼
Mercado Pago
   │
   ├── Pago aprobado
   ├── Pago pendiente
   └── Pago rechazado
          │
          ▼
Actualización del pedido
```

La aplicación utiliza las credenciales de prueba de Mercado Pago, por lo que **no se realizan cobros reales**.

---

## 🧪 Estados de prueba

Mercado Pago permite utilizar tarjetas de prueba para simular diferentes resultados.

| Resultado | Titular |
|---|---|
| ✅ Aprobado | `APRO` |
| 🟡 Pendiente | `CONT` |
| ❌ Rechazado | `OTHE` |

Estas operaciones se utilizan únicamente para comprobar el funcionamiento del simulador.

---

# 🗄️ Modelo de datos

La aplicación utiliza una base de datos relacional **MySQL**.

Los principales componentes del sistema son:

```text
┌─────────────┐
│    Usuario  │
└──────┬──────┘
       │
       │ 1:N
       ▼
┌─────────────┐
│    Pedido   │
└──────┬──────┘
       │
       │
       ▼
┌─────────────┐
│    Pago     │
└─────────────┘

       ▲
       │
       │ contiene
       │
┌──────┴──────┐
│  Producto   │
└─────────────┘
```

Las relaciones entre los modelos permiten mantener la información organizada y relacionar usuarios, pedidos, productos y pagos.

---

# ⚙️ Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/MisaelZanetti/Sistema_de_pagos.git
```

Ingresar a la carpeta:

```bash
cd Sistema_de_pagos
```

---

## 2. Crear un entorno virtual

En Windows:

```bash
python -m venv venv
```

Activar el entorno:

```bash
venv\Scripts\activate
```

En caso de utilizar PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

---

## 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

---

# 🗄️ Configuración de MySQL

Crear una base de datos llamada:

```text
sistema_pagos
```

Por ejemplo:

```sql
CREATE DATABASE sistema_pagos;
```

Luego configurar la conexión en el archivo `.env`.

> ⚠️ El archivo `.env` contiene información sensible y no debe subirse al repositorio.

---

# 🔐 Variables de entorno

El proyecto utiliza variables de entorno para configurar la aplicación.

Ejemplo:

```env
SECRET_KEY=tu_clave_secreta

DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost/sistema_pagos

MP_ACCESS_TOKEN=tu_access_token_de_prueba

MP_WEBHOOK_URL=tu_url_de_webhook
```

Las credenciales de Mercado Pago deben ser **credenciales de prueba**.

---

# 🔄 Migraciones

Una vez configurados los modelos y la base de datos, se pueden ejecutar las migraciones:

```bash
flask db init
```

Crear una migración:

```bash
flask db migrate -m "Creación de modelos"
```

Aplicar la migración:

```bash
flask db upgrade
```

---

# ▶️ Ejecutar el proyecto

Para iniciar la aplicación:

```bash
python run.py
```

Luego acceder desde el navegador a:

```text
http://localhost:5000
```

---

# 💳 Configuración de Mercado Pago

Para utilizar el simulador se deben configurar las **credenciales de prueba** de Mercado Pago.

El flujo utilizado por la aplicación es:

1. El usuario genera un pedido.
2. El sistema crea una preferencia de pago.
3. Mercado Pago devuelve el enlace de Checkout.
4. El usuario realiza una operación utilizando datos de prueba.
5. Mercado Pago informa el resultado.
6. El sistema actualiza el estado correspondiente.

Para probar los webhooks durante el desarrollo local puede utilizarse una herramienta de túnel como `ngrok`.

Ejemplo:

```bash
ngrok http 5000
```

La URL generada puede utilizarse para configurar el webhook de Mercado Pago.

---

# 📁 Organización de los módulos

Cada módulo sigue una estructura similar:

```text
module/
├── models.py
├── forms.py
├── services.py
└── routes.py
```

### `models.py`

Define los modelos y estructuras que representan los datos almacenados en la base de datos.

### `forms.py`

Contiene los formularios desarrollados con **Flask-WTF**, incluyendo validaciones de los datos ingresados por el usuario.

### `services.py`

Contiene la lógica de negocio del módulo.

Por ejemplo:

- Crear usuarios.
- Crear pedidos.
- Gestionar productos.
- Procesar operaciones de pago.

### `routes.py`

Define las rutas del módulo y conecta las solicitudes HTTP con los formularios, servicios y templates.

---

# 🧩 Principales módulos

### 🔐 Auth

Responsable de:

- Registro.
- Inicio de sesión.
- Cierre de sesión.
- Gestión de la sesión del usuario.

### 📦 Productos

Responsable de:

- Alta de productos.
- Modificación.
- Eliminación.
- Consulta.

### 🛒 Pedidos

Responsable de:

- Crear pedidos.
- Asociar productos.
- Gestionar estados.
- Relacionar pedidos con usuarios.

### 💳 Pagos

Responsable de:

- Crear preferencias de pago.
- Comunicarse con Mercado Pago.
- Procesar respuestas.
- Actualizar el estado del pago.
- Gestionar webhooks.

---

# 📚 Documentación utilizada

- [Flask](https://flask.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/)
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/)
- [Mercado Pago Developers](https://www.mercadopago.com.ar/developers)

---

# 👨‍💻 Autor

**Misael Zanetti**

Proyecto desarrollado como trabajo práctico de desarrollo web utilizando **Python + Flask**.

---

## 📄 Licencia

Este proyecto se encuentra bajo la licencia incluida en el repositorio.