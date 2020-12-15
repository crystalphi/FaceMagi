# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.deep_feat_interp import adapter as deep_feat_interp_adapter


class DeepFeatInterpFuncWorker(BaseFuncWorker):
    """deep_feat_interp 引擎子进程
    处理较慢，主要用于 Fun"""

    def __init__(self, daemon=True):
        super(DeepFeatInterpFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "age", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "d-young", "vip": 0,
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_editor",
                "func_name": "younger",
                "func_params": [2.0]
            }, {
                "name": "d-older", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_editor",
                "func_name": "older",
                "func_params": [2.0]
            }]
        }, {
            "func_group": "impression", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "d-smiling", "vip": 0, # bad
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_editor",
                "func_name": "Smiling",
                "func_params": [2.0]
            }, {
                "name": "d-sunglasses", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_editor",
                "func_name": "sunglasses",
                "func_params": [2.0]
            }]
        }, {
            "func_group": "beards_m", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "d-facehair", "vip": 0,
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_editor",
                "func_name": "facehair",
                "func_params": [2.5] # 处理强度
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "d-senior", "vip": 0,
                "sex": "all", # 适合性别：male/female/all（只在 __fun 中才需加上）
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "senior",
                "func_params": [2.0]
            }, {
                "name": "d-younger", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "younger",
                "func_params": [2.0]
            }, {
                "name": "d-older", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "older",
                "func_params": [2.0]
            }, {
                "name": "d-eye-glasses", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "Eyeglasses",
                "func_params": [2.0]
            }, {
                "name": "d-sunglasses", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "sunglasses",
                "func_params": [2.0]
            }, {
                "name": "d-child", "vip": 0, # bad
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "child",
                "func_params": [2.0]
            }, {
                "name": "d-baby", "vip": 0, # bad
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "baby",
                "func_params": [2.0]
            }, {
                "name": "d-shiny-skin", "vip": 0, # bad
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "shiny_skin",
                "func_params": [2.0]
            }, {
                "name": "d-strong-lines", "vip": 0, # good
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "strong_nose_mouth_lines",
                "func_params": [2.0]
            }, {
                "name": "d-asian", "vip": 0, # good
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "asian",
                "func_params": [2.0]
            }, {
                "name": "d-white", "vip": 0, # good
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "white",
                "func_params": [2.0]
            }, {
                "name": "d-facehair", "vip": 0,
                "sex": "all", # male/female/all
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "facehair",
                "func_params": [1.5]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = deep_feat_interp_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = deep_feat_interp_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['deep_feat_interp']['gpu_id'])
    