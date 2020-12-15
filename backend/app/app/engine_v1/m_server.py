# -*- coding: utf-8 -*-
""" 多进程通讯支持：本模块为服务端；Flask 作为请求客户端产生任务；各 AI 引擎作为工作客户端处理任务。
！！！注意：由于 cuda 不支持在父子进程中两次初始化 GPU 设备，所以不要在此管理进程中（包括子进程的 __init__ 函数中）启动任何需要对 GPU 做初始化的事情，比如人脸解析或超解析引擎等。所有的 GPU 初始化都需要在子进程中执行。
否则后续在子进程中执行任何依赖 GPU 的 AI 引擎初始化时，都会报错：“cuda runtime error (3) : initialization error...”
"""

import os
import sys
import time
import logging
import traceback
import multiprocessing
from collections import OrderedDict
from multiprocessing import freeze_support, Pool
from multiprocessing.managers import BaseManager

from app.engine_v1 import app_config, logger
from app.engine_v1.task import TaskController
from app.engine_v1.engine import EngineController
from app.engine_v1.worker import BaseFuncWorker


class MyManager(BaseManager):
    pass


class ManagerServer():
    """管理器服务端，最顶层"""

    def __init__(self):
        self.logger = logger
        
        # 父子进程间共享对象
        self.task_controller = TaskController()
        self.engine_controller = EngineController()
        self.shared_data_controller = SharedDataController()
        
        self.mm = MyManager(address=(app_config.EM_ADDRESS,
                                app_config.EM_PORT), authkey=app_config.EM_AUTHKEY)

    def __start_workers(self):
        """启动各工作引擎子进程"""

        Workers = [] # 待启动子进程清单
        
        # 1. 先执行工作引擎辅助子进程
        from app.engine_v1.worker import SharedDataEsrganWorker # 超解析
        Workers.append([SharedDataEsrganWorker, 
                    app_config.ENGINE_CONFIG['esrgan']['proc_num']])
        from app.engine_v1.worker import SharedDataFaceParsingWorker # 人脸解析
        Workers.append([SharedDataFaceParsingWorker, 
                    app_config.ENGINE_CONFIG['face_parsing']['proc_num']])
        
        # 2. 再执行工作引擎子进程

        # 2.1 Facelet_Bank 工作引擎系列
        #if app_config.ENGINE_CONFIG['facelet_pt_feminization']['enabled']:
        #    from app.engine_v1.workers.facelet_pt import FaceletPtFeminizationFuncWorker
        #    Workers.append([FaceletPtFeminizationFuncWorker, # 女性化
        #            app_config.ENGINE_CONFIG['facelet_pt_feminization']['proc_num']])
        #if app_config.ENGINE_CONFIG['facelet_pt_masculinization']['enabled']:
        #    from app.engine_v1.workers.facelet_pt import FaceletPtMasculinizationFuncWorker
        #    Workers.append([FaceletPtMasculinizationFuncWorker, # 男性化
        #            app_config.ENGINE_CONFIG['facelet_pt_masculinization']['proc_num']])
        #if app_config.ENGINE_CONFIG['facelet_pt_older']['enabled']:
        #    from app.engine_v1.workers.facelet_pt import FaceletPtOlderFuncWorker
        #    Workers.append([FaceletPtOlderFuncWorker, # 老年化
        #            app_config.ENGINE_CONFIG['facelet_pt_older']['proc_num']])
        #if app_config.ENGINE_CONFIG['facelet_pt_younger']['enabled']:
        #    from app.engine_v1.workers.facelet_pt import FaceletPtYoungerFuncWorker
        #    Workers.append([FaceletPtYoungerFuncWorker, # 年轻化
        #            app_config.ENGINE_CONFIG['facelet_pt_younger']['proc_num']])
        #if app_config.ENGINE_CONFIG['facelet_pt_facehair']['enabled']:
        #    from app.engine_v1.workers.facelet_pt import FaceletPtFacehairFuncWorker
        #    Workers.append([FaceletPtFacehairFuncWorker, # 胡子
        #            app_config.ENGINE_CONFIG['facelet_pt_facehair']['proc_num']])
        
        # 2.2 DFI 多效果工作引擎（处理较慢，不建议使用）
        #if app_config.ENGINE_CONFIG['deep_feat_interp']['enabled']:
        #    from app.engine_v1.workers.deep_feat_interp import DeepFeatInterpFuncWorker
        #    Workers.append([DeepFeatInterpFuncWorker,
        #            app_config.ENGINE_CONFIG['deep_feat_interp']['proc_num']])

        # 2.3 AttGAN 多效果工作引擎（发色、肤色等）
        #if app_config.ENGINE_CONFIG['attgan_pt']['enabled']:
        #    from app.engine_v1.workers.attgan_pt import AttganPtFuncWorker
        #    Workers.append([AttganPtFuncWorker,
        #            app_config.ENGINE_CONFIG['attgan_pt']['proc_num']])
        
        # 2.4 FaceMakeup 换色美妆工作引擎
        if app_config.ENGINE_CONFIG['face_makeup_pt']['enabled']:
            from app.engine_v1.workers.face_makeup_pt import FaceMakeupPtFuncWorker
            Workers.append([FaceMakeupPtFuncWorker,
                    app_config.ENGINE_CONFIG['face_makeup_pt']['proc_num']])

        # 2.5 BeautyGAN 智能美妆工作引擎
        if app_config.ENGINE_CONFIG['beautygan']['enabled']:
            from app.engine_v1.workers.beautygan import BeautyganFuncWorker
            Workers.append([BeautyganFuncWorker,
                    app_config.ENGINE_CONFIG['beautygan']['proc_num']])

        # 2.6 UGATIT 漫画工作引擎
        if app_config.ENGINE_CONFIG['ugatit']['enabled']:
            from app.engine_v1.workers.ugatit import UgatitFuncWorker
            Workers.append([UgatitFuncWorker,
                    app_config.ENGINE_CONFIG['ugatit']['proc_num']])

        # 2.7 CartoonGAN 漫画工作引擎系列
        # 每个引擎占用约 3.6G 显存，一般只开一个即可
        if app_config.ENGINE_CONFIG['cartoongan_pt']['enabled']:
            from app.engine_v1.workers.cartoongan_pt import CartoonganPtHayaoFuncWorker
            Workers.append([CartoonganPtHayaoFuncWorker, # Hayao 风格
                    app_config.ENGINE_CONFIG['cartoongan_pt']['proc_num']])
            #from app.engine_v1.workers.cartoongan_pt import CartoonganPtHosodaFuncWorker
            #Workers.append([CartoonganPtHosodaFuncWorker, # Hosoda 风格
            #        app_config.ENGINE_CONFIG['cartoongan_pt']['proc_num']])
            #from app.engine_v1.workers.cartoongan_pt import CartoonganPtPaprikaFuncWorker
            #Workers.append([CartoonganPtPaprikaFuncWorker, # Paprika 风格（过暗，暂不用）
            #        app_config.ENGINE_CONFIG['cartoongan_pt']['proc_num']])
            from app.engine_v1.workers.cartoongan_pt import CartoonganPtShinkaiFuncWorker
            Workers.append([CartoonganPtShinkaiFuncWorker, # Shinkai 风格
                    app_config.ENGINE_CONFIG['cartoongan_pt']['proc_num']])
            
        # 2.8 面部保护风格迁移工作引擎系列
        if app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['enabled']:
            from app.engine_v1.workers.face_preserving_style_transfer_pt import FacePreservingStyleTransferPtMangaFuncWorker # manga-face 风格
            Workers.append([FacePreservingStyleTransferPtMangaFuncWorker,
                    app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['proc_num']])
            from app.engine_v1.workers.face_preserving_style_transfer_pt import FacePreservingStyleTransferPtMosaicFuncWorker # mosaic-face 风格
            Workers.append([FacePreservingStyleTransferPtMosaicFuncWorker,
                    app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['proc_num']])
            #from app.engine_v1.workers.face_preserving_style_transfer_pt import FacePreservingStyleTransferPtGrandeJatteFuncWorker # grande-jatte 风格
            #Workers.append([FacePreservingStyleTransferPtGrandeJatteFuncWorker,
            #        app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['proc_num']])
            #from app.engine_v1.workers.face_preserving_style_transfer_pt import #FacePreservingStyleTransferPtRainsRustleFuncWorker # rain-rustle 风格
            #Workers.append([FacePreservingStyleTransferPtRainsRustleFuncWorker,
            #        app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['proc_num']])
            #from app.engine_v1.workers.face_preserving_style_transfer_pt import FacePreservingStyleTransferPtStaryNightFuncWorker # stary-night 风格
            #Workers.append([FacePreservingStyleTransferPtStaryNightFuncWorker,
            #        app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['proc_num']])
            from app.engine_v1.workers.face_preserving_style_transfer_pt import FacePreservingStyleTransferPtWaveFuncWorker # wave 风格
            Workers.append([FacePreservingStyleTransferPtWaveFuncWorker,
                    app_config.ENGINE_CONFIG['face_preserving_style_transfer_pt']['proc_num']])

        # 2.9 武断风格迁移
        if app_config.ENGINE_CONFIG['arbitrary_style_transfer']['enabled']:
            from app.engine_v1.workers.arbitrary_style_transfer import ArbitraryStyleTransferWorker
            Workers.append([ArbitraryStyleTransferWorker,
                    app_config.ENGINE_CONFIG['arbitrary_style_transfer']['proc_num']])

        # 3. 再执行框架辅助子进程

        # 3.1 循环定时执行新任务预处理
        from app.engine_v1.worker import PreprocessWorker
        Workers.append([PreprocessWorker, app_config.ENGINE_CONFIG['preprocess']['proc_num']])

        # 3.2 循环定时清理过期任务及资源文件
        from app.engine_v1.worker import CleanerWorker
        Workers.append([CleanerWorker, app_config.ENGINE_CONFIG['cleaner']['proc_num']])

        # 4. 启动上述各子进程

        self.logger.info('start work subprocesses...')
        for Worker, p_num in Workers: # 上述每类引擎
            for i in range(p_num): # 启动指定数量子进程
                w = Worker()
                if issubclass(Worker, BaseFuncWorker): # 仅注册普通工作引擎信息到共享对象中
                    self.engine_controller.engine_add({
                        'name': w.name,
                        'func_info_list': w._func_info_list,
                        'worker': w
                    })
                    self.logger.info('worker {} added to engine_controller'.format(w.name))
                w.start()
            w.join(1)  # 由于子进程是守护进程，等待超时后会继续往下执行
            self.logger.info('{} {} subprocesses started!'.format(i+1, w.name))
        
        # 5. 依次注册需要在进程间共享的对象，使其方法通过进程间 proxy 可见
        self.logger.info('register task_controller into MyManager...')
        self.mm.register('task_controller', callable=lambda: self.task_controller)
        self.logger.info('register engine_controller into MyManager...')
        self.mm.register('engine_controller', callable=lambda: self.engine_controller)
        self.logger.info('register share_controller into MyManager...')
        self.mm.register('shared_data_controller', callable=lambda: self.shared_data_controller)

    def __start_my_manager(self):
        
        s = self.mm.get_server()
        self.logger.info('[*] Running [{}] manager at {}:{} ...'.format(
                           os.environ.get("FLASK_ENV"), 
                           app_config.EM_ADDRESS, app_config.EM_PORT))
        s.serve_forever()

    def run(self):

        # 启动各工作引擎子进程
        self.__start_workers()
        
        # 启动管理服务器
        self.__start_my_manager()


