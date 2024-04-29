#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:26
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : routes.py
# 功能描述  ：路由控制

from datetime import datetime
from flask import jsonify, request, Blueprint
from app.services import _get_one_random_poem, _get_poem_by_id, _get_all_poems, _get_all_categories, \
    _get_poems_by_category_id, _get_openid

# 使用 prefix 参数定义蓝图的前缀为 '/studypoem'
routes = Blueprint('studypoem', __name__, url_prefix='/studypoem')

@routes.route('/')
def helloworld():
    return f'好好学习\n 天天向上\n {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'


@routes.route('/random_poem', methods=['GET'])
def get_random_poem():
    """
    随机返回一首古诗
    :return:
    """
    poem = _get_one_random_poem()
    return jsonify(poem)


@routes.route('/all_poems', methods=['GET'])
def get_all_poems():
    """
    返回所有古诗
    :return:
    """
    poems = _get_all_poems()
    return jsonify(poems)


@routes.route('/poem_details', methods=['GET'])
def get_poem_by_id():
    """
    根据id返回古诗详情
    test：http://127.0.0.1:5000/studypoem/poem_details?id=af4715c0208f
    :return:
    """
    # 获取查询参数 'id'
    poem_id = request.args.get('id')
    # 调用函数获取诗词详情
    poem = _get_poem_by_id(poem_id)
    if poem is None:
        return jsonify({'error': f'古诗{poem_id} not found!'}), 404
    return jsonify(poem)


@routes.route('/all_categories', methods=['GET'])
def get_all_categories():
    """
    返回所有古诗类别
    :return:
    """
    categories = _get_all_categories()
    return jsonify(categories)


@routes.route('/category', methods=['GET'])
def get_poems_by_category_id():
    """
    根据类别id返回古诗s
    :return:
    """
    # 获取查询参数 'id'
    category_id = request.args.get('category_id')
    # 调用函数获取诗词详情
    category = _get_poems_by_category_id(category_id)
    if category is None:
        return jsonify({'error': f'类别{category_id} not found!'}), 404
    print(f'category={category}\n')
    return jsonify(category)


@routes.route('/openid', methods=['POST'])
def get_openid():
    """
    根据code获取微信的openid和session_key
    :return:
    """
    print(f'开始请求...')
    code = request.json.get('code')
    print(f'code={code}')
    result = _get_openid(code)
    if result is None:
        return jsonify({'error': f'获取用户：{code} not found!'}), 404
    return jsonify(result)
