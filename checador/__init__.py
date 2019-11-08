import os 
from flask import Flask

def create_app(test_config=None):
    # Crea y configura la app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'checa.sqlite'),
    )

    if test_config is None:
        # Carga la instancia config.py
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # Nos aseguramos que exista la carpeta instance
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Registramos la función init_app
    from . import db
    db.init_app(app)

    # Registramos nuestro Blueprint
    from . import auth
    app.register_blueprint(auth.bp)

    from . import checar
    app.register_blueprint(checar.bp)
    app.add_url_rule('/', endpoint='index')

    return app
