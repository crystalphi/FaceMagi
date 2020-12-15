# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.face_makeup_pt import adapter as face_makeup_pt_adapter


class FaceMakeupPtFuncWorker(BaseFuncWorker):
    """face_makeup_pt 引擎子进程"""

    def __init__(self, daemon=True):
        super(FaceMakeupPtFuncWorker, self).__init__(daemon)
        self.__icon_dir = face_makeup_pt_adapter.SAVE_ICON_DIR
        self.__icon_dir = self.__icon_dir[self.__icon_dir.index('/static'):]

        # 引擎功能函数注册信息
        self._func_info_list = []
        self._func_info_list.append({
            "func_group": "hair", # 更改发色（必须在预定义类型中，否则将被拒绝注册）
            "func_list": [{
                "name": "red", "vip": 0,
                "icon": self.__icon_dir + "/red_hair.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['red_hair', ['hair'], [0, 38, 255]] # b,g,r
            }, {
                "name": "blue", "vip": 0,
                "icon": self.__icon_dir + "/blue_hair.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['blue_hair', ['hair'], [250, 10, 10]] # b,g,r
            }, {
                "name": "sky blue", "vip": 1,
                "icon": self.__icon_dir + "/sky_hair.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['sky_hair', ['hair'], [255, 213, 117]] # b,g,r
            }, {
                "name": "green", "vip": 0,
                "icon": self.__icon_dir + "/green_hair.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['green_hair', ['hair'], [10, 250, 10]] # b,g,r
            }, {
                "name": "lemon", "vip": 0,
                "icon": self.__icon_dir + "/lemon_hair.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['lemon_hair', ['hair'], [0, 251, 254]] # b,g,r
            }, {
                "name": "magenta", "vip": 1,
                "icon": self.__icon_dir + "/magenta_hair.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['magenta_hair', ['hair'], [255, 64, 255]] # b,g,r
            }]
        })
        self._func_info_list.append({
            "func_group": "alien", # 更改肤色（必须在预定义类型中，否则将被拒绝注册）
            "func_list": [{
                "name": "red", "vip": 0, # 红色
                "icon": self.__icon_dir + "/red.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['red', ['skin'], [20, 20, 230]]
            }, {
                "name": "hawk", "vip": 0, # 浩克
                "icon": self.__icon_dir + "/hawk.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['hawk', ['skin'], [20, 230, 50]]
            }, {
                "name": "avatar", "vip": 1, # 阿凡达
                "icon": self.__icon_dir + "/avatar.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['avatar', ['skin'], [230, 50, 20]] # 功能名，编辑区域，颜色
            }, {
                "name": "jade", "vip": 1, # 银白色
                "icon": self.__icon_dir + "/jade.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['jade', ['skin'], [210, 210, 210]]
            }, {
                "name": "golden", "vip": 1, # 金色
                "icon": self.__icon_dir + "/golden.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['golden', ['skin'], [132, 227, 255]]
            }]
        })
        '''
        self._func_info_list.append({
            "func_group": "makeup_f", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "red lips", "vip": 0,
                "icon": self.__icon_dir + "/red_lips.jpg",
                "func_class": "fc_editor",
                "func_name": "chg_color",
                "func_params": ['red_lips', ['u_lip', 'l_lip'], [20, 70, 180]]
            }]
        })
        '''
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "red lips", "vip": 0,
                "sex": "all",
                "icon": self.__icon_dir + "/red_lips.jpg",
                "func_class": "fc_fun",
                "func_name": "chg_color",
                "func_params": ['red_lips', ['u_lip', 'l_lip'], [20, 70, 180]] # b,g,r
            }, {
                "name": "avatar", "vip": 0,
                "sex": "all",
                "icon": self.__icon_dir + "/avatar.jpg",
                "func_class": "fc_fun",
                "func_name": "chg_color",
                "func_params": ['avatar', ['skin'], [230, 50, 20]] # b,g,r
            }, {
                "name": "blue hair", "vip": 0,
                "sex": "all",
                "icon": self.__icon_dir + "/blue_hair.jpg",
                "func_class": "fc_fun",
                "func_name": "chg_color",
                "func_params": ['blue_hair', ['hair'], [250, 10, 10]] # b,g,r
            }, {
                "name": "magenta", "vip": 0,
                "sex": "all",
                "icon": self.__icon_dir + "/magenta_hair.jpg",
                "func_class": "fc_fun",
                "func_name": "chg_color",
                "func_params": ['magenta_hair', ['hair'], [255, 64, 255]] # b,g,r
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = face_makeup_pt_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = face_makeup_pt_adapter.init_model(
                gpu_id=app_config.ENGINE_CONFIG['face_makeup_pt']['gpu_id'])
    