#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:26
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : routes.py
# 功能描述  ：路由控制
import json
import uuid
from datetime import datetime
from flask import jsonify, request, Blueprint, current_app, send_file
from werkzeug.utils import secure_filename
from .services import _get_one_random_poem, _get_poem_by_id, _get_all_poems, _get_all_categories, \
    _get_poems_by_category_id, _get_openid

# 使用 prefix 参数定义蓝图的前缀为 '/studypoem'
from .services.plan_service import _get_plan_details_by_id, _mark_learned
from .services.poem_service import _search
from .services.user_service import _get_user_plans_by_user_id
# from .tts.output_all_poems import _out_poems

routes = Blueprint('studypoem', __name__, url_prefix='/studypoem')


# 记录请求信息的请求钩子
@routes.before_request
def before_request():
    request_id = secure_filename(str(uuid.uuid4()))  # 使用uuid库生成UUID
    request.environ['REQUEST_ID'] = request_id  # 将请求ID存储在request.environ中
    current_app.logger.info(f"请求: 方法:{request.method}, url:{request.url}, 参数:{request.args}")


# 记录响应信息的请求钩子
@routes.after_request
def after_request(response):
    current_app.logger.info(f"响应结果-状态码:{response.status_code}")
    # current_app.logger.info(f"响应结果-数据:{response.data.decode('utf-8')}")
    try:
        content = response.get_json()  # 尝试将响应内容解析为 JSON 格式
        formatted_content = json.dumps(content, indent=4, ensure_ascii=False)
    except Exception:
        formatted_content = response.data.decode('utf-8')  # 如果无法解析为 JSON，以 UTF-8 格式显示

    current_app.logger.info(f"响应结果-数据: {formatted_content}")
    return response


@routes.route('/')
def helloworld():
    poem = """
    将进酒<br><br><br>
    君不见黄河之水天上来，奔流到海不复回。<br><br>
    君不见高堂明镜悲白发，朝如青丝暮成雪。<br><br>
    人生得意须尽欢，莫使金樽空对月。<br><br>
    天生我材必有用，千金散尽还复来。<br><br>
    烹羊宰牛且为乐，会须一饮三百杯。<br><br>
    岑夫子，丹丘生，将进酒，杯莫停。<br><br>
    与君歌一曲，请君为我侧耳听。<br><br>
    钟鼓馔玉不足贵，但愿长醉不复醒。<br><br>
    古来圣贤皆寂寞，惟有饮者留其名。<br><br>
    陈王昔时宴平乐，斗酒十千恣欢谑。<br><br>
    主人何为言少钱，径须沽取对君酌。<br><br>
    五花马、千金裘，呼儿将出换美酒，与尔同销万古愁。
    """
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'''
    <html>
    <head>
    <style>
    body {{
        background-color: gray; /* Light gray background color */
        font-family: Arial, sans-serif; /* Font family */
        color: blue; /* Text color */
    }}
    .poem-container {{
        text-align: center;
        margin-top: 10%;
        font-size: 24px; /* Font size for the poem */
    }}
    .time-container {{
        position: absolute;
        top: 10px;
        right: 10px;
        font-size: 14px; /* Font size for the time */
    }}
    </style>
    </head>
    <body>
    <div class="poem-container">
        <p>{poem}</p>
    </div>
    <div class="time-container">{current_time}</div>
    </body>
    </html>
    '''

@routes.route('/random_poem', methods=['GET'])
def get_random_poem():
    """
    随机返回一首古诗
    :return:
    """
    try:
        poem = _get_one_random_poem()
        current_app.logger.info(f"Response-data: poem:{poem}")
    except Exception as e:
        return e,500
    return jsonify(poem)


@routes.route('/all_poems', methods=['GET'])
def get_all_poems():
    """
    返回所有古诗
    :return:
    """
    try:
        poems = _get_all_poems()
        current_app.logger.info(f"Response-data: poems:{poems}")
    except Exception as e:
        return e,500
    return jsonify(poems)


@routes.route('/poem_details', methods=['GET'])
def get_poem_by_id():
    """
    根据id返回古诗详情
    test：http://127.0.0.1:5000/studypoem/poem_details?id=af4715c0208f
    :return:
    """
    try:
        # 获取查询参数 'id'
        poem_id = request.args.get('id')
        # 调用函数获取诗词详情
        poem = _get_poem_by_id(poem_id)
        current_app.logger.info(f"Response-data: poem:{poem}")
        if poem is None:
            return jsonify({'error': f'古诗{poem_id} not found!'}), 404
    except Exception as e:
        return e,500
    return jsonify(poem)


