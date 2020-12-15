# -*- coding: utf-8 -*-
""" 引擎管理：
建立引擎管理队列，支持功能注册、状态查询；周期统计运行数据等。
"""

import time
import datetime
import enum
import inspect
from collections import OrderedDict
#from multiprocessing import Process, Queue

from app.engine_v1 import app_config, logger


# 引擎状态（2种）：在线：online、离线：offline
EngineStat = enum.Enum('EngineStat', ('ONLINE', 'OFFLINE'))


class Engine:
    """图片处理引擎"""

    INVALID_VALUE = -9999
    
    def __init__(self, name=None, func_info_list=None, worker=None, msg=None):
        # 1. 引擎名称
        self.name = name
        # 2. 引擎状态
        self.engine_stat = EngineStat.OFFLINE
        # 3. 功能注册信息
        self.func_info_list = func_info_list
        # 4. 工作引擎实例：类型为一个单独的子进程
        self.worker = worker
        # 5. 完成处理的任务总数
        self.task_processed = 0
        # 6. 引擎开始运行时间
        self.start_time = None
        # 7. 附加信息：一般作为引擎状态的补充说明
        self.msg = msg

        #TODO: 对功能信息 func_info_list 进行合法性检查，通过且 worker 非空则设置状态为在线，否则离线
        
        if self.engine_stat == EngineStat.ONLINE:
            self.start_time = datetime.datetime.now()

    def update(self, key, value=INVALID_VALUE):
        """更新节点字段内容（不包含只读字段如 name）"""

        # 首先检查字段合法性
        if key not in self.__dict__:
            return False, 'unknown engine item: {}'.format(key)
        
        # 更新指定的属性值
        if value != self.INVALID_VALUE:
            self.__dict__[key] = value

    def status(self):
        """查询引擎状态"""

        stat = OrderedDict()
        stat["status"] = self.engine_stat
        stat["start_time"] = self.start_time
        stat["task_processed"] = self.task_processed
        stat["uptime"] = datetime.datetime.now() - self.start_time


