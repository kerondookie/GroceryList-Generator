from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField, TextField
from wtforms.fields.html5 import EmailField
from wtforms.validators import InputRequired, EqualTo, Email


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    todos = db.relationship('Todo', backref='user', lazy=True) # sets up a relationship to todos which references User

    def toDict(self):
      return {
        "id": self.id,
        "username": self.username,
        "email": self.email,
        "password": self.password
      }



