#!/usr/bin/env python
# coding=utf-8

from . import db, login_manager
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from app.exceptions import ValidationError


####### class User --> table users
class User(UserMixin, db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  openId = db.Column(db.String(50), unique=True, nullable=False) # 即客户端 user_id
  brandModel = db.Column(db.String(50), nullable=False) # 设备品牌、型号，逗号分隔
  screen = db.Column(db.String(20)) # 屏幕像素率、宽、高，逗号分隔
  language = db.Column(db.String(40)) # 使用语言
  version = db.Column(db.String(40)) # 开发包版本
  platformSystem = db.Column(db.String(40)) # 系统平台、版本，逗号分隔
  appleUser = db.Column(db.String(50))
  cashbox = db.Column(db.Numeric(8,2), default=0.0)
  orders = db.relationship('Order', backref='user', lazy='dynamic')
  cTimestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
  level = db.Column(db.Integer, default=0)  # 用户等级
  levelExpTimestamp = db.Column(db.DateTime, default=datetime.utcnow())  # 用户等级到期时间

  def __repr__(self):
    return 'User %r' % self.brandModel

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_user = {
      'uri'   : url_for('api.get_user', id=self.id, _external=True),
      'openId'  : self.openId,
      'brandModel'  : self.brandModel,
      'screen'  : self.screen,
      'language'  : self.language,
      'version'  : self.version,
      'platformSystem'  : self.platformSystem,
      'appleUser'  : self.appleUser,
      'cashbox' : str(self.cashbox),
      'cTimestamp': self.cTimestamp.strftime('%Y-%m-%d'),
      'level' : str(self.level),
      'levelExpTimestamp': self.levelExpTimestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    return json_user

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_user):
    openId = json_user.get('openId')
    brandModel = json_user.get('brandModel')
    screen = json_user.get('screen')
    language = json_user.get('language')
    version = json_user.get('version')
    platformSystem = json_user.get('platformSystem')
    appleUser = json_user.get('appleUser')
    cashbox = Decimal(json_user.get('cashbox'))
    level = int(json_user.get('level'))
    levelExpTimestamp = datetime.strptime(json_user.get('levelExpTimestamp'), "%Y-%m-%d %H:%M:%S")
#    if body is None or body = '':
#      raise ValidationError('user does not hava a name')
    return User(openId=openId, brandModel=brandModel, screen=screen, language=language, 
            version=version, platformSystem=platformSystem, appleUser=appleUser, 
            cashbox=cashbox, level=level, levelExpTimestamp=levelExpTimestamp)

  # 生成初始数据
  @staticmethod
  def generate_users():
    user = User(id=1, openId='26388362-oAk3s0', brandModel='Apple,iPhoneSimulator', 
            screen='2,375,667', language='en', version='1.9.9.74105', platformSystem='ios,13.4', 
            appleUser=None, cashbox='0.0', level=0)
    db.session.add(user)
    try:
      db.session.commit()
      print('generate users successfully')
    except IntegrityError:
      db.session.rollback()
      print('fail to generate users')

  # 生成授权token
  def generate_auth_token(self, expiration=3600):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'openId': self.openId})

  # 验证授权token
  @staticmethod
  def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
      data = s.loads(token)
      print(data)
    except:
      return None
    return User.query.filter_by(openId=data['openId']).first()


# user_loader回调，用于从会话中存储的用户ID重新加载用户对象
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


####### class AnonymousUser --> no table 
class AnonymousUser(AnonymousUserMixin):
  def can(self, permissions):
    return False

  def is_administrator(self):
    return False


login_manager.anonymous_user = AnonymousUser



####### class Order --> table orders
class Order(db.Model):
  __tablename__ = 'orders'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'))
  status = db.Column(db.Integer, default=0) # 1-order, 2-consume, 3-comment
  prepayId = db.Column(db.String(64), unique=True, nullable=False)
  cTimestamp = db.Column(db.DateTime, index=True, default=datetime.now())
  uTimestamp = db.Column(db.DateTime, default=datetime.now())

  def __repr__(self):
    return 'Order: %r' % (self.prepayId)

  # 序列化转换: 资源->JSON
  def to_json(self, user=None):
    json_order = {
      'uri'   : url_for('api.get_order', id=self.id, _external=True),
      'orderId': self.id,
      'userUri': url_for('api.get_user', id=self.userId, _external=True),
      'user'  : user,
      'status' : self.status,
      'prepayId' : self.prepayId,
      'cTimestamp': self.cTimestamp.strftime('%Y-%m-%d'),
      'uTimestamp': self.uTimestamp
    }
    return json_order

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_order):
    userId = json_order.get('userId')
    status = json_order.get('status')
    prepayId = json_order.get('prepayId')
    return Order(userId=userId, status=status, prepayId=prepayId)

  # 生成初始数据
  @staticmethod
  def generate_orders():
    statuses = [1, 2, 3, 3]
    prepayIds = ['wx1', 'wx2', 'wx3', 'wx4']
    for i in range(len(statuses)):
      order = Order(id=i+1, userId=1, status=statuses[i], prepayId=prepayIds[i])
      db.session.add(order)
    try:
      db.session.commit()
      print('generate orders successfully')
    except IntegrityError:
      db.session.rollback()
      print('fail to generate orders')


####### class Config --> table config
class Config(db.Model):
  __tablename__ = 'config'
  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String(64), unique=True, nullable=False)
  value = db.Column(db.String(128), nullable=False)

  def __repr__(self):
    return 'Config: %r' % (self.key)

  # 序列化转换: 资源->JSON
  def to_json(self):
    json_config = {
      'uri'   : url_for('api.get_config', id=self.id, _external=True),
      'key' : self.key,
      'value' : self.value
    }
    return json_config

  # 序列化转换：JSON->资源
  @staticmethod
  def from_json(json_config):
    key = json_config.get('key')
    value = json_config.get('value')
    return Config(key=key, value=value)

  # 生成初始数据
  @staticmethod
  def generate_configs():
    keys = ['mch_name', 'valid_user_cash', 'invalid_user_cash']
    values = [u'FaceMagi', '2.0', '1.0']
    for i in range(len(keys)):
      config = Config(id=i+1, key=keys[i], value=values[i])
      db.session.add(config)
    try:
      db.session.commit()
      print('generate configs successfully')
    except IntegrityError:
      db.session.rollback()
      print('fail to generate configs')

