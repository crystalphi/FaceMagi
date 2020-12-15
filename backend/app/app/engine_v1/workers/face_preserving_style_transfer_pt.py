# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.face_preserving_style_transfer_pt import adapter as face_preserving_style_transfer_pt_adapter


class FacePreservingStyleTransferPtMangaFuncWorker(BaseFuncWorker):
    """face_preserving_style_transfer_pt manga-face 引擎子进程
    """

    def __init__(self, daemon=True):
        super(FacePreservingStyleTransferPtMangaFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_styles_1", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "manga-p", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_art",
                "func_name": "manga-p",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "manga", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_fun",
                "func_name": "manga",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_preserving_style_transfer_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_preserving_style_transfer_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['gpu_id'],
                  style='manga-face')


class FacePreservingStyleTransferPtMosaicFuncWorker(BaseFuncWorker):
    """face_preserving_style_transfer_pt mosaic-face 引擎子进程
    """

    def __init__(self, daemon=True):
        super(FacePreservingStyleTransferPtMosaicFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_styles_1", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "mosaic", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_art",
                "func_name": "mosaic",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "mosaic", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_fun",
                "func_name": "mosaic",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_preserving_style_transfer_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_preserving_style_transfer_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['gpu_id'],
                  style='mosaic-face')


class FacePreservingStyleTransferPtGrandeJatteFuncWorker(BaseFuncWorker):
    """face_preserving_style_transfer_pt grande-jatte 引擎子进程
    """

    def __init__(self, daemon=True):
        super(FacePreservingStyleTransferPtGrandeJatteFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_styles_1", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "grande-jatte", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_art",
                "func_name": "grande-jatte",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "grande-jatte", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_fun",
                "func_name": "grande-jatte",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_preserving_style_transfer_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_preserving_style_transfer_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['gpu_id'],
                  style='grande-jatte')


class FacePreservingStyleTransferPtRainsRustleFuncWorker(BaseFuncWorker):
    """face_preserving_style_transfer_pt rains-rustle 引擎子进程
    """

    def __init__(self, daemon=True):
        super(FacePreservingStyleTransferPtRainsRustleFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_styles_1", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "rains-rustle", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_art",
                "func_name": "rains-rustle",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "rains-rustle", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_fun",
                "func_name": "rains-rustle",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_preserving_style_transfer_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_preserving_style_transfer_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['gpu_id'],
                  style='rains-rustle')


class FacePreservingStyleTransferPtStaryNightFuncWorker(BaseFuncWorker):
    """face_preserving_style_transfer_pt stary-night 引擎子进程
    """

    def __init__(self, daemon=True):
        super(FacePreservingStyleTransferPtStaryNightFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_styles_1", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "stary-night", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_art",
                "func_name": "stary-night",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "stary-night", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_fun",
                "func_name": "stary-night",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_preserving_style_transfer_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_preserving_style_transfer_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['gpu_id'],
                  style='stary-night')


class FacePreservingStyleTransferPtWaveFuncWorker(BaseFuncWorker):
    """face_preserving_style_transfer_pt wave 引擎子进程
    """

    def __init__(self, daemon=True):
        super(FacePreservingStyleTransferPtWaveFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        self._func_info_list = [{
            "func_group": "__art_styles_1", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "wave", "vip": 0,
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_art",
                "func_name": "wave",
                "func_params": []
            }]
        }]
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "wave", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/face_demo/4.jpg",
                "func_class": "fc_fun",
                "func_name": "wave",
                "func_params": []
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_preserving_style_transfer_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_preserving_style_transfer_pt_adapter.init_model(
                  gpu_id=app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['gpu_id'],
                  style='wave')
