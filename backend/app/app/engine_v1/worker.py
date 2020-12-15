# -*- coding: utf-8 -*-
""" 工作引擎管理：各工作引擎子进程的初始化，以及功能函数注册。
"""

import os
import sys
import io
import time
import shutil
import datetime
import logging
import traceback
import multiprocessing
from multiprocessing import Process, Queue
import numpy as np

from app.util import load_task_obj_data, save_task_obj_data
from app.util import make_cache_file_name
from app.engine_v1 import app_config, logger
from app.engine_v1 import image_process_wrap, save_cache_demo_image
from app.engine_v1.m_client import ManagerClient
from app.engine_v1.task import TaskQueue, TaskStat
from app.engine_v1.utils.face_detector import FaceDetector
from app.engine_v1.ai_modules.face_attribute_fan import adapter as face_attribute_adapter


class BaseWorker(Process):
    """子进程基类"""

    def __init__(self, daemon=True):
        super(BaseWorker, self).__init__(daemon=True)
        self.name = self.__class__.__name__
        self.logger = logger

    def run(self):
        """封装具体任务的执行，若异常则重新加载
        【本函数不得被子类重载】，请重载 run_worker 函数！"""

        # 等待一段时间让 manager 主进程启动完成，然后再连接
        delay_seconds = 30
        self.logger.info(
            'waiting {}s for manager to start ...'.format(delay_seconds))
        time.sleep(delay_seconds)

        while True:
            self._mm_client = ManagerClient()
            self.logger.info('manger client is alive: %s' %
                             self._mm_client.is_alive())

            try:
                self.run_worker()
            except Exception as e:
                self.logger.error(
                    '{} got exception when running: {}'.format(self.name, e))
                self.logger.error(traceback.format_exc(limit=10))
                time.sleep(10)
                self.logger.warn('reload {}...'.format(self.name))

    def run_worker(self):
        """具体的任务内容（需要被重载）"""
        pass


class BaseFuncWorker(BaseWorker):
    """图片处理引擎子进程基类"""

    def __init__(self, daemon=True):
        super(BaseFuncWorker, self).__init__(daemon=True)
        self._engine = None
        self._task_filters = None
        self._func_process_image = None
        self._func_info_list = None

    def run_worker(self):
        """图片处理引擎主流程：循环读取任务队列，直到收到空任务才退出"""

        while True:
            time.sleep(0.2)  # 间隔定时处理，避免空耗CPU

            if not self._task_filters:
                continue
            
            # 根据子类注册功能函数获取待处理任务
            #TODO: 检查 _task_filters 中的 func_name 和 func_args 基本取值合法性
            result = self._mm_client.shared_obj_func_call(
                'task_controller', 'pending_tasks_get', (self._task_filters,))
            if result:
                if result['return'] == 'success' and result['data'] is not None:
                    task = result['data']
                    self.logger.info('got a pending task for {}: {}'
                                    .format(self, task))
                    
                    # 调用引擎处理图片，并更新任务状态
                    _task_stat = TaskStat.FAIL
                    _task_msg = None
                    try:
                        if self._process(task):
                            _task_stat = TaskStat.SUCCESS
                    except Exception as e:
                        _task_msg = str(e)
                        self.logger.error(traceback.format_exc(limit=5))
                    self._mm_client.shared_obj_func_call(
                            'task_controller', 'task_update', (task.task_id, TaskQueue.PROCESS, {'task_stat': _task_stat, 'msg': _task_msg}))
                else:
                    #self.logger.warn('shared_obj_func_call(task_controller, pending_task_get) got None, not connected or no such func?') # 此行输出太多，注释掉
                    pass

    def _engine_init(self):
        """执行引擎初始化
        注意：由于 cuda 不能重复初始化，该函数只应在子进程中调用，不可在子进程的 __init__ 中调用"""
        pass

    def _get_tasks_filter(self):
        task_filters = []
        if self._func_info_list:
            for i in self._func_info_list:
                _ll = [x['func_name'] for x in i['func_list'] if x['func_name']]
                func_name_list = [] # 去重
                for x in _ll:
                    if x not in func_name_list:
                        func_name_list.append(x)
                task_filters.append((i['func_group'], func_name_list))
        return task_filters
    
    def _process(self, task):
        self.logger.info('processing task {}: {}, {}, {}...'
            .format(task.task_id, task.func_group, task.func_name, task.func_params))

        process_ok = False

        if not self._engine:
            self._engine_init()

        if self._engine:
            image = load_task_obj_data(app_config.SAVE_FILE_NAME['image_save'],
                                task.m_id, app_config, logger)
            face_data = load_task_obj_data(app_config.SAVE_FILE_NAME['face_data'],
                                task.m_id, app_config, logger)
            # 根据 task 内容选择相应引擎处理函数，对图片进行处理
            image_output = image_process_wrap(image, face_data, 
                                self._func_process_image, self._engine,task.func_class, 
                                task.func_group, task.func_name, task.func_params,
                                worker=self)
            image.close()

            if image_output:
                save_task_obj_data(image_output, app_config.SAVE_FILE_NAME['image_temp'],
                                    task.m_id, app_config, logger)
                process_ok = True
                self.logger.info('task {} process done.'.format(task.task_id))
                
                # 对于 demo 图片，定期更新缓存结果
                if 'img_hash' in face_data:
                    img_hash = face_data['img_hash']
                    if img_hash in app_config.IMG_HASH_APP_DEMO: # APP 前端所用的四个 demo 图片之一
                        if task.func_params and len(task.func_params) > 0:
                            func_args = str(task.func_params[0])
                        else:
                            func_args = None
                        cache_file_name = make_cache_file_name(task.func_class, 
                                                task.func_group, task.func_name, func_args)
                        save_cache_demo_image(image_output, img_hash, 
                                              app_config.DEMO_CACHE_DIR, cache_file_name)
            else:
                self.logger.info('task {} process failed. Unsupported picture?'.format(task.task_id))

        return process_ok


