from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
from models import *
from forms import *
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
import os
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join('static', 'uploads')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin_my_blog:admin123@0.0.0.0:5432/my_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'qwertyiioacsc'
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER,
                               filename)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                # Перенаправление на главную страницу
                return redirect(url_for('index'))
            else:
                flash('Неверный пароль.', 'danger')
        else:
            flash(
                'Пользователя с таким именем нет, попробуйте зарегистрироваться.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Проверка существования имени пользователя
        existing_user_username = User.query.filter_by(
            username=form.username.data).first()
        if existing_user_username:
            flash('Такое имя пользователя уже занято. Выберите другое имя.', 'danger')
            return render_template('register.html', form=form)

        # Проверка существования email
        existing_user_email = User.query.filter_by(
            email=form.email.data).first()
        if existing_user_email:
            flash(
                'Такой email уже зарегистрирован. Войдите или используйте другой email.', 'danger')
            return render_template('register.html', form=form)

        # Если проверки пройдены успешно, создаем нового пользователя
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


@app.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if current_user.role_id != 1:
        abort(403)  # Запрещаем доступ не-администраторам

    form = PostForm()  # Предполагается, что у вас есть форма для добавления поста
    if form.validate_on_submit():
        try:
            post = Post(
                title=form.title.data,
                content=form.content.data,
                author=current_user,
                created_at=datetime.now(),
                edited_at=datetime.now()
            )
            db.session.add(post)
            db.session.flush()  # Это обновит id в сессии

            post_id = post.id
            # Сохраняем фотографии
            for photo in request.files.getlist('photos'):
                filename = photo.filename
                if filename:
                    filename = f"{post_id}_{filename}"
                    photo_path = os.path.join(UPLOAD_FOLDER, filename)
                    photo.save(photo_path)  # Сохраняем файл на диск
                    # Создаем экземпляр модели Photo
                    # Используем поле image
                    photo_model = Photo(image=filename, post=post)
                    db.session.add(photo_model)

            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(f"{e}", 'danger')
    
    return render_template('add_post.html', form=form)


@app.route('/post/<id>', methods=['GET'])
@login_required
def read_post(id):
    post = Post.query.get_or_404(id)
    # Формирование словаря с информацией о посте
    formatted_post = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'edited_at': post.edited_at.strftime('%d-%m-%Y %H:%M'),
        'photos': [photo.image for photo in post.photos]
    }

    return render_template('read_post.html', post=formatted_post)


@app.route('/')
def index():
    posts = Post.query.order_by(Post.edited_at.desc())
    formatted_posts = [
        {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'edited_at': post.edited_at.strftime('%d-%m-%Y %H:%M'),
            'photos': [photo.image for photo in post.photos]

        }
        for post in posts
    ]
    return render_template('index.html', posts=formatted_posts)


if __name__ == "__main__":
    app.run(debug=True)
