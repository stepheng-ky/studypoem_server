#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/28 9:51
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : config.py
# 功能描述  ：主应用入口
import sys

from flask import Flask
from .config import Config
from .config import db
from .routes import routes

sys.path.extend([r"/data/env/studyPoem-server/studypoem_server"])

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 注册路由
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run()