class EngineController(object):
    """引擎管理器。通过多进程代理提供给客户端进行访问。主要接口有：
    功能清单查询，引擎状态查询；清理失效引擎等。
    """

    def __init__(self):
        """初始化"""

        # 引擎队列：所有成功注册的引擎都挂在此队列中，需定时调用相关方法检查状态或清理无效引擎
        self.__engine_queue = OrderedDict()

        # 引擎功能：各引擎在此注册所支持的图片处理功能信息，必须归属到某一个 func_group 里
        self.__engine_func_groups = OrderedDict()
        for i in ( # 以下功能组顺序参考了 faceApp 的设计（可以为空）：
            'smiles', # 笑容
            'impression', # 印象
            'age', # 年龄
            'beards_m', # 男胡子 only for male
            'makeup_f', # 女化妆 only for female
            #'hair_colors', # 发色
            #'hair_styles', # 发型
            'hair', # 头发 #zzz 目前只有发色
            'alien', # 肤色 #zzz, just for face_makeup_pt
            'bright', # 化妆 for all #zzz, just for beautygan
            'dark', # 化妆 for all #zzz, just for beautygan
            'nature', # 化妆 for all #zzz, just for beautygan
            'glasses', # 眼镜
            'makeup_m', # 男化妆 only for male
            'filters', # 滤镜
            'lens_blur', # 对焦
            'background', # 背景
            'overlay', # 光斑
            'tatto', # 纹身
            'vignette', # 暗角
            'adjustments', # 对比
            '__art_cartoon', # 卡通（ART 标签页功能）
            '__art_painting', # 武断迁移风格-油画（同上）
            '__art_watercolor', # 武断迁移风格-水彩（同上）
            '__art_prints', # 武断迁移风格-版画（同上）
            '__art_creative', # 武断迁移风格-创意（同上）
            '__fun' # FUN 标签页功能
        ):
            func_class_value = 'fc_editor'
            name_value = i
            if i[0:5] == '__art':
                func_class_value = 'fc_art'
                name_value = i[6:]
                name_value.replace('_', ' ')
            elif i[0:5] == '__fun':
                func_class_value = 'fc_fun'
            self.__engine_func_groups[i] = {
                "func_group": i, # 功能类别，与字典键值一致
                "name": name_value, # 显示名称：前端再多语言翻译
                "sex": "all", # 适合性别：male/female/all
                "vip": 0, # 适合用户等级：0/1
                "icon": "/static/ui_data/func_group/{}.jpg".format(i), # 显示图标
                "func_list": [] # 功能组下的功能清单
            }
            # 各功能组功能清单的第1项固定为“恢复原图”（Fun 功能组例外）
            if i != '__fun':
                self.__engine_func_groups[i]["func_list"].append({
                        "name": "original", "vip": 0,
                        "icon": "/static/ui_data/face_demo/face_original.jpg",
                        "func_class": func_class_value,
                        "func_name": None,
                        "func_params": []
                    })
        # 如果要直接返回图标内容而不是路径，可以读取本地文件系统图片，并转为 base64 格式。示例代码：
        # image_to_base64(read_local_image("ui_data/face_demo/3.jpg",folder_type="STATIC_FOLDER"))
        
        #TODO: 如有需要，可以在此修改上述某些 func_group 的字段值
        # 修改部分 editor 功能组的适合性别
        self.__engine_func_groups['beards_m']['name'] = "beards"
        self.__engine_func_groups['beards_m']['sex'] = "male"
        self.__engine_func_groups['makeup_f']['name'] = "makeup"
        self.__engine_func_groups['makeup_f']['sex'] = "female"
        self.__engine_func_groups['makeup_m']['name'] = "makeup"
        self.__engine_func_groups['makeup_m']['sex'] = "male"
        
        # 将输出到客户端的引擎信息
        self.engine_info = {}
        self.engine_info['functions'] = []

    def __make_response(self, if_success, data=None):
        if if_success:
            return({'return': 'success', 'data': data})
        else:
            return({'return': 'fail', 'data': data})

    def engine_add(self, engine={}):
        """添加新引擎节点到队列中
        引擎信息主要包括：输入图片、人脸地图数据、人脸特征数据、处理方式名称、处理方式参数"""

        # 参数合法性检查
        params_invalid = False
        msg = None
        if 'name' not in engine or 'func_info_list' not in engine:
            params_invalid = True
            msg = 'need engine name and func_info_list'
        #TODO: 检查 func_info_list 内容合法性
        if params_invalid:
            return self.__make_response(False, msg)

        # 根据客户端传入的 engine 信息生成引擎对象
        name = engine['name']
        new_engine = Engine(
            name=name,
            func_info_list=engine['func_info_list'],
            worker=engine['worker']
        )
        self.__engine_queue[name] = new_engine

        return self.__make_response(True, {'name':name})

    def engine_update(self, name, engine_items={}):
        """更新引擎节点属性值"""

        if name not in self.__engine_queue:
            return self.__make_response(False, 'no such engine: {}'.format(name))
        
        engine = self.__engine_queue[name]
        for i in engine_items:
            if i not in dir(engine):
                return self.__make_response(False, 'no such engine item: {}'.format(i))
        
        for i in engine_items:
            engine.update(i, engine_items[i])
        
        return self.__make_response(True, engine)
    
    def engine_functions(self):
        """返回引擎队列支持的所有功能信息，主要有：功能分组、功能函数、函数参数、及引擎实例。
        功能分组：在代码中预先指定，5~9个类别
        功能函数：在各引擎注册时分别挂到不同分组功能下，包括显示名称、函数名称、函数参数
        引擎实例： = (输出图片内容，或补充信息)
        """

        if len(self.engine_info['functions']) == 0:
            # 逐一按照各引擎功能函数注册信息进行注册
            for engine in self.__engine_queue:
                for i in self.__engine_queue[engine].func_info_list:
                    fg = i['func_group']
                    if fg not in self.__engine_func_groups:
                        logger.error('invalid func_group of engine {}: {}'.format(engine, fg))
                    else:
                        self.__engine_func_groups[fg]['func_list'].extend(i['func_list'])
            # 将注册信息整合为前端功能菜单所需数据
            for i in self.__engine_func_groups:
                if len(self.__engine_func_groups[i]['func_list']) > 1:
                    self.engine_info['functions'].append(self.__engine_func_groups[i])
            
        return self.__make_response(True, self.engine_info)

    def engine_delete(self, name):
        """从指定引擎队列中删除节点（不包括图片等引擎文件，这些另外清理）"""

        if name not in self.__engine_queue:
            return self.__make_response(False, 'no engine found: {}'.format(name))
        else:
            #TODO: 关闭 worker 实例
            return self.__make_response(True, self.__engine_queue.pop(name))

    def status(self):
        """查询服务状态
        返回各引擎的运行统计信息"""
        
        stat = OrderedDict()

        stat["engines"] = OrderedDict()
        for engine in self.__engine_queue:
            stat["engines"][engine] = self.__engine_queue[engine].status()
        stat["length"] = len(self.__engine_queue)

        return self.__make_response(True, stat)
    