@routes.route('/all_categories', methods=['GET'])
def get_all_categories():
    """
    返回所有古诗类别
    :return:
    """
    try:
        categories = _get_all_categories()
        current_app.logger.info(f"Response-data: categories:{categories}")
    except Exception as e:
        return e,500
    return jsonify(categories)


@routes.route('/category', methods=['GET'])
def get_poems_by_category_id():
    """
    根据类别id返回古诗s
    :return:
    """
    try:
        # 获取查询参数 'id'
        category_id = request.args.get('category_id')
        # 调用函数获取诗词详情
        category = _get_poems_by_category_id(category_id)
        current_app.logger.info(f"Response-data: category:{category}")
        if category is None:
            return jsonify({'error': f'类别{category_id} not found!'}), 404
    except Exception as e:
        return e,500
    return jsonify(category)


@routes.route('/openid', methods=['POST'])
def get_openid():
    """
    根据code获取微信的openid和session_key
    test：http://127.0.0.1:5000/studypoem/openid
    body:{
        "code": "code",
        "nickName":"nickName",
        "avatarUrl":”avatarUrl“
    }
    :return:
    """
    try:
        code = request.json.get('code')
        avatarUrl = request.json.get('avatarUrl')
        nickName = request.json.get('nickName')
        result = _get_openid(code,avatarUrl,nickName)
        current_app.logger.info(f"Response-data: result:{result}")
        if result is None:
            return jsonify({'error': f'获取用户：{code} not found!'}), 404
    except Exception as e:
        return e,500
    return jsonify(result)


@routes.route('/user_plans', methods=['GET'])
def get_user_plans_by_user_id():
    """
    根据user_id返回用户计划列表
    test：http://127.0.0.1:5000/studypoem/user_plans
    :return:
    """
    try:
        # 获取查询参数 'user_id'
        user_id = request.args.get('user_id')
        # 调用函数获取学习计划列表
        plans = _get_user_plans_by_user_id(user_id)
        current_app.logger.info(f"Response-data: plans:{plans}")
        if plans is None:
            return jsonify({'error': f'用户{user_id} not found!'}), 404
    except Exception as e:
        return e,500
    return jsonify(plans)


@routes.route('/plan_details', methods=['GET'])
def get_plan_details_by_id():
    """
    根据plan_id返回计划详情
    test：http://127.0.0.1:5000/studypoem/plan_details?plan_id=1
    :return:
    """
    try:
        # 获取查询参数 'plan_id'
        plan_id = request.args.get('plan_id')
        # 调用函数获取学习计划详情
        plan = _get_plan_details_by_id(plan_id)
        current_app.logger.info(f"Response-data: plan:{plan}")
        if plan is None:
            return jsonify({'error': f'计划{plan_id} not found!'}), 404
    except Exception as e:
        return e,500
    return jsonify(plan)


@routes.route('/search', methods=['GET'])
def search():
    """
    根据q返回模糊匹配到的所有诗词
    test：http://127.0.0.1:5000/studypoem/search?q=李白
    :return:
    """
    try:
        # 获取查询参数 'q'
        q = request.args.get('q')
        # 调用函数获取学习计划详情
        poems = _search(q)
        if poems is None:
            return jsonify({'error': f'模糊搜索关键字【{q}】没有结果!'}), 404
    except Exception as e:
        return e,500
    return jsonify(poems)


@routes.route('/mark_learned', methods=['POST'])
def mark_learned():
    """
    根据id打卡，修改为已学习
    test：http://127.0.0.1:5000/studypoem/mark_learned
    body:{
        "plan_id": plan_id,
        "id":"id",
        "is_learned":1/0
    }
    :return:
    """
    try:
        plan_id = request.json.get('plan_id')
        id = request.json.get('id')
        is_learned = request.json.get('is_learned')
        result = _mark_learned(plan_id, id, is_learned)
        current_app.logger.info(f"Response-data: result:{result}")
        if result is None:
            return jsonify({'error': f'计划{plan_id}的诗{id}打卡失败!'}), 500
    except Exception as e:
        return e,500
    return jsonify(result)

@routes.route('/get_png/<filename>', methods=['GET'])
def get_png(filename):
    """
    获取图片
    test：http://127.0.0.1:5000/studypoem/get_png/test.png
    """
    try:
        return send_file(f'poems_png/{filename}', mimetype='image/png')
    except FileNotFoundError:
        return f"File {filename} not found", 404
    except Exception as e:
        return e,500

# 临时功能，停用
# @routes.route('/out_all_poems', methods=['GET'])
# def out_all_poems():
#     return _out_poems()

@routes.route('/play/<filename>', methods=['GET'])
def play_mp3(filename):
    """
    获取图片
    test：http://127.0.0.1:5000/studypoem/play/1
    """
    filepath = f'mp3/{filename}.mp3'
    try:
        # 使用send_file返回文件
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        return str(e), 500