#!/usr/bin/env python
# coding=utf-8

from flask import g, jsonify, request, current_app, url_for
from datetime import datetime
from PIL import Image
from io import BytesIO
import os
import requests
import json
import base64
import traceback
from xml.etree import cElementTree as ET

from . import api
from .. import db
from ..models import User


@api.route('/wx_getwxacode', methods=['GET'])
def wx_getwxacode():
    out = {}

    try:
        res = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'
                           % (current_app.config['APP_ID'], current_app.config['SECRET_KEY']))
        print('get token res.content:', res.content)
        res = json.loads(res.content)
        token = res['access_token']

        path = request.args.get('path')
        path = base64.b64decode(path).decode()
        print('--> [%d chars] path: %s' % (len(path), path))
        if len(path) > 128:  # path 不能大于128字符
            path = 'page/mate/index/index'
        data = {
            'path': path,
            'width': 430
        }
        baseUrl = 'https://api.weixin.qq.com/wxa/getwxacode'  # 获取小程序码
        # baseUrl = 'https://api.weixin.qq.com/cgi-bin/wxaapp/createwxaqrcode'  # 获取小程序二维码
        res = requests.post(baseUrl + '?access_token=%s' %
                            token, data=json.dumps(data))
        # 返回的 res.content 即图片的二进制数据
        # print('create code image res.content[:100]: %s' % res.content[:100])

        # 直接将图片内容编码输出
        # out['b64image'] = base64.b64encode(res.content)

        # 或将图片保存为文件，返回文件地址
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = os.path.join(BASE_DIR, "upload/images/")
        image_file = g.current_user.openId + '-qrcode.png'
        image_file_path = image_path + image_file
        if os.path.exists(image_path) == False:
            os.mkdir(image_path)
        wx_code = Image.open(BytesIO(res.content))
        wx_code.save(image_file_path)
        print('--> save qrcode image to %s' % image_file_path)
        out['image_file'] = image_file

    except Exception as e:
        out['err'] = str(e)
        # print(repr(e))
        traceback.print_exc()

    return jsonify(out)
