# -*- coding: utf-8 -*-
""" Flask server with Deep Learning model.
"""
__author__ = "vedasky"
__copyright__ = "Copyright 2019"

import os
import logging
import sys, traceback
import pymysql
from flask import Flask, current_app, render_template, jsonify, request
from flask import g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#BASE_DIR = os.path.join(os.path.dirname(
#    os.path.dirname(os.path.abspath(__file__))), "..")
#sys.path.append(BASE_DIR)

from .config import config
from .engine_v1.m_client import ManagerClient

# 数据库
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

# 登录模块
login_manager = LoginManager()
login_manager.session_protection = 'strong'  # 'basic' or 'strong'
login_manager.login_view = 'auth.login'

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app(config_name="default"):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 接口访问速率限制
    """
    默认限制器
    key_func 参数是判断函数,表示以何种条件判断算一次访问
    default_limits 是一个数组,用于依次提同判断条件.比如100/day是指一天100次访问限制.
    常用的访问限制字符串格式如下:
      10 per hour
      10/hour
      10/hour;100/day;2000 per year
      100/day, 500/7days
    注意：默认的限制器对所有视图都有效，除非自定义一个限制器覆盖默认限制器，或者使用 limiter.exempt 装饰器来取消限制
    """
    app.limiter = Limiter(
        app,
        key_func=get_remote_address, # 根据访问者的IP记录访问次数
        default_limits=["10800 per hour", "16 per second"] # 默认限制
    )
    ''' 3种基本用法：
    @app.route("/some_api")
    (1) @app.limiter.limit("1 per day") # 自定义访问速率
    (2) @app.limiter.exempt # 无访问速率限制
    (3) # 不加该修饰则表示使用默认限制
    
    更多用法示例：
    @app.limiter.limit("100/30seconds", error_message=json.dumps({"data": "You hit the rate limit", "error": 429}))
    @app.limiter.limit("100/day;10/hour;1/minute")
    
    动态共享限制：
    host_limit = app.limiter.shared_limit("2/hour", scope=host_scope)
    @host_limit

    还可以将访问记录存储在 mysql 或者 redis 数据库中。
    '''

    app.logger.setLevel(logging.INFO)
    app.logger.info('')
    app.logger.info('-' * 40)
    app.logger.info('- Start Flask Server')
    app.logger.info('-' * 40)

    # ---------- 所需各依赖项注册（有则必须）----------

    # 将扩展对象绑定到应用上
    db.init_app(app)
    #app.logger.info('SQLALCHEMY_DATABASE_URI:' + app.config['SQLALCHEMY_DATABASE_URI'])
    login_manager.init_app(app)

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})

    with app.app_context():
        # 初始化引擎管理进程访问接口模块
        app.logger.info('init app.mm_client...')
        app.mm_client = ManagerClient()
        app.logger.info('app.mm_client is alive: {}'
                        .format(app.mm_client.is_alive())) # 执行时若异常会重连一次
        # 初始化超解析引擎
        #app.logger.info('init app.esrgan...')
        #from .engine_v1.utils.esrgan import adapter as esrgan_adapter
        #app.esrgan = esrgan_adapter.init_model(gpu_id=0)

        # ---------- 注册各应用蓝图（有则必须）----------

        # 注册主程序蓝本，解决路由和自定义错误页面处理程序
        from .main import main as main_blueprint
        app.register_blueprint(main_blueprint)

        # 注册授权服务蓝本
        from .auth import auth as auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        # 注册REST Web服务蓝本
        from .api_v1 import api as api_v1_blueprint
        app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

        app.logger.info("[*] register blueprint DONE.")

    # ---------- 定义全局页面（可选）----------

    # 使用自定义 404 页面
    @app.errorhandler(404)
    def error_404(error):
        response = dict(status=0, message="404 Not Found")
        return jsonify(response), 404

    # ---------- 定义子应用演示页面（可选）----------

    @app.route("/demo/v1/mnist", methods=["GET"])
    def v1_demo_mnist():
        return render_template("demo/mnist.html")

    @app.route("/demo/v1/attgan_pt", methods=["GET"])
    def v1_demo_attgan_pt():
        return render_template("demo/attgan_pt.html")

    # ---------- Flask App 初始化完毕 ----------

    app.logger.info("[*] Flask app created for {0} DONE!".format(config_name))
    return app
