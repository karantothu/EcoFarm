from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from werkzeug.security import check_password_hash, generate_password_hash
import functools

bp_auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

# **************************** AUTH START ****************************************


@bp_auth.route('/home')
def index():
    return render_template('home.html')


@bp_auth.route('/register', methods=('GET', 'POST'))
def register():
    from app import dbh
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        error = None
        query = """SELECT id FROM user WHERE username = '{}'""".format(username)

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not confirm_password or password != confirm_password:
            error = 'Password not matched.'
        elif dbh.fetch_one(query) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            query = """INSERT INTO user (username, password) 
                       VALUES ('{}', '{}')""".format(username, generate_password_hash(password))

            dbh.execute(query)
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')


@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    from app import dbh
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        query = """SELECT * FROM user WHERE username = '{}'""".format(username)
        user = dbh.fetch_one(query)
        print(user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('auth.index'))

        flash(error)

    return render_template('login.html')


@bp_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))


@bp_auth.before_app_request
def load_logged_in_user():
    from app import dbh
    user_id = session.get('username')

    if user_id is None:
        g.user = None
    else:
        query = """SELECT * FROM user WHERE username = '{}'""".format(user_id)
        g.user = dbh.fetch_one(query)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# **************************** AUTH END ****************************************

