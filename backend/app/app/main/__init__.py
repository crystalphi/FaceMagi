from flask import current_app, Blueprint, render_template
from flask_restful import Api, Resource, reqparse


main = Blueprint('default', __name__)


# 方式1示例：采用 Api 模块添加资源模式
from .hello import Hello
api_main = Api(main)
api_main.add_resource(Hello, '/')


# 方式2示例：采用 route 定义，或错误句柄注册模式
from . import views, errors
