"""
Script para crear la base de datos del proyecto.

Toma la URI de conexión que la app ya usa en desarrollo
(app/config.py -> SQLALCHEMY_DATABASE_URI), se conecta al servidor
MySQL y ejecuta CREATE DATABASE IF NOT EXISTS con charset utf8mb4.

Uso:
    python create_db.py                 # crea la base de datos
    python create_db.py --tables        # crea la base de datos y las tablas
    python create_db.py --drop          # elimina la base de datos (cuidado)
"""
import sys

import pymysql
from sqlalchemy.engine import make_url

from app import create_app
from app.extensions import db

BACKEND_SOPORTADO = 'mysql'
CHARSET = 'utf8mb4'
COLLATE = 'utf8mb4_unicode_ci'


def obtener_url():
    app = create_app('development')
    url = make_url(app.config['SQLALCHEMY_DATABASE_URI'])
    return app, url


def crear_base_de_datos(url):
    params = {
        'host': url.host,
        'port': url.port or 3306,
        'user': url.username,
        'password': url.password,
        'charset': CHARSET,
    }
    database = url.database

    print(f"Conectando a MySQL en {params['host']}:{params['port']} "
          f"como usuario '{params['user']}'...")
    conexion = pymysql.connect(**params)
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{database}` "
                f"CHARACTER SET {CHARSET} COLLATE {COLLATE}"
            )
    finally:
        conexion.close()

    return database


def eliminar_base_de_datos(url):
    params = {
        'host': url.host,
        'port': url.port or 3306,
        'user': url.username,
        'password': url.password,
        'charset': CHARSET,
    }
    database = url.database

    print(f"Eliminando base de datos `{database}`...")
    conexion = pymysql.connect(**params)
    try:
        with conexion.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS `{database}`")
    finally:
        conexion.close()


def crear_tablas(app):
    with app.app_context():
        db.create_all()
    print("Tablas creadas correctamente (desde los modelos de SQLAlchemy).")


def main():
    try:
        app, url = obtener_url()
    except Exception as error:
        print(f"Error leyendo la configuración: {error}")
        sys.exit(1)

    if url.get_backend_name() != BACKEND_SOPORTADO:
        print(f"Este script sólo soporta MySQL. "
              f"Backend detectado: {url.get_backend_name()}")
        sys.exit(1)

    try:
        if '--drop' in sys.argv:
            eliminar_base_de_datos(url)
            print("Base de datos eliminada.")
            return
        database = crear_base_de_datos(url)
        print(f"Base de datos '{database}' lista (creada o ya existía).")
        if '--tables' in sys.argv:
            crear_tablas(app)
    except Exception as error:
        print(f"No se pudo crear la base de datos: {error}")
        print("Verificá que MySQL esté corriendo y que las credenciales de "
              "app/config.py sean correctas.")
        sys.exit(1)


if __name__ == '__main__':
    main()