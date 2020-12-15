# -*- coding: utf-8 -*-

from app.engine_v1 import app_config, logger, image_process_wrap
from app.engine_v1.worker import BaseFuncWorker
from app.engine_v1.ai_modules.arbitrary_style_transfer import adapter as arbitrary_style_transfer_adapter


class ArbitraryStyleTransferWorker(BaseFuncWorker):
    """arbitrary_style_transfer 引擎子进程
    """

    def __init__(self, daemon=True):
        super(ArbitraryStyleTransferWorker, self).__init__(daemon)

        # 引擎功能函数注册信息
        # 根据文件名前缀分为 3 种风格：油画、版画、创意
        # painting / prints / creative
        self._func_info_list = []
        all_styles = arbitrary_style_transfer_adapter.get_all_styles()
        '''
        self._func_info_list.append({
            "func_group": "__art_styles_2", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": []
        })
        for i in sorted(all_styles.keys()):
            self._func_info_list[0]["func_list"].append({
                "name": i, "vip": 0,
                "icon": "/static/ui_data/images/ast/{}.jpg".format(i),
                "func_class": "fc_art",
                "func_name": "arbitrary_style_transfer",
                "func_params": [i]
            })
        '''
        style_categories = set()
        for i in all_styles:
            #print('--> i:', i)
            _category, _style = i.split('-')
            style_categories.add(_category)
        for _category in style_categories:
            _func_info = {
                "func_group": "__art_" + _category, # 必须在预定义类型中，否则将被拒绝注册
                "func_list": []
            }
            _s_idx = 0
            for i in sorted(all_styles.keys()):
                _c, _s = i.split('-')
                if _c == _category:
                    _vip = 0 if _s_idx in range(2) or _s_idx % 6 == 0 else 1
                    _func_info["func_list"].append({
                        "name": _s, "vip": _vip,
                        "icon": "/static/ui_data/modules/ast/{}.jpg".format(i),
                        "func_class": "fc_art",
                        "func_name": i,
                        "func_params": [i]
                    })
                    _s_idx += 1
            self._func_info_list.append(_func_info)
        
        # 以下注册 FUN 标签页功能
        self._func_info_list.append({
            "func_group": "__fun", # 必须在预定义类型中，否则将被拒绝注册
            "func_list": [{
                "name": "painting", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ast/painting-in26.jpg",
                "func_class": "fc_fun",
                "func_name": "painting-in26",
                "func_params": ["painting-in26"]
            }, {
                "name": "prints", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ast/prints-sketch.jpg",
                "func_class": "fc_fun",
                "func_name": "prints-sketch",
                "func_params": ["prints-sketch"]
            }, {
                "name": "creative", "vip": 0,
                "sex": "all",
                "icon": "/static/ui_data/modules/ast/creative-s01.jpg",
                "func_class": "fc_fun",
                "func_name": "creative-s01",
                "func_params": ["creative-s01"]
            }]
        })

        self._task_filters = self._get_tasks_filter()
        self._func_process_image = arbitrary_style_transfer_adapter.process_image
        self.logger.info("subprocess {} init DONE".format(self.name))

    def _engine_init(self):
        self._engine = arbitrary_style_transfer_adapter.init_model(
                          gpu_id=app_config.ENGINE_CONFIG['arbitrary_style_transfer']['gpu_id'])
    