class PreprocessWorker(BaseWorker):
    """新任务预处理子进程
    定时检查”新任务队列”，依次获取任务节点并进行预处理，完毕后迁移到待处理队列
    """

    def __init__(self, daemon=True):
        super(PreprocessWorker, self).__init__(daemon=True)

    def run_worker(self):
        """定时循环获取新任务，对任务图片进行预处理，并将处理完的任务节点进行迁移"""

        # 首先执行人脸检测和特征识别辅助引擎初始化
        self.logger.info("initializing face detector engine...")
        self.face_detector = FaceDetector()
        self.logger.info("initializing face attribute engine...")
        self.face_attribute = face_attribute_adapter.init_model()

        func_list = self._mm_client.shared_obj_func_list('task_controller')
        self.logger.info('task controller functions: {}'.format(func_list))
        func_list = self._mm_client.shared_obj_func_list('engine_controller')
        self.logger.info('engine controller functions: {}'.format(func_list))

        while True:
            time.sleep(0.2)  # 间隔定时处理，避免空耗CPU

            result = self._mm_client.shared_obj_func_call(
                'task_controller', 'new_task_get')
            if result and result['return'] == 'success' and result['data']:
                task = result['data']
                self.logger.info('got a new task: {}'.format(task.task_id))
                task_stat = TaskStat.SUCCESS # 预处理成功后的状态
                task_msg = None

                # 1、读取新提交的任务图片
                image = load_task_obj_data(app_config.SAVE_FILE_NAME['image_base'],
                                          task.m_id, app_config, logger)
                
                # 2、对图片进行归一化处理，并保存到文件
                image_output = image_process_wrap(image) # 不指定引擎函数即只做归一化
                for ff in (app_config.SAVE_FILE_NAME['image_norm'],
                            app_config.SAVE_FILE_NAME['image_temp'],
                            app_config.SAVE_FILE_NAME['image_save']):
                    save_task_obj_data(image_output, ff, task.m_id, app_config, logger)
                image.close()

                # 3、调用引擎获取人脸地图及人脸特征，保存到文件
                #（大部分 AI 模型只支持正方形的面部图片，所以需要进行人脸识别，并截取）
                # 不管是否有人脸图均返回成功，对于无人脸图片引擎处理时再判断报错
                
                face_data = {}
                
                image_output_np = np.asarray(image_output)
                # 获取人脸位置及图像（如果人脸部分尺寸小于模型尺寸，则返回指定的最小尺寸为模型尺寸）
                faces_images = self.face_detector.get_faces_images(
                                    image_output_np, app_config.FACE_MIN_SIZE)
                if len(faces_images) == 0:
                    task_msg = "no face found in this picture."
                    self.logger.info(task_msg)
                else:
                    self.logger.info("got %d faces_images" % len(faces_images))
                    # 识别第一张人脸的特征，并保存 #FIXME: 或者取中间的人脸？
                    for (x, y, w, h, face_image) in faces_images:
                        attr_all = face_attribute_adapter.get_face_attrs(self.face_attribute, face_image)
                        self.logger.info('face_attribute_adapter get_face_attrs: %s' % attr_all)
                        
                        # 从 celeba 全部 40 个属性中选取所需的部分
                        name_all = "5_o_Clock_Shadow Arched_Eyebrows Attractive Bags_Under_Eyes Bald Bangs Big_Lips Big_Nose Black_Hair Blond_Hair Blurry Brown_Hair Bushy_Eyebrows Chubby Double_Chin Eyeglasses Goatee Gray_Hair Heavy_Makeup High_Cheekbones Male Mouth_Slightly_Open Mustache Narrow_Eyes No_Beard Oval_Face Pale_Skin Pointy_Nose Receding_Hairline Rosy_Cheeks Sideburns Smiling Straight_Hair Wavy_Hair Wearing_Earrings Wearing_Hat Wearing_Lipstick Wearing_Necklace Wearing_Necktie Young".split()
                        # default attrs: Bald Bangs Black_Hair Blond_Hair Brown_Hair Bushy_Eyebrows Eyeglasses Male Mouth_Slightly_Open Mustache No_Beard Pale_Skin Young
                        attr = [attr_all[name_all.index(n)] for n in app_config.ATTRS_ENABLED]
                        attr_dict = {}
                        for i in range(len(attr)):
                            if attr[i] == 1:
                                attr_dict[app_config.ATTRS_ENABLED[i]] = True
                            else:
                                attr_dict[app_config.ATTRS_ENABLED[i]] = False
                        self.logger.info('selected attr: {}, attr_dict: {}'.format(attr, attr_dict))
                        
                        face_data['x'] = x
                        face_data['y'] = y
                        face_data['w'] = w
                        face_data['h'] = h
                        face_data['attr'] = attr # 人脸属性（0 或 1 的列表）
                        face_data['attr_dict'] = attr_dict # 人脸属性（名称、键值字典）
                        face_data['face_image'] = face_image # 截取的人脸图片
                        #print('--> task.m_id:', task.m_id) # 20200107-07-45-32f6e7262b0e3c9b99c59f710d652b2a
                        face_data['img_hash'] = task.m_id.split('-')[-1]
                        #cv2.imwrite(join(app_config.SAVE_FILE_NAME['face_data'], '.jpg'), face_image)
                        
                        task_msg = face_data['attr_dict']
                        break # 只处理第一张人脸
                
                # 保存人脸图片及位置等信息到 pickle 文件
                save_task_obj_data(face_data, app_config.SAVE_FILE_NAME['face_data'], task.m_id, app_config, logger)
                
                # 4、更新任务节点状态
                result = self._mm_client.shared_obj_func_call('task_controller',
                                  'task_update', (task.task_id, TaskQueue.NEW, {'task_stat': task_stat, 'msg': task_msg}))
                self.logger.info(
                    'task_update {} result: {}'.format(task.task_id, result))
                
                # 5、迁移到”处理任务队列“（任务预处理引擎已在 new_task_get 中做迁移了）
                result = self._mm_client.shared_obj_func_call('task_controller', 
                                    'task_move', (task.task_id, TaskQueue.NEW, 
                                    TaskQueue.PROCESS,))
                self.logger.info(
                    'task_move {} result: {}'.format(task.task_id, result))
                
                # 对于 demo 图片，定期更新缓存结果
                if task_stat != TaskStat.FAIL and 'img_hash' in face_data:
                    img_hash = face_data['img_hash']
                    if img_hash in app_config.IMG_HASH_APP_DEMO: # APP 前端所用的四个 demo 图片之一
                        cache_file_name = make_cache_file_name()
                        save_cache_demo_image(image_output, img_hash,
                                              app_config.DEMO_CACHE_DIR, cache_file_name)
                        # 上述预处理文件，也需要拷贝到缓存目录下
                        dir_from = os.path.join(app_config.UPLOAD_FOLDER, task.m_id.replace('-', '/'))
                        img_hash = task.m_id.split('-')[-1]
                        for ff in (app_config.SAVE_FILE_NAME['image_norm'],
                                app_config.SAVE_FILE_NAME['image_temp'],
                                app_config.SAVE_FILE_NAME['image_save'],
                                app_config.SAVE_FILE_NAME['face_data']):
                            file_from = os.path.join(dir_from, ff)
                            file_to = os.path.join(app_config.DEMO_CACHE_DIR, img_hash, ff)
                            shutil.copyfile(file_from, file_to)
            
            else:
                #print('no new task found.')
                pass


