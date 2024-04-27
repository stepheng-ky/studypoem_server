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


# Poems类 转json
def poem_to_dict(poem):
    return {
        'id': poem.id,
        'title': poem.title,
        'author': poem.author,
        'content': poem.content,
        'yiwen': poem.yiwen,
        'zhailu': poem.zhailu
    }


def _get_one_random_poem():
    """
    随机返回一首古诗
    :return:
    """
    poem = Poems.query.order_by(func.rand()).first()
    return poem_to_dict(poem)


def _get_poem_by_id(poem_id):
    """
    根据id查询古诗
    :param poem_id:
    :return:
    """
    poem = Poems.query.get(poem_id)
    return poem_to_dict(poem)


def _get_all_poems():
    """
    返回所有古诗
    :return:
    """
    poems = Poems.query.all()
    poems_list = [poem_to_dict(poem) for poem in poems]
    return poems_list
