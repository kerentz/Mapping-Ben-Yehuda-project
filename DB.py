from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask("Prose")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ProjectDataBase.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Work(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    general_note = db.Column(db.String(200))
    genre = db.Column(db.String(100))
    author_id = db.Column(db.Integer)
    work_id = db.Column(db.Integer)
    h4 = db.Column(db.String(100))
    edition_details = db.Column(db.String(200))
    h3 = db.Column(db.String(200))
    edition_id = db.Column(db.String(200))
    p = db.Column(db.String(200))
    type = db.Column(db.String(200))
