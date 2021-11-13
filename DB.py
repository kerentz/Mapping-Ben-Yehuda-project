from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask("DataBase")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDataBase.sqlite3'
db = SQLAlchemy(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    link = db.Column(db.String(100))
    years = db.Column(db.String(200))


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.Integer, Foreign_Key=Author.id)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))


