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
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)

        return redirect(url_for('index'))

    else:
        flash('Невалидные данные.', 'danger')
    return render_template('register.html', form=form)


@app.route('/post/add', methods=['GET', 'POST'])
@login_required
def add_post():
    if current_user.role_id != 1:
        abort(403)  # Запрещаем доступ не-администраторам

    form = PostForm()  # Предполагается, что у вас есть форма для добавления поста
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            author=current_user,
            created_at=datetime.now(),
            edited_at=datetime.now()
        )
        db.session.add(post)

        # Сохраняем фотографии
        for photo in request.files.getlist('photos'):
            filename = secure_filename(photo.filename)
            print(filename)
            photo_path = os.path.join(UPLOAD_FOLDER, filename)
            print(photo_path)
            photo.save(photo_path)  # Сохраняем файл на диск

            # Создаем экземпляр модели Photo
            # Используем поле image
            photo_model = Photo(image=photo_path, post=post)
            db.session.add(photo_model)

        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_post.html', form=form)


@app.route('/delete_photo/<int:post_id>/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(post_id, photo_id):
    post = Post.query.get_or_404(post_id)
    photo = Photo.query.filter_by(id=photo_id).first_or_404()
    db.session.delete(photo)
    db.session.commit()
    flash('Фото успешно удалено!', 'success')
    return redirect(url_for('view_post', post_id=post.id))


@app.route('/')
def index():
    posts = Post.query.order_by(Post.edited_at.desc())
    formatted_posts = [
        {
            'title': post.title,
            'content': post.content,
            'author': post.author.username,
            'edited_at': post.edited_at.strftime('%d-%m-%Y %H:%M'),
            'photos': [photo.image for photo in post.photos]
            
        }
        for post in posts
    ]
    print(formatted_posts)
    return render_template('index.html', posts=formatted_posts)


if __name__ == "__main__":
    app.run(debug=True)
