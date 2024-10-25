from flask import Blueprint, request, flash, url_for, redirect, session, render_template, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


menu = [
    {'url': '.index', 'title': 'Панель'},
    {'url': '.listpubs', 'title': 'Посты'},
    {'url': '.listusers', 'title': 'Пользователи'},
    {'url': '.logout', 'title': 'Выйти'}
]

db = None

@admin.before_request
def before_request():
    global db
    db = g.get('link_db')

@admin.teardown_request
def teardown_request(request):
    global db
    db = None 
    return request    

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


@admin.route('/list_pubs')
def listpubs():
    if not isLogget():
        return redirect(url_for('.login'))
    
    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT title, text, url FROM posts')
            list = cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения статей из БД {e}")

    return render_template('admin/list_pubs.html', title='Список статей', menu=menu, list=list)



@admin.route('/list_users')
def listusers():
    if not isLogget():
        return redirect(url_for('.login'))
    
    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT name, email FROM users ORDER BY time DESC')
            list = cur.fetchall()
        except sqlite3.Error as e:
            print(f"Ошибка получения пользователей из БД {e}")

    return render_template('admin/list_users.html', title='Список пользователей', menu=menu, list=list)