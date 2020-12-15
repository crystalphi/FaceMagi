# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.beautygan import adapter as beautygan_adapter


class BeautyganFuncWorker(BaseFuncWorker):
    """智能美妆引擎子进程"""

    def __init__(self, daemon=True):
        super(BeautyganFuncWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        ''' beautygan 的 func_name 取值为如下图片的文件名称：
        .../beautygan/imgs/makeup/bright-b01.png
        .../beautygan/imgs/makeup/dark-d01.png
        .../beautygan/imgs/makeup/nature-n03.png
        '''
        all_face_area = ['face', 'l_brow', 'r_brow', #'l_eye', 'r_eye', 
                         'l_ear', 'r_ear', 'nose', 'teeth', 'u_lip', 'l_lip']
        # 引擎功能函数注册信息
        self._func_info_list = []
        all_styles = beautygan_adapter.get_all_styles()
        style_categories = set()
        for i in all_styles:
            _category, _style = i.split('-')
            style_categories.add(_category)
        for _category in style_categories:
            _func_info = {
                "func_group": _category, # 必须在预定义类型中，否则将被拒绝注册
                "func_list": []
            }
            _s_idx = 0
            for i in sorted(all_styles.keys()):
                _c, _s = i.split('-')
                if _c == _category:
                    _vip = 0 if _s_idx in range(2) or _s_idx % 6 == 0 else 1
                    _func_info["func_list"].append({
                        "name": _s, "vip": _vip,
                        "icon": "/static/ui_data/modules/btg/{}.jpg".format(i),
                        "func_class": "fc_editor",
                        "func_name": i,
                        "func_params": [1.0, all_face_area]
                    })
                    _s_idx += 1
            self._func_info_list.append(_func_info)
        
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "bright", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/btg/bright-b10.jpg",
                "func_class": "fc_fun",
                "func_name": "bright-b10",
                "func_params": [1.0, all_face_area]
            }, {
                "name": "dark", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/btg/dark-d12.jpg",
                "func_class": "fc_fun",
                "func_name": "dark-d12",
                "func_params": [1.0, all_face_area]
            }, {
                "name": "nature", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/btg/nature-n10.jpg",
                "func_class": "fc_fun",
                "func_name": "nature-n10",
                "func_params": [1.0, all_face_area]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = beautygan_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = beautygan_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['beautygan']['gpu_id'])
    