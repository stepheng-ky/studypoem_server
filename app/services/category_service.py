#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:32
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : category_service.py
# 功能描述  ：类别服务

from ..models import Categories, CategoryPoem, Poems
from ..utils import model_to_dict

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