class CleanerWorker(BaseWorker):
    """任务和资源清理子进程"""

    def __init__(self, daemon=True):
        super(CleanerWorker, self).__init__(daemon=True)

    def run_worker(self):
        """定时循环进行各项清理任务"""

        #func_list = self._mm_client.shared_obj_func_list('task_controller')
        #self.logger.info('task controller functions: {}'.format(func_list))
        
        count = 0
        while True:
            time.sleep(15)  # 间隔定时处理，避免空耗CPU

            self._mm_client.shared_obj_func_call('task_controller', 'tasks_clean')
            
            # 按目录名删除3天前的缓存目录
            count += 1
            if count % 120 == 0: # 每半个小时执行一次
                dir_to_clean = app_config.UPLOAD_FOLDER
                for _dir in os.listdir(dir_to_clean):
                    _now = time.localtime()
                    _time = time.strptime(_dir, '%Y%m%d')
                    _delta_days = int((int(time.mktime(_now)) - int(time.mktime(_time))) / (24 * 60 * 60))
                    if _delta_days >= 3:
                        _dir_path = os.path.join(dir_to_clean, _dir)
                        shutil.rmtree(_dir_path, ignore_errors=True)
                        self.logger.info('clean cache: delete dir {}'.format(_dir_path))
        

class SharedDataEsrganWorker(BaseWorker):
    """处理超解析共享数据任务的工作子进程"""
    
    def __init__(self, daemon=True):
        super(SharedDataEsrganWorker, self).__init__(daemon=True)
        self.task_engine = None # 此处在父进程中执行，使用 cuda 的引擎不可在此初始化
        
    def run_worker(self):
        """定时获取待处理任务，执行处理并回填结果"""

        from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

        self.task_engine = esrgan_adapter.init_model(
                                  gpu_id=app_config.ENGINE_CONFIG['esrgan']['gpu_id'])

        while True:
            time.sleep(0.2)  # 间隔定时处理，避免空耗CPU

            try:
                # 获取 n 个待处理任务
                pending_tasks = self._mm_client.shared_obj_func_call('shared_data_controller', 'get_pending_tasks', ('esrgan', 5))
                for i in pending_tasks:
                    img_pil, img_w, img_h = i['args']
                    # 调用超解析引擎进行处理
                    if not self.task_engine: # 此处在子进程中执行，使用 cuda 的引擎在此初始化
                        self.task_engine = esrgan_adapter.init_model(
                                  gpu_id=app_config.ENGINE_CONFIG['esrgan']['gpu_id'])
                    _img_out_pil = esrgan_adapter.process_image(
                                          img_pil, self.task_engine, img_w, img_h)
                    # 更新结果
                    self._mm_client.shared_obj_func_call('shared_data_controller', 'update_task_result', ('esrgan', i['t_id'], _img_out_pil,))
            except Exception as e:
                self.task_engine = None
                for i in pending_tasks:
                    # 恢复结果为待处理状态
                    self._mm_client.shared_obj_func_call('shared_data_controller', 'update_task_result', ('esrgan', i['t_id'], None,))
                raise e


