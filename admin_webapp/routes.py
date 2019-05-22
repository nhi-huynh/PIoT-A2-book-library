# vim: set et sw=4 ts=4 sts=4:
from class_.Auth import Auth
from flask import redirect, session, render_template, request
from flask_wtf import FlaskForm
import wtforms as wtf
from run import app


# NOTE
# GenerateVisual class:
#
# gv = GenerateVisual(
#       app.config['PLOTLY_USERNAME'],
#       app.config['PLOTLY_USERNAME']
# )


def logged_in(sess):
    return 'auth_success' in sess and sess['auth_success']


class LoginForm(FlaskForm):
    uname = wtf.TextField('Username', [wtf.validators.required()])
    password = wtf.PasswordField('Password', [wtf.validators.required()])
    submit = wtf.SubmitField('Submit')


@app.route('/')
@app.route('/index')
def index():
    if logged_in(session):
        return redirect('/admin')

    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in(session):
        return redirect('/admin')

    if request.method == 'GET' or 'ajax' not in request.form:
        form = LoginForm()
        return render_template('login.bs.html', form=form)

    if 'user' not in request.form or 'pass' not in request.form:
        return '{"auth_succes":false}'

    user = request.form['user']
    pass_ = request.form['pass']

    if not Auth.verify_passwd(pass_, app.config['ADMIN_PASSWORD']):
        return '{"auth_succes":false}'

    if user != app.config['ADMIN_USERNAME']:
        return '{"auth_success":false}'

    session['auth_success'] = True

    return '{"auth_success":true}'


@app.route('/logout')
def logout():
    if 'auth_success' in session:
        del session['auth_success']

    return redirect('/login')


@app.route('/admin')
@app.route('/admin/dashboard')
def dashboard():
    if not logged_in(session):
        return redirect('/login')

    return render_template('admin-dashboard.bs.html', page='dashboard')


@app.route('/admin/book-manager')
def book_manage():
    if not logged_in(session):
        return redirect('/login')
    
    return render_template('admin-book-manage.bs.html', page='manage')


@app.route('/admin/daily-borrows')
def daily_borrows():
    if not logged_in(session):
        return redirect('/login')
    
    return render_template('admin-dailyborrows.bs.html', page='manage')
