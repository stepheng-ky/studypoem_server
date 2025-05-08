#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 18:21
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : footprints_service.py
# 功能描述  ：诗词服务
from sqlalchemy import func, or_
from ..models import Footprints
from ..utils import model_to_dict



def _get_all_footprints():
    """
    返回所有足迹
    :return:
    """
    footprints = Footprints.query.all()
    footprints_list = [model_to_dict(footprint) for footprint in footprints]
    return footprints_list

