# Configuración por entorno
"""
Configuración por entorno. Usamos el patrón de clases que
recomienda la propia documentación de Flask para no repetir
config entre desarrollo/testing/producción.
"""
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(basedir, '..'))
load_dotenv(os.path.join(project_root, '.env'))


class Config:
    """Config base: lo que comparten todos los entornos."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-provisoria-cambiar-en-.env')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB máx por archivo subido

    # --- Mercado Pago ---
    # Access Token + Public Key se sacan de las credenciales de TU app.
    # Para simular pagos usá siempre las credenciales de prueba (TEST-...).
    MP_ACCESS_TOKEN = os.environ.get('MP_ACCESS_TOKEN')
    MP_PUBLIC_KEY = os.environ.get('MP_PUBLIC_KEY')
    # URL pública que recibe los webhooks de Mercado Pago
    MP_WEBHOOK_URL = os.environ.get(
        'MP_WEBHOOK_URL', 'http://localhost:5000/pagos/webhook'
    )
    # URL base del sitio (para los back_urls de la preferencia)
    APP_BASE_URL = os.environ.get('APP_BASE_URL', 'http://localhost:5000')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:Alvlgeddl09*@localhost/sistema_pagos'
    )


class TestingConfig(Config):
    TESTING = True
    # SQLite en memoria para tests: rápido y no ensucia la BDD real
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False  # simplifica los tests de formularios


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}