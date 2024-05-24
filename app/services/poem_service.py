#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:31
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : poem_service.py
# 功能描述  ：诗词服务
from sqlalchemy import func, or_
from ..models import Poems
from ..utils import model_to_dict


def _get_one_random_poem():
    """
    随机返回一首古诗
    :return:
    """
    poem = model_to_dict(Poems.query.filter(Poems.zhailu != '').order_by(func.rand()).first())

    return poem


def _get_poem_by_id(poem_id):
    """
    根据id查询古诗
    :param poem_id:
    :return:
    """
    poem = model_to_dict(Poems.query.get(poem_id))
    return poem


def _get_all_poems():
    """
    返回所有古诗
    :return:
    """
    poems = Poems.query.all()
    poems_list = [model_to_dict(poem) for poem in poems]
    return poems_list


def _search(q):
    """
    根据关键字q，模糊搜索poems的title、author、content，返回匹配到的结果
    :param q:入参 搜索关键字
    :return:
    """
    poems = Poems.query.filter(
        or_(
            Poems.title.like(f'%{q}%'),
            Poems.author.like(f'%{q}%'),
            Poems.content.like(f'%{q}%')
        )
    ).all()
    poems_list = [model_to_dict(poem) for poem in poems]
    return poems_list
