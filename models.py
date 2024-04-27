# models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


class Poems(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    yiwen = db.Column(db.Text)
    zhailu = db.Column(db.Text)
    author_short = db.Column(db.String(100), nullable=False)


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255), nullable=False)


class CategoryPoem(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    second_level_category = db.Column(db.String(255))
    id = db.Column(db.String(255), primary_key=True)


def model_to_dict(model):
    """
    将Flask-SQLAlchemy模型对象转换为字典。
    """
    # 初始化一个空字典来存储属性
    if not model:
        return
    result = {}
    # 遍历模型对象的所有属性
    for column in model.__table__.columns:
        # 使用getattr来获取属性的值
        value = getattr(model, column.name)
        # 如果值是关系对象（比如另一个模型），则递归调用model_to_dict
        if isinstance(value, db.Model):
            value = model_to_dict(value)
        # 将属性名和值添加到字典中
        result[column.name] = value
    return result


def _get_one_random_poem():
    """
    随机返回一首古诗
    :return:
    """
    poem = model_to_dict(Poems.query.order_by(func.rand()).first())
    return poem


def _get_poem_by_id(poem_id):
    """
    根据id查询古诗
    :param poem_id:
    :return:
    """
    poem = model_to_dict(Poems.query.get(poem_id))
    return poem


def _get_all_poems():
    """
    返回所有古诗
    :return:
    """
    poems = Poems.query.all()
    poems_list = [model_to_dict(poem) for poem in poems]
    return poems_list


def _get_all_categories():
    """
    返回所有类别
    :return:
    """
    categories = Categories.query.all()
    categories_list = [model_to_dict(category) for category in categories]
    return categories_list


def _get_poems_by_category_id(category_id):
    """
    根据类别id返回古诗
    :return:
    """
    result = {'category_id': category_id}
    # 类别信息
    category = Categories.query.get(category_id)
    if not category:
        return
    result.update({'category_name': category.category_name})
    # 诗词信息
    category_poems = [{'second_level_category': category_poem.second_level_category,
                       'poem': model_to_dict(Poems.query.get(category_poem.id))} for category_poem in
                      CategoryPoem.query.filter_by(category_id=category_id).all()]
    result.update({'poems': [{'second_level_category': category_poem.get('second_level_category'),
                              'id': category_poem.get('poem').get('id'),
                              'title': category_poem.get('poem').get('title'),
                              'author_short': category_poem.get('poem').get('author_short')
                              }
                             for category_poem in category_poems
                             ]
                   })
    return result
