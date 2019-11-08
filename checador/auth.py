import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from checador.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.route('/register', methods=('GET', 'POST'))
@login_required
def register():
    # Validamos si el método fue POST
    if request.method == 'POST':
        # Igualamos las variables del formulario
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        nombre = request.form['nombre']
        ap_1 = request.form['ap_1']
        ap_2 = request.form['ap_2']
        
        db = get_db()
        error = None
        # Verificamos que no haya errores
        if not username:
            error = 'El usuario es requerido.'
        elif not password:
            error = 'El password es requerido.'
        elif not nombre:
            error = 'El nombre es requerido.'
        elif not ap_1:
            error = 'El primer apellido es requerido.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'El usuario "{}" ya se encuentra registrado.'.format(username)

        if error is None:
            # Si no hubo errores procedemos insertar la info en la base de datos
            db.execute(
                'INSERT INTO user (username, password, email, nombre, ap_1, ap_2)'
                ' VALUES (?, ?, ?, ?, ? ,?)', (username, 
                generate_password_hash(password), email, nombre, ap_1, ap_2)
            )
            db.commit()
            # Retornamos la vista para hacer login
            return redirect(url_for('auth.login'))
        flash(error)
    # Si el método no fue POST, regresamos el formulario de registro
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'La información proporcionada no es correcta.'
        elif not check_password_hash(user['password'], password):
            error = 'La información proporcionada no es correcta.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_loged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
