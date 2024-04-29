#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 11:32
# @Author  : Stepheng
# @Email   : 1142262478@qq.com
# @File    : user_service.py
# 功能描述  ：用户服务
import requests
from ..config import Config


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

