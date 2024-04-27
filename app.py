# app.py
import sys
from flask import Flask, jsonify, request
from config import Config
from models import db, _get_one_random_poem, _get_poem_by_id, _get_all_poems
from datetime import datetime

sys.path.extend([r"/data/env/studyPoem-server/studypoem_server"])


app = Flask(__name__)
app.config.from_object(Config)  # 加载配置
db.init_app(app)


@app.route('/studypoem')
def helloworld():
    return f'hello-world {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'


@app.route('/studypoem/random_poem', methods=['GET'])
def get_random_poem():
    """
    随机返回一首古诗
    :return:
    """
    poem = _get_one_random_poem()
    return jsonify(poem)


@app.route('/studypoem/all_poems', methods=['GET'])
def get_all_poems():
    """
    返回所有古诗
    :return:
    """
    poems = _get_all_poems()
    return jsonify(poems)


@app.route('/studypoem/poem_details', methods=['GET'])
def _get_poem_details():
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
        return jsonify({'error': 'Poem not found!'}), 404
    return jsonify(poem)


if __name__ == '__main__':
    app.run()
