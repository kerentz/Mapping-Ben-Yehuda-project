from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask("DataBase")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDataBase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    link = db.Column(db.String(100))
    years = db.Column(db.String(200))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    author = db.Column(db.Integer, db.ForeignKey('Author.id'))
    edition = db.Column(db.String(100))


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    book = db.Column(db.Integer, db.ForeignKey('Book.id'))



