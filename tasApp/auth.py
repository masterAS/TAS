import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
engine = create_engine('sqlite:///tas_db.db', echo = True)
from sqlalchemy.orm import sessionmaker
from . import db_initialization as db
bp = Blueprint('auth', __name__, url_prefix='/auth')
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        db_session = sessionmaker(bind = engine)
        d_session = db_session()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif d_session.query(db.Users).filter(db.Users.username == username):
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user = db.Users(first_name = first_name, last_name= last_name, email = email, 
            username= username, password=generate_password_hash(password), phone= phone)
            d_session.add(user)
            session.commit()
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_session = sessionmaker(bind = engine)
        d_session = db_session()
        error = None
        user = d_session.query(db.Users).filter(db.Users.username == username).all()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[0].password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user[0].username
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db_session = sessionmaker(bind = engine)
        d_session = db_session()
        g.user = d_session.query(db.Users).filter(db.Users.username == user_id).all()
        
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))