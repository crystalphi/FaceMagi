#!/usr/bin/env python
# coding=utf-8

import json
import base64
import hashlib
import requests
from decimal import Decimal
from Crypto.Cipher import AES
from flask import current_app as app
from flask import request, current_app, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from app.exceptions import ValidationError

from . import auth
from .. import db
from ..models import User, Config


@auth.route('/login', methods=['GET', 'POST'])
def login():
    code = request.args.get('code')
    # app.logger.debug('--> code: %s' % code)
    encryptedData = request.args.get('encryptedData')
    rawData = request.args.get('rawData')
    signature = request.args.get('signature')
    iv = request.args.get('iv')

    # 用js_code，appid，secret，grant_type向微信服务器获取session_key,openid,expires_in
    data = {}
    data['appid'] = current_app.config['APP_ID']
    data['secret'] = current_app.config['SECRET_KEY']
    data['js_code'] = code
    data['grant_type'] = 'authorization_code'
    res = requests.get(
        'https://api.weixin.qq.com/sns/jscode2session', params=data).json()

    # app.logger.debug('--> res: %s, rawData: %s' % (res, rawData))
    if 'session_key' in res:
        session_key = res['session_key']
        openid = res['openid']
        expires_in = 7200  # 原本是在res中返回的，现在的接口中没有了，设为默认取值

        # 校验签名，判别数据完整性
        if sha1Sign(session_key, rawData) != signature:
            raise ValidationError('Invalid rawData!')

        # 解密加密数据，校验appid
        if decrypt(session_key, encryptedData, iv) != data['appid']:
            raise ValidationError('Invalid encryptedData!')

        # 默认是老客户
        is_first = False

        # 根据openid是否插入用户
        user = User.query.filter_by(openId=openid).first()
        if user is None:
            app.logger.info('add user: %s' % rawData)
            is_first = True
            rData = json.loads(rawData)
            user = User(openId=openid,
                        nickName=rData['nickName'],
                        gender=rData['gender'],
                        city=rData['city'],
                        province=rData['province'],
                        country=rData['country'],
                        avatarUrl=rData['avatarUrl'],
                        cashbox=0)
            db.session.add(user)
            db.session.commit()

        # 登录用户，并返回由openid和SECRET_KEY构成的token
        login_user(user, True)
        token = user.generate_auth_token(expiration=expires_in)
        app.logger.debug('token: %s' % token)
        return jsonify({'userId': user.id, 'is_first': is_first, 'cashbox': str(user.cashbox), 'token': token, 'expiration': expires_in})

    return str(res)


@auth.route('/secret')
# @login_required
def secret():
    return 'only authenticated users are allowed!'


# 验签数据
def sha1Sign(session_key, rawData):
    # print(rawData.encode('utf-8'))
    data = '%s%s' % (rawData, session_key)
    return hashlib.sha1(data.encode('utf-8')).hexdigest()


# 解密加密数据，获取watermark中的appid
def decrypt(session_key, encryptedData, iv):
    sessionKey = base64.b64decode(session_key)
    encryptedData = base64.b64decode(encryptedData)
    iv = base64.b64decode(iv)

    cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
    s = cipher.decrypt(encryptedData)
    decrypted = json.loads(s[:-ord(s[len(s)-1:])])
    print(decrypted)

    return decrypted['watermark']['appid']
