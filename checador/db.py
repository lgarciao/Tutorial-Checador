import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

def get_db():
    # Crea conexión a la base de datos
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    # Cierra la base de datos
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    # Inicializa la BD
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_user():
    # Creamos el usuario admin
    db = get_db()
    db.execute(
        'INSERT INTO user ( username, password, nombre, ap_1 )'
        ' VALUES ( ?, ?, ?, ? )', ('admin', generate_password_hash('admin'), 'Administrador', 'Del Sistema'))
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    '''Borra la información existente y crea nuevas tablas.'''
    init_db()
    click.echo('Base de datos inicializada...')
    init_user()
    click.echo('Usuario "admin" creado.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
