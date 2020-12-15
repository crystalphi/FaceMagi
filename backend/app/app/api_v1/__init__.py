from flask import Blueprint, jsonify, request, url_for

api = Blueprint('api', __name__)

# 导入各单文件子模块的 Blueprint 接口
from . import \
    authentication, \
    configs, \
    files, \
    media, \
    orders, \
    users, \
    wxpay, \
    wxtools

# 导入各 AI 目录子模块的 Blueprint 接口
#from .ai_modules.mnist import adapter
#from .ai_modules.attgan_pt import adapter
#from .ai_modules.beautygan import adapter