class SharedDataFaceParsingWorker(BaseWorker):
    """处理人脸解析共享数据任务的工作子进程"""
    
    def __init__(self, daemon=True):
        super(SharedDataFaceParsingWorker, self).__init__(daemon=True)
        self.task_engine = None # 此处在父进程中执行，使用 cuda 的引擎不可在此初始化
        
    def run_worker(self):
        """定时获取待处理任务，执行处理并回填结果"""

        from app.engine_v1.utils.face_parsing import adapter as face_parsing_adapter

        self.task_engine = face_parsing_adapter.init_model(
                                  gpu_id=app_config.ENGINE_CONFIG['face_parsing']['gpu_id'])
        
        while True:
            time.sleep(0.2)  # 间隔定时处理，避免空耗CPU

            try:
                # 获取 n 个待处理任务
                pending_tasks = self._mm_client.shared_obj_func_call('shared_data_controller', 'get_pending_tasks', ('face_parsing', 5))
                for i in pending_tasks:
                    face_image, edit_area = i['args']
                    # 调用任务引擎进行处理
                    if not self.task_engine: # 此处在子进程中执行，使用 cuda 的引擎在此初始化
                        self.task_engine = face_parsing_adapter.init_model(
                                  gpu_id=app_config.ENGINE_CONFIG['face_parsing']['gpu_id'])
                    mask = face_parsing_adapter.getFaceMask(
                              face_image, self.task_engine, edit_area)
                    # 更新结果
                    self._mm_client.shared_obj_func_call('shared_data_controller', 'update_task_result', ('face_parsing', i['t_id'], mask,))
            except Exception as e:
                self.task_engine = None
                for i in pending_tasks:
                    # 恢复结果为待处理状态
                    self._mm_client.shared_obj_func_call('shared_data_controller', 'update_task_result', ('face_parsing', i['t_id'], None,))
                raise e
