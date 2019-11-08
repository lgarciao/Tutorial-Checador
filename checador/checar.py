from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash
from checador.db import get_db

bp = Blueprint('checar', __name__)


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        ultima_checada = None
        if username is None:
            error = 'El usuario es requerido.'
        elif password is None:
            error = 'La contraseña es requerida.'
        else:
            user = db.execute(
                'SELECT * FROM user WHERE username = ? AND baja = 0', (username,)
            ).fetchone()
            if user is None:
                error = 'El usuario no es correcto.'
            elif not check_password_hash(user['password'], password):
                error = 'La contraseña no es correcta.'
        
        if error is None:
            ultima_checada = db.execute(
                'SELECT * FROM checks'
                ' WHERE user_id = ?'
                    ' AND date(checa_entrada) = date("now", "localtime")'
                    ' AND baja = 0'
                    ' AND checa_salida IS NULL'
                ' ORDER BY checa_entrada DESC', (user['id'],)
            ).fetchone()
            if ultima_checada is not None:
                # El usuario ya registró entrada
                db.execute(
                    'UPDATE checks'
                    ' SET checa_salida = datetime(CURRENT_TIMESTAMP, "localtime")'
                    ' WHERE id = ?', (ultima_checada['id'],)
                )
            else:
                # El usuario no tiene una entrada
                db.execute(
                    'INSERT INTO checks (user_id)'
                    ' VALUES (?)', (user['id'],)
                )
            db.commit()
        else:
            flash(error)      
    checadas = db.execute(
        'SELECT u.username, time(c.checa_entrada) as checa_entrada,'
            ' time(c.checa_salida) as checa_salida'
        ' FROM checks c'
        ' JOIN user u ON c.user_id = u.id'
        ' WHERE date(c.checa_entrada) = date("now", "localtime")'
            ' or date(c.checa_salida) = date("now", "localtime")'
            ' and c.baja = 0'
    ).fetchall()
    return render_template('checar/index.html', checadas=checadas)
