# -*- coding: utf-8 -*-
""" config.py: Configurations used by Flask server.
"""
__author__ = "alvertogit"
__copyright__ = "Copyright 2019"

import os
import logging
from logging.handlers import RotatingFileHandler


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """默认环境配置"""

    DEBUG = False # 是否开启调试功能
    TESTING = False
    
    # ----- 服务器相关设置 -----

    # 设置允许终端访问的域名
    # SERVER_NAME = 'www.vedasky.cn'  # !!! 必须正确设置或不设置。否则若终端访问域名与此不一致，将全返回 404

    # 设置静态文件所在目录（代码中要访问这些内容时可以从此获取）
    STATIC_FOLDER = os.path.join(basedir, 'static')  # 最好使用绝对路径，否则位于app目录下

    # FIXME: 正式发布时改为云数据库配置（注意权限分配，关键表只读）
    # 配置 SQLAlchemy 的链接字符串
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Jdd107_MSL_DCKR@localhost/FaceMagi?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Jdd107_MSL_DCKR@backend_py_mysql_1/FaceMagi?charset=utf8mb4'
    # 配置 SQLAlchemy 的连接池大小
    SQLALCHEMY_POOL_SIZE = 5
    # 配置 SQLAlchemy 的连接超时时间
    SQLALCHEMY_POOL_TIMEOUT = 15
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_TEARDOWN = True

    # 日志相关参数
    LOG_PATH = os.path.join(basedir, 'logs')
    LOG_PATH_FLASK_ERROR = os.path.join(LOG_PATH, 'flask_error.log')
    LOG_PATH_FLASK_INFO = os.path.join(LOG_PATH, 'flask_info.log')
    LOG_PATH_ENGINE_ERROR = os.path.join(LOG_PATH, 'engine_error.log')
    LOG_PATH_ENGINE_INFO = os.path.join(LOG_PATH, 'engine_info.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 10  # 文件轮转数量

    # ----- 存储相关设置 -----

    STORAGE_TYPE = 'local'  # local, amz_s3, tc_s3?

    # local 本地存储设置
    UPLOAD_FOLDER = os.path.join(basedir, 'upload/images') # 指定上传文件存储目录
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 # 限制上传文件大小
    UPLOAD_ALLOWED_EXTS = set(['png', 'jpg', 'JPG', 'jpeg']) # 限制上传文件类型

    # 任务缓存资源，文件名称定义
    SAVE_FILE_NAME = {}
    SAVE_FILE_NAME['image_base'] = 'image_base.png' # 原始上传图片
    SAVE_FILE_NAME['image_norm'] = 'image_norm.png' # 归一化后的原始图片
    SAVE_FILE_NAME['image_temp'] = 'image_temp.png' # 最近处理后的临时图片
    SAVE_FILE_NAME['image_save'] = 'image_save.png' # 最近处理并应用的保存图片
    SAVE_FILE_NAME['face_data'] = 'face_data.pkl' # 包括人脸位置、人脸特征、以及人脸截图数据
    
    DEMO_ICON_ENABLE = True # 是否将 icon demo 人脸处理结果保存为前端菜单远程图标文件（周期更新）
    DEMO_CACHE_ENABLE = True # 是否将 app demo 图片处理结果进行缓存（周期更新，web 端将直接使用缓存）
    DEMO_CACHE_DIR = os.path.join(STATIC_FOLDER, 'cache/demo')
    DEMO_CACHE_UPDATE_TERM = 7*24*3600 # app demo 图片处理结果缓存文件更新间隔（默认 7 天）
    
    # 用于生成图标的 demo 图片哈希（只能有一个）
    #IMG_HASH_ICON_DEMO = ['32f6e7262b0e3c9b99c59f710d652b2a'] # 女性平均人脸图，超短发，400x500
    #IMG_HASH_ICON_DEMO = ['5ab1f110b3dece65753f2c650ced4c07'] # 基于上图，缩小了人脸，扩展了白边
    #IMG_HASH_ICON_DEMO = ['51349c47a64cf022db3487cd94d722ac'] # 基于上图，抠除背景，400x500
    #IMG_HASH_ICON_DEMO = ['e7d83803a60c30229c11b03472652c0a'] # 另一女性平均人脸图，576x718（4:5）
    IMG_HASH_ICON_DEMO = ['743f96e6352ae213f36840210a79d482'] # 从 thispersondoesnotexist.com 中挑选出来的，在头发颜色等效果上好于上述平均脸
    # 用于生成直接访问缓存的 demo 图片哈希（APP 前端所用的四张 demo 图片）
    # 注意：若开启保存 icon 图片函数中的边框裁剪，则哈希值会出现变化。
    #IMG_HASH_APP_DEMO = ['12d2b6c4a62be56c494324809441be41',
    #                     'c43bb231c75e199ae47a6c1a8bbc7a77',
    #                     '521a59f9a6bb46f931b703ab1d1e8653',
    #                     '23b3b3b277204289385787ab7e011364'] # 最早的四张从本地 AI 生成图片中挑选的
    IMG_HASH_APP_DEMO = ['bf1fa7a452f406d175a46826c72b059d', # 从真机或模拟器执行的值，IDE 预览不一样
                         '1f6a00d9a985b1582ca565a02864ffc7',
                         '081aae6f5487d62a3405d08bdd488135',
                         '95a0abd7ed0e24736ca649da4e83c0ee'] # 从 thispersondoesnotexist.com 中挑选出来的示例图，青年和少年男女各一
    
    # ----- 微信平台相关设置 -----

    # FIXME: 目前为“合婚占星”小程序后台信息，待修改
    API_KEY = os.environ.get('API_KEY') or '666ZhangWangLuTin00FaceMagi999'

    # APP_ID = 'wx749ba1873afde6ee' # 个人号
    APP_ID = 'wxf1d4089b16b47b77'  # 阿特玛企业号

    # SECRET_KEY = os.environ.get('SECRET_KEY') or '653808ddacdd8bdf627dbfbdff5c53ed' # 个人号
    SECRET_KEY = os.environ.get(
        'SECRET_KEY') or '3a8533a7cd665f5a17f08dc151a91961'  # 阿特玛企业号

    # 微信商户号
    MCH_ID = '1443221402'

    # ----- 安全相关设置 -----

    if os.environ.get("SECRET_KEY"):
        SECRET_KEY = os.environ.get("SECRET_KEY")
    else:
        # 强制必须设置该环境变量
        raise ValueError("SECRET KEY NOT FOUND!")

    # ----- AI 引擎相关设置 -----

    # 模型文件存储路径
    MODEL_DIR = os.environ.get("MODEL_DIR") or basedir + "/engine_v1/models_release"
    MODEL_PATH = {}
    MODEL_PATH["mnist"] = MODEL_DIR + "/mnist_model.h5"

    # 工作引擎配置信息
    ENGINE_CONFIG = {
        # 引擎名称：是否启用、GPU ID（-1 or 0,1,2,3）、进程数量、是否调试模式、是否保存图标
        # 以下为任务处理系统引擎：
        'preprocess': # 预处理引擎，必须启用（建议启动 2 个）
            {'enabled': True, 'gpu_id': -1, 'proc_num': 2, 'debug': False, 'save_icon': False},
        'cleaner': # 过期任务清理引擎，必须启用
            {'enabled': True, 'gpu_id': -1, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'esrgan': # 超解析小任务处理引擎，必须启用
            {'enabled': True, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'face_parsing': # 人脸解析小任务处理引擎，必须启用
            {'enabled': True, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        # 以下为任务处理普通引擎：
        # 建议使用 GPU 的引擎数量为 1~2 个，使用 CPU 的为 4~8 个。
        'facelet_pt_feminization': # 每进程占显存 ~2G
            {'enabled': False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'facelet_pt_masculinization': # 每进程占显存 ~2G
            {'enabled': False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'facelet_pt_older': # 每进程占显存 ~2G
            {'enabled': False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'facelet_pt_younger': # 每进程占显存 ~2G
            {'enabled': False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'facelet_pt_facehair': # 每进程占显存 ~3G
            {'enabled': False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        #'deep_feat_interp': # 默认使用 CPU，每进程占显存 0G（!!! 处理较慢，暂停使用）
        #    {'enabled': False, 'gpu_id': -1, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'attgan_pt': # 每进程占显存 ~2G（特点不突出，暂不开启）
            {'enabled': False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'beautygan': # 默认使用 CPU，每进程占显存 0G（建议启动 4 个）
            {'enabled': True, 'gpu_id': -1, 'proc_num': 2, 'debug': False, 'save_icon': False},
        'face_makeup_pt': # 只能使用默认可用 GPU，每进程占显存 ~3G
            {'enabled': True, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'ugatit': # 每进程占显存 ~1G
            {'enabled': True, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'cartoongan_pt': # 每进程占显存 ~3.6G（x3，每种风格至少一个进程）
            {'enabled': True, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        # 功能特色与下述 AST 相比，无特别突出之处，可以降低优先级
        'face_preserving_style_transfer_pt': # 每进程占显存 ~0.8G（x6，每种风格至少一个进程）
            {'enabled':  False, 'gpu_id': 0, 'proc_num': 1, 'debug': False, 'save_icon': False},
        'arbitrary_style_transfer': # 默认使用 CPU，每进程占显存 0G（建议启动 4 个）
            {'enabled': True, 'gpu_id': -1, 'proc_num': 2, 'debug': False, 'save_icon': False}
    }

    # 引擎管理进程访问参数
    EM_ADDRESS = '127.0.0.1'
    EM_PORT = 7807
    EM_AUTHKEY = b'haribol'

    # 图片尺寸参数
    OUTPUT_SIZE_EDITOR = (480, 600) # Editor 图片尺寸，也是归一化标准尺寸（w, h）, (400, 500)，(480, 600)
    OUTPUT_SIZE_FUN = (288, 360) # Fun 图片尺寸（w, h）, (240, 300)，(480, 600)
    MODEL_IMAGE_SIZE = (256, 256) # 指定输入处理引擎的最佳图片大小
    # 人脸检测引擎返回的人脸图片最小尺寸（正方形）
    FACE_MIN_SIZE = 300 # 人脸解析器的最小输出图，获取的人脸会自动扩展，此处比后续处理引擎模型尺寸稍大即可
    # 是否开启超解析处理
    #ENABLE_ESR = True # 若开启，人脸图片会缩放为标准尺寸进行处理，然后再超解析扩展为原尺寸
    ENABLE_APPLY_IMAGE_SAVE = False # 若开启，客户端点击“Apply”应用图片后，后端也会保存，以实现连续编辑功能（当前编辑功能所需的 BeautyGAN 只能支持到x256，所以采用了缩放。连续编辑会导致图片质量持续下降，故此默认关闭。#TODO: 等将来模型支持达到 384/512 后可以再开启）
    
    # 支持的人脸特征（从 CelebA 40 特征中选择）
    ATTRS_ENABLED = [
        'Bald', 'Bangs', 'Black_Hair', 'Blond_Hair', 'Brown_Hair',
        'Bushy_Eyebrows','Eyeglasses', 'Male', 'Mouth_Slightly_Open', 'Mustache',
        'No_Beard', 'Pale_Skin', 'Young'
    ]

    # 任务时间参数
    TERM_TASK_EXPIRED = 60*5 # 任务状态从新建转为过期的时间间隔（默认 5 分钟）
    TERM_TASK_CLEANED = 60*60*24 # 任务从新建到清理的时间间隔（默认 24 小时）
    MM_TASK_EXPIRED = 3 # 通过管理进程查询的小任务（如超解析、人脸解析等）过期时间（默认 3 秒）
    

    @staticmethod
    def init_app(app):
        print("### DEFAULT CONFIG ###")

    @classmethod
    def _log_init(cls, app):
        """日志模块初始化"""
        set_logger(app.logger,
                   cls.LOG_PATH_FLASK_INFO, cls.LOG_PATH_FLASK_ERROR,
                   cls.LOG_FILE_MAX_BYTES, cls.LOG_FILE_BACKUP_COUNT)


class ProdConfig(BaseConfig):
    """生产环境配置"""

    #SQLALCHEMY_DATABASE_URI = "sqlite:///sweet_heart.db"
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:Jdd107_MSL_DCKR@db.facemagi.com/FaceMagi?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Jdd107_MSL_DCKR@backend_py_mysql_1/FaceMagi?charset=utf8mb4'

    @classmethod
    def init_app(cls, app):
        print("### PRODUCTION CONFIG ###")
        cls._log_init(app)


class DevConfig(BaseConfig):
    """开发环境配置"""

    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = "sqlite:///sweet_heart.db"
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Jdd107_MSL_DCKR@backend_py_mysql_1/FaceMagi?charset=utf8mb4'

    @classmethod
    def init_app(cls, app):
        print("### DEVELOPMENT CONFIG ###")
        cls._log_init(app)


class TestConfig(BaseConfig):
    """测试环境配置"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Jdd107_MSL_DCKR@backend_py_mysql_1/FaceMagi?charset=utf8mb4'

    @classmethod
    def init_app(cls, app):
        print("### TESTING CONFIG ###")
        cls._log_init(app)


config = {
    "development": DevConfig,
    "testing": TestConfig,
    "production": ProdConfig,
    "default": ProdConfig
}


class ColoredFormatter(logging.Formatter):
    """日志颜色格式化，级别名加颜色，消息加粗"""

    #These are the sequences need to get colored ouput
    RESET_SEQ = "\033[0m"
    COLOR_SEQ = "\033[1;%dm"
    BOLD_SEQ = "\033[1m"

    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
    COLORS = {
        'WARNING':  YELLOW,
        'INFO': WHITE,
        'DEBUG': BLUE,
        'CRITICAL': YELLOW,
        'ERROR': RED
    }

    def __init__(self, fmt):
        fmt = fmt.replace("$RESET", self.RESET_SEQ).replace("$BOLD", self.BOLD_SEQ)
        logging.Formatter.__init__(self, fmt)

    def __add_color(self, levelname, msg):
        #背景色为 40 加上颜色数字，前景色为 30 加数字
        color_msg = self.COLOR_SEQ % (30 + self.COLORS[levelname]) + msg + self.RESET_SEQ
        return color_msg
        
    def format(self, record):
        if record.levelname in self.COLORS:
            # 貌似只能修改 levelname 字段，无法修改 message，其他字段未知
            record.levelname = self.__add_color(record.levelname, record.levelname)
        return logging.Formatter.format(self, record)


def set_logger(logger, filename_info, filename_error, maxBytes, backupCount):
    """设置控制台和文件回滚日志输出"""

    # 删除 Flask 默认 Handler
    del logger.handlers[:]

    # 设置终端输出日志
    # define a Handler which writes messages to the sys.stderr
    console = logging.StreamHandler()
    # set a format which is simpler for console use
    formatter = ColoredFormatter( # 终端日志加颜色
        '[%(levelname)s %(filename)s:%(lineno)s] $BOLD%(message)s$RESET')
    # tell the handler to use this format
    console.setFormatter(formatter)
    console.setLevel(logging.DEBUG)  # FIXME: 是否区分环境做不同设置？
    logger.addHandler(console)

    # 设置文件回滚日志
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(process)d '
                                  '[%(filename)s:%(lineno)s %(funcName)s] %(message)s')
    # FileHandler Info
    file_handler_info = RotatingFileHandler(filename=filename_info,
                                            maxBytes=maxBytes, backupCount=backupCount)
    file_handler_info.setFormatter(formatter)
    file_handler_info.setLevel(logging.INFO)
    logger.addHandler(file_handler_info)
    # FileHandler Error
    file_handler_error = RotatingFileHandler(filename=filename_error,
                                             maxBytes=maxBytes, backupCount=backupCount)
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)
    logger.addHandler(file_handler_error)

    logger.debug('logger init DONE.')
