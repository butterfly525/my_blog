from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Role(db.Model):
    __tablename__ = 'role'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=2)
    role = db.relationship('Role', backref='users')


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    edited_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    

    def __repr__(self):
        return f'<Post {self.title}>'

class Photo(db.Model):
    __tablename__ = 'photos'  # Укажите имя таблицы

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)  # Поле для хранения пути к изображению
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)  # Внешний ключ на пост
    post = db.relationship('Post', backref=db.backref('photos', lazy='dynamic'))  # Связь с моделью Post

    def __repr__(self):
        return f'<Photo {self.id} for Post {self.post_id}>'