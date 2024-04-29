#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:23
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : __init__.py.py
# 功能描述  ：服务
from .poem_service import _get_one_random_poem,_get_poem_by_id,_get_all_poems
from .category_service import _get_all_categories,_get_poems_by_category_id
from .user_service import _get_openid
