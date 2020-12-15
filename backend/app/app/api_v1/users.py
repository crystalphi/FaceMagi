from datetime import datetime, timedelta
from flask import jsonify, request, url_for
from decimal import Decimal

from . import api
from .. import db
from ..models import User
from .authentication import auth

#TODO: 下述 API 需要检查用户权限，只有管理员才能访问！！！


@api.route('/users')
@auth.login_required
def get_users():
    """获取所有用户列表（注意：生产环境下应关闭！）"""
    users = User.query.all()
    # return jsonify({'users' : [user.to_json() for user in users]})
    return jsonify({'total users': len(users)})


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    if user.level > 0 and datetime.utcnow() > user.levelExpTimestamp:
        user.level = 0
    return jsonify(user.to_json())


@api.route('/users', methods=['POST'])
def new_user():
    user = User.from_json(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json(), 201, {'Location': url_for('api.get_user', id=user.id, _external=True)})


@api.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get_or_404(id)
    user.name = request.json.get('name', user.name)
    db.session.add(user)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/addCash', methods=['PUT'])
def user_get_ticket(id):
    user = User.query.get_or_404(id)
    user.cashbox += Decimal(request.json.get('cash', '0.0'))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())


@api.route('/users/<int:id>/subCash', methods=['PUT'])
def user_consume_cashbox(id):
    user = User.query.get_or_404(id)
    user.cashbox -= Decimal(request.json.get('cash', '0.0'))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())


@api.route('/users/<int:id>/setLevel', methods=['PUT'])
def user_set_level(id):
    user = User.query.get_or_404(id)
    user.level = int(request.json.get('level', '0'))
    if (datetime.utcnow() > user.levelExpTimestamp):
        user.levelExpTimestamp = datetime.utcnow(
        ) + timedelta(days=int(request.json.get('days', '0')))
    else:
        user.levelExpTimestamp += timedelta(
            days=int(request.json.get('days', '0')))
    user.cashbox -= Decimal(request.json.get('price', '0.0'))
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())
