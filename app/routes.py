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
from flask import jsonify, request, Blueprint, current_app, send_file, render_template, make_response
from urllib3.util import response
from werkzeug.utils import secure_filename
from .services import _get_one_random_poem, _get_poem_by_id, _get_all_poems, _get_all_categories, \
    _get_poems_by_category_id, _get_openid

# 使用 prefix 参数定义蓝图的前缀为 '/studypoem'
from .services.footprints_service import _get_all_footprints, _light_footprint, _check_footprint_password
from .services.plan_service import _get_plan_details_by_id, _mark_learned
from .services.poem_service import _search
from .services.user_service import _get_user_plans_by_user_id
from .services.tts_service import _tts, _get_voices

routes = Blueprint('studypoem', __name__, url_prefix='/studypoem')


# 记录请求信息的请求钩子
@routes.before_request
def before_request():
    request_id = secure_filename(str(uuid.uuid4()))
    request.environ['REQUEST_ID'] = request_id

    # 打印请求信息时，将参数统一格式化为 dict
    if request.method == 'GET':
        params = dict(request.args)
    elif request.method in ['POST', 'PUT', 'PATCH']:
        content_type = request.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                params = request.get_json()
            except Exception:
                params = 'Invalid JSON'
        elif 'application/x-www-form-urlencoded' in content_type:
            params = dict(request.form)
        else:
            params = 'Unsupported Content-Type'
    else:
        params = {}

    current_app.logger.info(
        f"[{request_id}] 请求: 方法:{request.method}, url:{request.url}, 参数:{params}"
    )


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
def index():
    return render_template('index.html')


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
        return e, 500
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
        return e, 500
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
        return e, 500
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
        return e, 500
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
        return e, 500
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
        result = _get_openid(code, avatarUrl, nickName)
        current_app.logger.info(f"Response-data: result:{result}")
        if result is None:
            return jsonify({'error': f'获取用户：{code} not found!'}), 404
    except Exception as e:
        return e, 500
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
        return e, 500
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
        return e, 500
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
        return e, 500
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
        return e, 500
    return jsonify(result)


@routes.route('/get_png/<filepath>/<filename>', methods=['GET'])
def get_png(filepath, filename):
    """
    获取图片
    test：http://127.0.0.1:5000/studypoem/get_png/test.png
    """
    try:
        return send_file(f'{filepath}/{filename}', mimetype='image/png')
    except FileNotFoundError:
        return f"File {filename} not found", 404
    except Exception as e:
        return e, 500


# 临时功能，停用
# @routes.route('/out_all_poems', methods=['GET'])
# def out_all_poems():
#     return _out_poems()

@routes.route('/play/<filename>', methods=['GET'])
def play_mp3(filename):
    """
    播放mp3
    test：http://127.0.0.1:5000/studypoem/play/1
    """
    filepath = f'mp3/{filename}.mp3'
    try:
        # 使用send_file返回文件
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        return str(e), 500


@routes.route('/play/tts/<filename>', methods=['GET'])
def play_tts_mp3(filename):
    """
    播放mp3
    test：http://127.0.0.1:5000/studypoem/play/tts/1
    """
    filepath = f'mp3_tts/{filename}.mp3'
    try:
        # 使用send_file返回文件
        return send_file(filepath, mimetype='audio/mpeg')
    except Exception as e:
        return str(e), 500


@routes.route('/tts', methods=['POST'])
def tts():
    """
    text to Speech 文字转语音 使用讯飞的语音合成服务
    test：http://127.0.0.1:5000/studypoem/tts
    body:{
        "text": "测试内容",
        "voice":"x3_xiaodu",
        "speed":50,
        "mp3_filename":"test"
    }
    :return:
    """
    try:
        text = request.json.get('text')
        if not text:
            return jsonify({'error': '请输入文本!'}), 400
        voice = request.json.get('voice')
        speed = request.json.get('speed')
        mp3_filename = request.json.get('mp3_filename')
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        mp3_filename = f'{mp3_filename}{current_time}'
        result = _tts(text, voice, speed, mp3_filename)
        result_code = result[0]
        result_info = result[1]
        if not result_code:
            return f'tts服务异常:{result_info}', 500
    except Exception as e:
        return e, 500
    return f"{result_info}", 200


@routes.route('/voices', methods=['GET'])
def get_voices():
    """
    返回tts所有音色
    test：http://127.0.0.1:5000/studypoem/voices
    :return:
    """
    try:
        voices = _get_voices()
        if voices is None:
            return jsonify({'error': f'系统暂无音色!'}), 404
    except Exception as e:
        return e, 500
    return jsonify(voices)


@routes.route('/download/<filename>', methods=['GET'])
def download(filename):
    # 设置要下载的 MP3 文件路径
    filepath = f'mp3_tts/{filename}'
    try:
        response = make_response(send_file(filepath, as_attachment=True))
        response.headers['Content-Disposition'] = 'attachment; filename=' + filename + '.mp3'
        return response
    except Exception as e:
        return str(e), 500


@routes.route('/tts_web')
def tts_web():
    return render_template('tts.html')


@routes.route('/all_footprints', methods=['GET'])
def get_all_footprints():
    """
    返回所有足迹
    :return:
    """
    try:
        footprints = _get_all_footprints()
        current_app.logger.info(f"Response-data: footprints:{footprints}")
    except Exception as e:
        return e, 500
    return jsonify(footprints)


@routes.route('/footprints')
def footprints():
    return render_template('footprints.html')


@routes.route('/light_footprint', methods=['POST'])
def light_footprint():
    """
    点亮足迹
    test：http://127.0.0.1:5000/studypoem/light_footprint
    body:{
        "province": "河南",
        "light_up_img":"img地址",
        "light_up_time": "2025-04-11"
    }
    :return:
    """
    try:
        province = request.form.get('province')
        current_app.logger.info(f"province:{province}")
        light_up_img = request.files.get('light_up_img')
        current_app.logger.info(f"light_up_img:{light_up_img}")
        light_up_time = request.form.get('light_up_time')
        current_app.logger.info(f"light_up_time:{light_up_time}")

        if not all([province, light_up_img, light_up_time]):
            return jsonify({"status": "fail", "message": "缺少必要参数"}), 400
        result = _light_footprint(province, light_up_img, light_up_time)
        current_app.logger.info(f"Response-data: result:{result}")
        if result == "success":
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "fail", "message": result}), 500
    except Exception as e:
        return e, 500

@routes.route('/check_footprint_password', methods=['POST'])
def check_footprint_password():
    """
    接收密码并校验是否正确
    :return: JSON 响应
    """
    password = request.get_json().get('password')
    if not password:
        return jsonify({"status": "fail", "message": "缺少密码参数"}), 400
    result = _check_footprint_password(password)
    if result:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "fail", "message": "密码校验失败！"}), 500
