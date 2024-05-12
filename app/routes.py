#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:26
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : routes.py
# 功能描述  ：路由控制

import uuid
from datetime import datetime
from flask import jsonify, request, Blueprint, current_app
from werkzeug.utils import secure_filename
from .services import _get_one_random_poem, _get_poem_by_id, _get_all_poems, _get_all_categories, \
    _get_poems_by_category_id, _get_openid

# 使用 prefix 参数定义蓝图的前缀为 '/studypoem'
from .services.plan_service import _get_plan_details_by_id
from .services.poem_service import _search
from .services.user_service import _get_user_plans_by_user_id

routes = Blueprint('studypoem', __name__, url_prefix='/studypoem')


# 记录请求信息的请求钩子
@routes.before_request
def before_request():
    request_id = secure_filename(str(uuid.uuid4()))  # 使用uuid库生成UUID
    request.environ['REQUEST_ID'] = request_id  # 将请求ID存储在request.environ中
    current_app.logger.info(f"Request: method:{request.method}, url:{request.url}, args:{request.args}")


# 记录响应信息的请求钩子
@routes.after_request
def after_request(response):
    current_app.logger.info(f"Response-status_code:{response.status_code}")
    # 注意：不要在这里记录大型响应体，因为这可能会降低性能
    return response


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
    current_app.logger.info(f"Response-data: poem:{poem}")
    return jsonify(poem)


@routes.route('/all_poems', methods=['GET'])
def get_all_poems():
    """
    返回所有古诗
    :return:
    """
    poems = _get_all_poems()
    current_app.logger.info(f"Response-data: poems:{poems}")
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
    current_app.logger.info(f"Response-data: poem:{poem}")
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
    current_app.logger.info(f"Response-data: categories:{categories}")
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
    current_app.logger.info(f"Response-data: category:{category}")
    if category is None:
        return jsonify({'error': f'类别{category_id} not found!'}), 404
    return jsonify(category)


@routes.route('/openid', methods=['POST'])
def get_openid():
    """
    根据code获取微信的openid和session_key
    test：http://127.0.0.1:5000/studypoem/openid?code=123
    :return:
    """
    code = request.json.get('code')
    avatarUrl = request.json.get('avatarUrl')
    nickName = request.json.get('nickName')
    result = _get_openid(code,avatarUrl,nickName)
    current_app.logger.info(f"Response-data: result:{result}")
    if result is None:
        return jsonify({'error': f'获取用户：{code} not found!'}), 404
    return jsonify(result)


@routes.route('/user_plans', methods=['GET'])
def get_user_plans_by_user_id():
    """
    根据user_id返回用户计划列表
    test：http://127.0.0.1:5000/studypoem/user_plans?user_id=1
    :return:
    """
    # 获取查询参数 'user_id'
    user_id = request.args.get('user_id')
    # 调用函数获取学习计划列表
    plans = _get_user_plans_by_user_id(user_id)
    current_app.logger.info(f"Response-data: plans:{plans}")
    if plans is None:
        return jsonify({'error': f'用户{user_id} not found!'}), 404
    return jsonify(plans)


@routes.route('/plan_details', methods=['GET'])
def get_plan_details_by_id():
    """
    根据plan_id返回计划详情
    test：http://127.0.0.1:5000/studypoem/plan_details?plan_id=1
    :return:
    """
    # 获取查询参数 'plan_id'
    plan_id = request.args.get('plan_id')
    # 调用函数获取学习计划详情
    plan = _get_plan_details_by_id(plan_id)
    current_app.logger.info(f"Response-data: plan:{plan}")
    if plan is None:
        return jsonify({'error': f'计划{plan_id} not found!'}), 404
    return jsonify(plan)


@routes.route('/search', methods=['GET'])
def search():
    """
    根据q返回模糊匹配到的所有诗词
    test：http://127.0.0.1:5000/studypoem/search?q=李白
    :return:
    """
    # 获取查询参数 'q'
    q = request.args.get('q')
    # 调用函数获取学习计划详情
    poems = _search(q)
    current_app.logger.info(f"Response-data: poems:{poems}")
    if poems is None:
        return jsonify({'error': f'模糊搜索关键字【{q}】没有结果!'}), 404
    return jsonify(poems)