class SharedDataController(object):
    """父子进程间共享数据管理器。通过多进程代理提供给客户端进行访问。
    主要有：超解析及人脸分隔任务及处理结果等。
    """

    def __init__(self):
        """初始化"""

        self.logger = logger

        self.shared_tasks = {}
        self.shared_tasks['esrgan'] = OrderedDict() # 超解析任务
        self.shared_tasks['face_parsing'] = OrderedDict() # 人脸解析任务

    def __make_response(self, if_success, data=None):
        if if_success:
            return({'return': 'success', 'data': data})
        else:
            return({'return': 'fail', 'data': data})

    def add_task(self, t_type, args):
        """ 添加超解析任务。在执行该函数的子进程中定时轮询获取结果。
        ESRGAN 超解析引擎子进程中将会获取待处理任务，并对图片进行处理和回填结果"""
        
        t_id = time.time()
        try:
            self.shared_tasks[t_type][t_id] = {
                't_id': t_id,
                'args': args,
                'result': None
            }
            return self.__make_response(True, t_id)
        except Exception as e:
            self.logger.warn(traceback.format_exc(limit=5))
            return self.__make_response(False, 'exec_esrgan FAIL: {}'.format(e))
    
    def get_pending_tasks(self, t_type, num=5):
        # 清理过期任务
        keys = [i for i in self.shared_tasks[t_type]]
        for i in keys:
            if time.time() - float(i) > app_config.MM_TASK_EXPIRED + 2: # 任务过期就算失效，直接清除
                #print('--> task {} expired, delete now!')
                self.shared_tasks[t_type].pop(i)
        
        pending_tasks = []
        cnt = 0
        for i in self.shared_tasks[t_type]:
            if not self.shared_tasks[t_type][i]['result']:
                self.shared_tasks[t_type][i]['result'] = 'pengding' # 防止在处理时再被其他子进程获取
                pending_tasks.append(self.shared_tasks[t_type][i])
                cnt += 1
                if cnt >= num:
                    break
        return pending_tasks
        
    def update_task_result(self, t_type, t_id, result):
        if t_id in self.shared_tasks[t_type]:
            self.shared_tasks[t_type][t_id]['result'] = result
            return True
        else:
            return False
    
    def get_task_result(self, t_type, t_id):
        if t_id not in self.shared_tasks[t_type]:
            #print('--> get_task_result() self.shared_tasks[{}]:'.format(t_type), self.shared_tasks[t_type])
            #print('--> get_task_result() t_id not found:', t_id)
            return self.__make_response(False, 'no such t_id: {}'.format(t_id))
        elif not self.shared_tasks[t_type][t_id]['result']:
            #print('--> get_task_result() no result found for:', t_type, t_id)
            return self.__make_response(False, 'no result found for t_id {}'.format(t_id))
        elif self.shared_tasks[t_type][t_id]['result'] == 'pengding':
            return self.__make_response(False, 'processing for t_id {}'.format(t_id))
        else:
            return self.__make_response(True, self.shared_tasks[t_type][t_id]['result'])
