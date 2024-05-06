#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:32
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : user_service.py
# 功能描述  ：用户服务
import requests

from .plan_service import _get_plan_by_id
from ..config import Config
from ..models import Users, UserPlans
from ..utils import model_to_dict


def _get_openid(code):
    """
    根据code返回微信的openid和session_key
    小程序可以通过getUserInfo直接获取用户信息，https://developers.weixin.qq.com/miniprogram/dev/api/open-api/user-info/wx.getUserInfo.html
    :param code:
    :return:
    """
    APPID = Config.APPID
    APPSECRET = Config.APPSECRET
    WX_API_URL = Config.WX_API_URL
    url = f"{WX_API_URL}/sns/jscode2session?appid={APPID}&secret={APPSECRET}&js_code={code}&grant_type=authorization_code"
    # 发起请求
    response = requests.get(url)
    result = response.json()
    print(f'result:{result}')
    return result


def _get_user_plans_by_user_id(user_id):
    """
    根据user_id返回用户的学习计划列表
    """
    plans = [model_to_dict(plan) for plan in UserPlans.query.filter_by(user_id=user_id)]
    for plan in plans:
        plan['plan_name'] = _get_plan_by_id(plan['plan_id'])['plan_name']
    return plans
