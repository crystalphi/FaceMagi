# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.facelet_pt import adapter as facelet_pt_adapter


class FaceletPtFeminizationFuncWorker(BaseFuncWorker):
    """facelet_pt 引擎子进程 - feminization"""

    def __init__(self, daemon=True):
        super(FaceletPtFeminizationFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "impression", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "feminize", "vip": 0,
                "icon": "/static/ui_data/face_demo/1.jpg",
                "func_class": "fc_editor",
                "func_name": "feminization",
                "func_params": [6] # 处理强度
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "feminize", "vip": 0,
                "sex": "all", # 适合性别：male/female/all（只在 __fun 中才需加上）
                "icon": "/static/ui_data/face_demo/1.jpg",
                "func_class": "fc_fun",
                "func_name": "feminization",
                "func_params": [8]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = facelet_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = facelet_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['facelet_pt_feminization']['gpu_id'],
                  effect='feminization')
    

class FaceletPtMasculinizationFuncWorker(BaseFuncWorker):
    """facelet_pt 引擎子进程 - masculinization"""

    def __init__(self, daemon=True):
        super(FaceletPtMasculinizationFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "impression", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "masculinize", "vip": 0,
                "icon": "/static/ui_data/face_demo/1.jpg",
                "func_class": "fc_editor",
                "func_name": "masculinization",
                "func_params": [6] # 处理强度
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "masculinize", "vip": 0,
                "sex": "all", # 适合性别：male/female/all（只在 __fun 中才需加上）
                "icon": "/static/ui_data/face_demo/1.jpg",
                "func_class": "fc_fun",
                "func_name": "masculinization",
                "func_params": [8]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = facelet_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = facelet_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['facelet_pt_masculinization']['gpu_id'],
                  effect='masculinization')
    

class FaceletPtOlderFuncWorker(BaseFuncWorker):
    """facelet_pt 引擎子进程 - older"""

    def __init__(self, daemon=True):
        super(FaceletPtOlderFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "age", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "older", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_editor",
                "func_name": "older",
                "func_params": [6] # 处理强度
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "older", "vip": 0,
                "sex": "all", # 适合性别：male/female/all（只在 __fun 中才需加上）
                "icon": "/static/ui_data/face_demo/1.jpg",
                "func_class": "fc_fun",
                "func_name": "older",
                "func_params": [8]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = facelet_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = facelet_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['facelet_pt_older']['gpu_id'],
                  effect='older')
    

class FaceletPtYoungerFuncWorker(BaseFuncWorker):
    """facelet_pt 引擎子进程 - younger"""

    def __init__(self, daemon=True):
        super(FaceletPtYoungerFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "age", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "younger", "vip": 0,
                "icon": "/static/ui_data/face_demo/3.jpg",
                "func_class": "fc_editor",
                "func_name": "younger",
                "func_params": [6] # 处理强度
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "younger", "vip": 0,
                "sex": "all", # 适合性别：male/female/all（只在 __fun 中才需加上）
                "icon": "/static/ui_data/face_demo/3.jpg",
                "func_class": "fc_fun",
                "func_name": "younger",
                "func_params": [8]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = facelet_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = facelet_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['facelet_pt_younger']['gpu_id'],
                  effect='younger')
    

class FaceletPtFacehairFuncWorker(BaseFuncWorker):
    """facelet_pt 引擎子进程 - facehair"""

    def __init__(self, daemon=True):
        super(FaceletPtFacehairFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = []
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "facehair", "vip": 0,
                "sex": "all", # 适合性别：male/female/all（只在 __fun 中才需加上）
                "icon": "/static/ui_data/face_demo/2.jpg",
                "func_class": "fc_fun",
                "func_name": "facehair",
                "func_params": [7]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = facelet_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = facelet_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['facelet_pt_facehair']['gpu_id'],
                  effect='facehair')
    