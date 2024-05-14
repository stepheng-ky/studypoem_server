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


def optimize_poems(data):
    """
    优化data的结构
    """
    # 创建一个字典来存储优化后的数据
    optimized_data = {
        'category_id': data['category_id'],
        'category_name': data['category_name'],
        'poems': []
    }
    # 使用字典推导式按second_level_category分组
    grouped_poems = {}
    for poem_dict in data['poems']:
        poem = poem_dict['poem']
        second_level_category = poem_dict['second_level_category']
        # 如果该second_level_category还没有在分组字典中，则初始化一个空列表
        grouped_poems.setdefault(second_level_category, []).append({
            'author_short': poem['author_short'],
            'id': poem['id'],
            'title': poem['title']
        })
    # 将分组后的数据转换为所需的格式
    for second_level_cat, poems in grouped_poems.items():
        optimized_data['poems'].append({
            'second_level_category': second_level_cat,
            'second_level_poems': poems
        })
    return optimized_data


def _get_poems_by_category_id(category_id):
    """
    根据类别id返回古诗
    :return:
    """
    # 类别信息
    category = Categories.query.get(category_id)
    if not category:
        return None
    result = {'category_id': category_id,
              'category_name': category.category_name,
              "poems": []}
    # 诗词信息
    category_poems = [{'second_level_category': category_poem.second_level_category,
                       'poem': model_to_dict(Poems.query.get(category_poem.poem_id))}
                      for category_poem in
                      CategoryPoem.query.filter_by(category_id=category_id).order_by(CategoryPoem.second_level_category_order.asc()).all()]
    result.update({'poems': [{'second_level_category': category_poem.get('second_level_category'),
                              'poem': category_poem.get('poem')
                              }
                             for category_poem in category_poems
                             ]
                   })
    # print(f'result:{result}')
    result_final = optimize_poems(result)
    # print(f'result_final:{result_final}')
    return result_final
