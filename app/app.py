#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/28 9:51
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : config.py
# 功能描述  ：主应用入口
import logging
import sys
from logging.handlers import RotatingFileHandler
from flask import Flask, request
from .config import Config, db
from .routes import routes

sys.path.extend([r"/data/env/studyPoem-server/studypoem_server"])


def create_app():
    app = Flask(__name__)

    # 日志过滤器，添加id
    class RequestIDFilter(logging.Filter):
        def filter(self, record):
            record.request_id = request.environ.get('REQUEST_ID', 'unknown')
            return True

    # 日志格式化
    formatter = logging.Formatter('%(asctime)s - %(request_id)s - %(name)s - %(levelname)s - %(message)s')

    # 配置日志记录器
    app.logger.setLevel(logging.INFO)

    # 创建一个handler，用于写入日志文件
    file_handler = RotatingFileHandler('app/logs/app.log', maxBytes=10240, backupCount=3)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(RequestIDFilter())  # 添加过滤器
    app.logger.addHandler(file_handler)

    app.config.from_object(Config)  # 加载配置
    db.init_app(app)  # 初始化数据库
    app.register_blueprint(routes)  # 注册路由
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
