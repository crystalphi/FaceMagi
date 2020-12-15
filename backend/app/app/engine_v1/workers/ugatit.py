# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.ugatit import adapter as ugatit_adapter


class UgatitFuncWorker(BaseFuncWorker):
    """ugatit 引擎子进程
    """

    def __init__(self, daemon=True):
        super(UgatitFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_cartoon", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "ugatit", "vip": 0,
                "icon": "/static/ui_data/modules/ugatit.jpg",
                "func_class": "fc_art",
                "func_name": "ugatit",
                "func_params": []
            }]
        }]
        '''
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "ugatit", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ugatit.jpg",
                "func_class": "fc_fun",
                "func_name": "ugatit",
                "func_params": []
            }]
        })
        '''

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = ugatit_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = ugatit_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['ugatit']['gpu_id'])
    
