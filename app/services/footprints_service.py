#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 18:21
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : footprints_service.py
# 功能描述  ：诗词服务
import os
from flask import current_app
from werkzeug.utils import secure_filename
from ..models import Footprints, FootprintsPass
from ..utils import model_to_dict
from ..config import db
from pypinyin import pinyin, Style


def _get_all_footprints():
    """
    返回所有足迹
    :return:
    """
    footprints = Footprints.query.all()
    footprints_list = [model_to_dict(footprint) for footprint in footprints]
    return footprints_list


UPLOAD_FOLDER = 'app/footprints_png'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _light_footprint(province, light_up_img, light_up_time):
    """
    点亮足迹：上传图片并保存路径到数据库
    :param province: 省份名称
    :param file: 图片文件对象
    :param light_up_time: 时间字符串
    :return: 成功或失败信息
    """
    if not allowed_file(light_up_img.filename):
        return "fail: 不支持的文件类型"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # 安全处理文件名
    province_pinyin = ''.join([i[0] for i in pinyin(province, style=Style.NORMAL)])
    filename = secure_filename(f"{province_pinyin}_{light_up_time}_{light_up_img.filename}")
    current_app.logger.info(f"filename 1 :{filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    try:
        # 保存文件到服务器
        light_up_img.save(filepath)

        # 构造相对路径（可以是相对于 uploads 的路径）
        relative_path = filepath.replace('app/', '')

        new_footprint = Footprints(
            province=province,
            light_up_img=relative_path,
            light_up_time=light_up_time
        )

        db.session.add(new_footprint)
        db.session.commit()
        return "success"
    except Exception as e:
        db.session.rollback()
        return f"fail: {str(e)}"


def _check_footprint_password(your_password):
    """
    检查密码是否正确（匹配 Footprints 表中的 password 字段）
    :param password: 密码
    :return: True 或 False
    """
    footprint = FootprintsPass.query.filter_by(password=your_password).first()
    if footprint:
        return True
    return False

