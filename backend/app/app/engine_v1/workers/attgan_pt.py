# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.attgan_pt import adapter as attgan_pt_adapter


class AttganPtFuncWorker(BaseFuncWorker):
    """attgan_pt 引擎子进程
    支持 13 种特性：Bald, Bangs, Black_Hair, Blond_Hair, Brown_Hair, Bushy_Eyebrows, Eyeglasses, Male, Mouth_Slightly_Open, Mustache, No_Beard, Pale_Skin, Young
    """

    def __init__(self, daemon=True):
        super(AttganPtFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = []
        '''
        self._func_info_list.append({
            "func_group": "impression", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "white face", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_editor",
                "func_name": ["Pale_Skin"],
                "func_params": ([0.9], ["face"])
            }]
        })
        self._func_info_list.append({
            "func_group": "age", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "age", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_editor",
                "func_name": ["Young"],
                "func_params": ([0.9], ["face"])
            }]
        })
        '''
        self._func_info_list.append({
            "func_group": "hair", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "blond", "vip": 0,
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_editor",
                "func_name": ["Blond_Hair"], # 列表，可以同时多个；下面的强度参数应一致
                "func_params": ([1.0], ["hair"]) # 处理强度（0~1），编辑区域
                # 人脸编辑区域取值可参考 face_parsing/adapter.py
            }, {
                "name": "brown", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_editor",
                "func_name": ["Brown_Hair"],
                "func_params": ([1.0], ["hair"])
            }, {
                "name": "black", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_editor",
                "func_name": ["Black_Hair"],
                "func_params": ([1.0], ["hair"])
            }]
        })
        '''
        self._func_info_list.append({
            "func_group": "hair", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{ # 效果不好
                "name": "bangs", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_editor",
                "func_name": ["Bangs"],
                "func_params": ([1.0], ["hair", "face"])
            }]
        })
        '''
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "age", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": ["Young"],
                "func_params": ([0.9], ["face"])
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = attgan_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = attgan_pt_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['attgan_pt']['gpu_id'])
    