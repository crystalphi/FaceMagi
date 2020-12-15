# coding=utf-8

import traceback
from datetime import datetime
from flask import current_app, request, jsonify, make_response, g
from flask_httpauth import HTTPBasicAuth

from . import api
from .. import db
from ..models import User, AnonymousUser
from .common import resp_result
from .errors import unauthorized, forbidden


auth = HTTPBasicAuth()


@api.route("/auth/user_login", methods=["POST"])
def user_login():
    """ 用户登录或注册：客户端每次打开时都需调用该接口一次。post 参数：
    1、device_info: 设备信息字符串
    2、user_id: 用户ID（若为空，则本函数中基于设备信息自定义哈希算法值+分钟级标准时间戳自动生成）
    3、vr_code: 校验码（客户端基于 user_id+标准时间戳，采用自定义哈希生成。主要目的：增加攻击调用该接口的难度）

    该接口被调用时，首先根据自定义哈希算法检查校验码是否合法；如果找到该 user_id 记录，则更新并返回；否则基于设备信息和时间戳生成 user_id，将该新登记设备信息写入数据库并返回。

    TODO: 客户端收到返回的数据后应写入本地缓存，后续调用其他限权接口时，需带上该 user_id 及相应哈希密码。

    TODO: 该记录表每几天清理一次，没有购买信息的记录可直接删除。
    """

    data = {}
    data["login_success"] = False

    try:
        user_id = request.form['user_id'] if 'user_id' in request.form else None
        device_info = request.form['device_info'] if 'device_info' in request.form else None
        # deviceInfo sample: Apple,iPhoneSimulator,2,375,667,en,1.9.9.74105,ios,13.4
        vr_code = request.form['vr_code'] if 'vr_code' in request.form else None
        print('--> device_info:', device_info)
        print('--> user_id:', user_id)
        print('--> vr_code:', vr_code)

        if not user_id:  # 新用户
            # 检查校验码后按自定义算法生成用户名
            _timestamp = get_time_stamp()
            print('--> server _timestamp:', _timestamp)
            if zzz_hash(device_info + str(_timestamp)) == vr_code:
                user_id = zzz_hash(device_info) + '-' + str(_timestamp)
                if len(User.query.filter_by(openId=user_id).all()) == 0:
                    # 写数据库，新用户记录
                    brand, model, pixelRatio, windowWidth, windowHeight, language, version, platform, system = device_info.split(',')
                    brandModel = brand + ',' + model
                    screen = pixelRatio + ',' + windowWidth + ',' + windowHeight
                    platformSystem = platform + ',' + system
                    user = User(openId=user_id, brandModel=brandModel, screen=screen, language=language, version=version, platformSystem=platformSystem, appleUser=None, cashbox=0.0, level=0)
                    db.session.add(user)
                    db.session.commit()
                    current_app.logger.info('a new user {} added!'.format(user_id))
            else:
                current_app.logger.warn('vr_code is not match! passing add user.')
        
        # TODO: 读数据库，获取用户级别、时效等相关信息
        user = User.query.filter_by(openId=user_id).first()
        if user:
            data["token"] = user.generate_auth_token(expiration=3600)
            data["login_success"] = True
            data["user_id"] = user.openId

    except Exception as e:
        current_app.logger.warn(e)
        current_app.logger.info(traceback.format_exc(limit=5))

    current_app.logger.info('user login: {}'.format(data))
    return resp_result(data)


# 授权进行的验证
@auth.verify_password
def verify_password(openid_or_token, password):
    #print('--> verify password. openid_or_token: {}, password: {}'.format(openid_or_token, password))

    if not openid_or_token or openid_or_token == '':
        print('openid_or_token is null, this is a anonymous user.')
        g.current_user = AnonymousUser()
        return False
    
    """ # 以下为根据数据库记录，对用户ID 或 token 进行校验
    user = User.verify_auth_token(openid_or_token)
    if user:
        # token登录
        print('token login')
        g.token_used = True
    else:
        user = User.query.filter_by(openId=openid_or_token).first()
        if user:
            # openId登录
            print('openid login')
            g.token_used = False
        else:
            # 非token和openId登录
            return False
    
    g.current_user = user
    print("verify_password success! token_used: {0}, user: {1}".format(g.token_used, user))
    """
    
    # 以下为根据自定义算法，使用用户 ID 和时间戳进行校验
    _timestamp = get_time_stamp()
    print('--> server _timestamp:', _timestamp)
    print('--> openid_or_token:', openid_or_token)
    print('--> password:', password)
    if not zzz_hash(openid_or_token + str(_timestamp)) == password:
        print('verify_password failed!')
        return False
    
    return True


# 授权失败返回的错误
@auth.error_handler
def auth_error():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


# FIXME: 生产环境下强制开启
# @api.before_request  # 在处理 api 请求时先执行该回调
@auth.login_required
def before_request():
    #print('--> auth.username:', auth.username())
    print('api: before request')
    if g.current_user.is_anonymous:
        return forbidden('Anonymous Account')


# 获取token
@api.route('/token')
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiratioin': 3600})


# 自定义字符串哈希算法
def zzz_hash(input, hashSeed=8087, xxx=6):
    I64BIT_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'
    hash = hashSeed

    #print('--> input:' + str(input))
    for i in input[::-1]:
        hash += (hash << 5) + ord(i)
        #print('--> hash: {}, i: {}'.format(str(hash), i))

    value = hash & 0x7FFFFFFF
    #print('--> value:' + str(value))

    retValue = ''
    while value:
        retValue += I64BIT_TABLE[value & 0x3F]
        value = value >> xxx

    return retValue


# 获取自定义时间戳字符串
def get_time_stamp():
    #_timestamp = int(datetime.utcnow().timestamp() / 60)
    #_timestamp = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT") #UTCString
    _timestamp = datetime.utcnow().isoformat() #ISOString
    _timestamp = _timestamp[0:16]
    _timestamp = _timestamp.replace(':', '-')
    return _timestamp[0:16]

