# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.cartoongan_pt import adapter as cartoongan_pt_adapter


class CartoonganPtHayaoFuncWorker(BaseFuncWorker):
    """CartoonganPt Hayao 引擎子进程
    """

    def __init__(self, daemon=True):
        super(CartoonganPtHayaoFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_cartoon", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "hyo", "vip": 0,
                "icon": "/static/ui_data/modules/ctg/hayao.jpg",
                "func_class": "fc_art",
                "func_name": "hayao",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        '''
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "hyo", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ctg/hayao.jpg",
                "func_class": "fc_fun",
                "func_name": "hayao",
                "func_params": []
            }]
        })
        '''

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = cartoongan_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = cartoongan_pt_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['cartoongan_pt']['gpu_id'],
                          style='Hayao')


class CartoonganPtHosodaFuncWorker(BaseFuncWorker):
    """CartoonganPt Hosoda 引擎子进程
    """

    def __init__(self, daemon=True):
        super(CartoonganPtHosodaFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_cartoon", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "hsd", "vip": 1,
                "icon": "/static/ui_data/modules/ctg/hosoda.jpg",
                "func_class": "fc_art",
                "func_name": "hosoda",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "hsd", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ctg/hosoda.jpg",
                "func_class": "fc_fun",
                "func_name": "hosoda",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = cartoongan_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = cartoongan_pt_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['cartoongan_pt']['gpu_id'],
                          style='Hosoda')


class CartoonganPtPaprikaFuncWorker(BaseFuncWorker):
    """CartoonganPt Paprika 引擎子进程
    """

    def __init__(self, daemon=True):
        super(CartoonganPtPaprikaFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_cartoon", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "ppk", "vip": 1,
                "icon": "/static/ui_data/modules/ctg/paprika.jpg",
                "func_class": "fc_art",
                "func_name": "paprika",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "ppk", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ctg/paprika.jpg",
                "func_class": "fc_fun",
                "func_name": "paprika",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = cartoongan_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = cartoongan_pt_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['cartoongan_pt']['gpu_id'],
                          style='Paprika')


class CartoonganPtShinkaiFuncWorker(BaseFuncWorker):
    """CartoonganPt Shinkai 引擎子进程
    """

    def __init__(self, daemon=True):
        super(CartoonganPtShinkaiFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_cartoon", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "snk", "vip": 1,
                "icon": "/static/ui_data/modules/ctg/shinkai.jpg",
                "func_class": "fc_art",
                "func_name": "shinkai",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "snk", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ctg/shinkai.jpg",
                "func_class": "fc_fun",
                "func_name": "shinkai",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = cartoongan_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = cartoongan_pt_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['cartoongan_pt']['gpu_id'],
                          style='Shinkai')
