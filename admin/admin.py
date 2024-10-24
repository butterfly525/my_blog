from flask import Blueprint, request, flash, url_for, redirect, session, render_template

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


menu = [
    {'url': '.index', 'title': 'Панель'},
    {'url': '.logout', 'title': 'Выйти'}
]

def login_admin():
    session['admin_logged']  = 1

def isLogget():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

@admin.route('/')
def index():
    if not isLogget():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title="Админ-панель")

@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogget():
        return redirect(url_for('.index'))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))

        else:
            flash("Неверная пара логин-пароль", "error")
    return render_template('admin/login.html', title='Админ-панель')

@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogget():
        return redirect(url_for('.login'))
    logout_admin()

    return redirect(url_for('.login'))