# app.py

import sys
sys.path.extend([r"/data/env/studyPoem-server/studyPoem-server"])


from flask import Flask, jsonify
from config import Config
from models import db, get_one_random_poem
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)  # 加载配置

db.init_app(app)


@app.route('/studypoem')
def helloworld():
    return f'hello-world {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'


# 定义GET请求接口来获取所有poem
@app.route('/studypoem/random_poem', methods=['GET'])
def get_random_poem():
    _poem = get_one_random_poem()
    poem = {'id': _poem.id, 'title': _poem.title, 'author': _poem.author, 'content': _poem.content, 'yiwen': _poem.yiwen,
         'zhailu': _poem.zhailu}
    return jsonify(poem)


if __name__ == '__main__':
    app.run
