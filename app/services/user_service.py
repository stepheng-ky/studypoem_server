#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:32
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : user_service.py
# 功能描述  ：用户服务
import requests

from .plan_service import _get_plan_by_id
from ..config import Config, db
from ..models import Users, UserPlans
from ..utils import model_to_dict


def _get_openid(code, avatarUrl, nickName):
    """
    根据code返回微信的openid和session_key
    小程序可以通过getUserInfo直接获取用户信息，https://developers.weixin.qq.com/miniprogram/dev/api/open-api/user-info/wx.getUserInfo.html
    :param code:小程序临时code
    :param avatarUrl:用户头像url
    :param nickName:微信名
    :return:
    """
    APPID = Config.APPID
    APPSECRET = Config.APPSECRET
    WX_API_URL = Config.WX_API_URL
    url = f"{WX_API_URL}/sns/jscode2session?appid={APPID}&secret={APPSECRET}&js_code={code}&grant_type=authorization_code"
    # {"session_key":"mMMaFzGz5YTQ/xgUXuwBeQ==","openid":"oFzO86665d2q_kaIC_jLoSlwLTIk"}
    response = requests.get(url).json()
    # 获取openid 并判断如果不存在就存储下来
    openid = response.get('openid')
    result = {"openid": openid}
    if openid:
        source = 'wx'
        _update_or_create_user(user_id=openid, user_name=nickName, source=source, avatarUrl=avatarUrl)
    return result


def _update_or_create_user(user_id, user_name, source, avatarUrl):
    """
    根据user_id如果不存在，创建用户；如果存在更新其他字段
    :param user_id:用户id
    :param user_name：用户名
    :param source：来源
    :param avatarUrl:用户头像
    :return:
    """
    user = Users.query.get(user_id)
    print(f'入参 {user_id}：{user_name}、{source}、{avatarUrl}，user:{user}')
    if user:
        # 如果存在对应的记录，则更新其他字段
        user.user_name = user_name
        user.source = source
        user.avatarUrl = avatarUrl
        print(f'更新用户{user_id}：{user_name}、{source}、{avatarUrl}')
    else:
        # 如果不存在对应的记录，则新增一条新的记录
        new_user = Users(user_id=user_id, user_name=user_name, source=source, avatarUrl=avatarUrl)
        db.session.add(new_user)
        print(f'新增用户{user_id}：{user_name}、{source}、{avatarUrl}')
    db.session.commit()


def _get_user_plans_by_user_id(user_id):
    """
    根据user_id返回用户的学习计划列表
    """
    plans = [model_to_dict(plan) for plan in UserPlans.query.filter_by(user_id=user_id)]
    for plan in plans:
        _plan = _get_plan_by_id(plan['plan_id'])
        plan['plan_name'] = _plan['plan_name']
        plan['start_date'] = _plan['start_date']
    return plans
