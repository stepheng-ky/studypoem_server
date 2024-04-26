# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Poems(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text)
    yiwen = db.Column(db.Text)
    zhailu = db.Column(db.Text)

def get_one_random_poem():
    poem = Poems.query.order_by(func.rand()).first()
    return poem

def get_all_poems():
    return Poems.query.all()
