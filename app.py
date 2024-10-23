from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import sqlite3
import os 
from FDataBase import FDataBase


SECRET_KEY = 'dhweidh3h3897yd37dy732qhdvhn'
DATABASE = 'tml/flsite.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

dbase = None
@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.route('/')
def index():
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route('/add_post', methods=["POST", "GET"])
def addPost():
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category = 'danger')
            else:
                flash('Статья добавлена', category = 'success')
        else:
            flash('Ошибка добавления статьи', category = 'danger')
    return render_template('add_post.html', menu = dbase.getMenu(), title = "Добавление статьи")

@app.route("/post/<alias>")
def showPost(alias):
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


@app.errorhandler(404)
def pageNotFound(error):
    menu = dbase.getMenu()
    return render_template('page404.html', title="Старница не найдена", menu=menu), 404

@app.errorhandler(401)
def pageNotFound(error):
    menu = dbase.getMenu()
    return render_template('page401.html', title="Пользователь не авторизован", menu=menu), 401

# @app.route('/about')
# def about():
#     print(url_for('about'))
#     return render_template('index.html', title="О сайте", menu=menu)

# @app.route('/contact', methods=["POST", "GET"])
# def contact():
#     if request.method == "POST":
#         print(request.form)
#         if len(request.form["username"]) > 2:
#             flash("Сообщение отправлено успешно", category="success")
#         else:
#             flash("Ошибка отправки", category="danger")

#     return render_template('contact.html', title="Обратная связь", menu=menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogget' not in session or session['userLogget'] != username:
        abort(401)
    return f"Пользователь {username}"

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('login.html', title="Авторизация", menu=dbase.getMenu())

@app.route("/register", methods=["GET", "POST"])
def register():
    if len(request.form['name']) > 4 and len(request.form['email']) > 4\
        and len(request.form['psw']) > 4 and len(request.form['psw']) == len(request.form['psw2']):
        hash = generate_password_hash(request.form['psw'])
        res = dbase.addUser(request.form['name'], request.form['email'], hash)
        if res:
            flash()
            return redirect(url_for('login'))
        else:
            flash()###########################
    else:
        flash() ###########################

    return render_template('register.html', menu=dbase.getMenu(), title="Регистрация")

if __name__ == '__main__':
    app.run(debug=True)
