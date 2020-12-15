# -*- coding: utf-8 -*-
""" 定义图片等媒体文件处理的相关 rest API 接口。
"""

import os
import time
import json
import shutil
from PIL import Image
from flask import current_app, jsonify, request, url_for

from . import api
from .. import db
from .authentication import auth
from .common import get_request_data, set_result_image, image_to_base64, \
                    resp_result, resp_error, image_add_watermark, read_local_image
                    
from app.util import save_task_image_from_selected, make_cache_file_name
from app.engine_v1.utils.esrgan import adapter as esrgan_adapter


@api.route("/media/config", methods=["GET"])
def config_storage():
    """返回服务端图片存储方式"""
    data = {}
    data["storage"] = current_app.config['STORAGE_TYPE']
    return resp_result(data)


@api.route("/media/face_demo", methods=["GET"])
#@auth.login_required # 基于 flask-httpauth 完成无状态 HTTP 认证（设置 header 方式）
def media_face_demo():
    """获取演示图片列表"""
    data = {}
    data["demo_list"] = [
        "/static/ui_data/face_demo/1.jpg",
        "/static/ui_data/face_demo/2.jpg",
        "/static/ui_data/face_demo/3.jpg",
        "/static/ui_data/face_demo/4.jpg"
    ]
    return resp_result(data)


@api.route("/media/task_add", methods=["POST"])
@current_app.limiter.limit("1800/hour;60/minute;4/second")  # 自定义访问速率
@auth.login_required
def task_add():
    """根据客户端请求生成图片处理任务"""
    data = {}
    if request.args.get("tk") == "harekrishna10800":  # FIXME: 改为正规的令牌校验机制
        if request.method == "POST":
            m_id, params, msg, is_new_image = get_request_data(request)
            current_app.logger.info('task_add() got post request. params: {}, msg: {}, '
                                    'm_id: {}, is_new_image: {}'
                                    .format(params, msg, m_id, is_new_image))
            if not params or not m_id:
                return resp_error(msg)

            # 根据 m_id 和 params 生成新任务，提交后端进行处理
            task = {}
            task.update(params)
            task['m_id'] = m_id
            #print('--> repr(task):', repr(task))
            # 新提交图片 task 示例：{'user_id': 'zzz123', 'func_group': None, 'm_id': '20200108-10-35-12d2b6c4a62be56c494324809441be41', 'func_class': None, 'func_params': None, 'func_name': None}
            # 图片任务 task 示例 {'func_params': ['avatar', ['face', 'l_ear', 'r_ear', 'nose', 'u_lip', 'l_lip']], 'func_class': 'fc_editor', 'func_name': 'chg_color', 'func_group': 'impression', 'user_id': 'zzz123'}
            
            data['m_id'] = m_id
            
            # 如果是 demo 图片，且请求的处理已经有未过期缓存，则直接返回一个特殊且固定的 task_id
            img_hash = m_id.split('-')[-1]
            if img_hash in current_app.config['IMG_HASH_APP_DEMO']: # 前端所用四个 demo 图片之一
                if task['func_params'] and type(task['func_params']) is list \
                and len(task['func_params']) > 0:
                    func_args = str(task['func_params'][0])
                else:
                    func_args = None
                cache_file = os.path.join(current_app.config['DEMO_CACHE_DIR'], img_hash, make_cache_file_name(task['func_class'], task['func_group'], 
                                     task['func_name'], func_args))
                
                current_app.logger.info('task_add() check cache file {}'.format(cache_file))
                if os.path.isfile(cache_file) and time.time() - os.path.getctime(cache_file) <= current_app.config['DEMO_CACHE_UPDATE_TERM']:
                    data['task_id'] = 'THE_CACHE_TASK_ID' # 其他 task_id 为浮点数
                    current_app.logger.info('task_add() found valid cache, bypass new_task_add.')
                    # 从缓存目录拷贝预处理文件到任务目录下，以便后续没有做过缓存的可以正常处理
                    dir_to = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                          m_id.replace('-', '/'))
                    for ff in (current_app.config['SAVE_FILE_NAME']['image_norm'],
                            current_app.config['SAVE_FILE_NAME']['image_temp'],
                            current_app.config['SAVE_FILE_NAME']['image_save'],
                            current_app.config['SAVE_FILE_NAME']['face_data']):
                        file_from = os.path.join(current_app.config['DEMO_CACHE_DIR'], 
                                                 img_hash, ff)
                        file_to = os.path.join(dir_to, ff)
                        shutil.copyfile(file_from, file_to)
                    return resp_result(data)
            
            # 判断是否新提交图片，如果是则置任务状态为 NEW，否则为 PENDING
            from ..engine_v1.task import TaskStat
            if is_new_image:
                task['task_stat'] = TaskStat.NEW
            else:
                #TODO: 在此通过后端逻辑判断是否为 VIP 功能，以及检查用户是否有 VIP 权限！（v2版本实现）
                task['task_stat'] = TaskStat.PENDING
            
            with current_app.app_context():
                try:
                    #func_list = current_app.mm_client.shared_obj_func_lists('task_controller')
                    #current_app.logger.warn('task controller functions: {}'.format(func_list))
                    result = current_app.mm_client.shared_obj_func_call(
                                                'task_controller', 'new_task_add', (task,))
                    current_app.logger.info('call new_task_add return: {}'.format(result))
                    if result['return'] == 'success' and result['data'] is not None:
                        data['task_id'] = result['data']['task_id']
                except Exception as e:
                    current_app.logger.error(e)
        else:
            return resp_error("invalid method")
    else:
        return resp_error("invalid tk")
    return resp_result(data)


@api.route("/media/task_query", methods=["GET"])
@current_app.limiter.limit("8/second")
@auth.login_required
def task_query():
    """查询任务状态
    备注：为给引擎留出处理时间，可每秒钟重新查询，最多10次（可配置），由于不便在 flask 中使用阻塞式 sleep，需要在前端实现该逻辑。
    """

    data = {}
    
    result = None
    task_id = request.args.get('task_id')
    if task_id:
        got_result_image = False
        data['progress'] = 5

        # 如果是请求 demo 图片处理结果的内定 task_id，则直接读取缓存并返回
        if task_id == 'THE_CACHE_TASK_ID':
            m_id = request.args.get('m_id')
            img_hash = m_id.split('-')[-1]
            
            if img_hash in current_app.config['IMG_HASH_APP_DEMO']: # 前端所用四个 demo 图片之一
                current_app.logger.info('task_query() got request args: {}'.format(repr(request.args)))
                func_group, func_class, func_name, func_param0 = __get_func_args_from_request_args(request)
                cache_file = os.path.join(current_app.config['DEMO_CACHE_DIR'], img_hash, make_cache_file_name(func_class, func_group, func_name, func_param0))
                
                current_app.logger.info('task_query() check cache file {}'.format(cache_file))
                if os.path.isfile(cache_file):
                    result_image = read_local_image(cache_file)
                    if func_class == 'fc_fun':
                        # 演示图片，右下角加 logo 水印
                        result_image = image_add_watermark(result_image)
                    got_result_image = True
                    data['m_id'] = m_id
                    data['msg'] = json.dumps('got cache result.')
                    current_app.logger.info('task_query() loaded cache result for the demo image.')
        
        # 如果没找到缓存，则向后端查询处理结果
        if not got_result_image:
            result = current_app.mm_client.shared_obj_func_call(
                                    'task_controller', 'task_query', (task_id,))
            current_app.logger.info('call task_query {} return: {}'
                                    .format(task_id, result))
            if result['return'] == 'success' and result['data'] is not None:
                data['progress'] = result['data']['progress']
                if data['progress'] == 100:
                    result_image = result['data']['image']
                    got_result_image = True
                    # 做超解析缩放为指定输出大小（已在引擎中处理，故此注释掉）
                    #out_img_w, out_img_h = current_app.config['OUTPUT_SIZE_FUN']
                    #with current_app.app_context():
                    #    result_image = esrgan_adapter.process_image(result_image,       current_app.esrgan, out_img_w, out_img_h)
                    if result['data']['func_class'] == 'fc_fun':
                        # 演示图片，右下角加 logo 水印
                        result_image = image_add_watermark(result_image)
                    data['m_id'] = result['data']['m_id']
                    data['msg'] = json.dumps(result['data']['msg'])
        
        if got_result_image:
            data['progress'] = 100
            data['image'] = image_to_base64(result_image) # 转成 jpg base64 返回

    return resp_result(data)


@api.route("/media/task_apply_image_save", methods=["GET"])
@auth.login_required
def task_apply_image_save():
    """保存任务处理后图片
    """

    data = {}
    
    if not current_app.config['ENABLE_APPLY_IMAGE_SAVE']:
        data['msg'] = 'Function disabled. Bypass task_apply_image_save().'
        current_app.logger.info(data['msg'])
        return resp_result(data)
    
    m_id = request.args.get('m_id')
    if m_id:
        try:
            demo_cahce_file = None
            img_hash = m_id.split('-')[-1]
            if img_hash in current_app.config['IMG_HASH_APP_DEMO']: # 前端所用四个 demo 图片之一
                current_app.logger.info('task_apply_image_save() got request args: {}'.format(repr(request.args)))
                f_group, f_class, f_name, f_param0 = __get_func_args_from_request_args(request)
                demo_cahce_file = os.path.join(current_app.config['DEMO_CACHE_DIR'], img_hash, make_cache_file_name(f_class, f_group, f_name, f_param0))
            save_task_image_from_selected(m_id, current_app.config, current_app.logger, demo_cahce_file)
        except Exception as e:
            current_app.logger.error('task_apply_image_save failed: {}'.format(e))
            data['m_id'] = m_id
            data['msg'] = str(e)
            return resp_error(data)
    
    return resp_result(data)


@api.route("/media/task_restore_original_image", methods=["GET"])
@auth.login_required
def task_restore_original_image():
    """恢复任务处理后图片为原图
    """

    data = {}
    
    m_id = request.args.get('m_id')
    if m_id:
        try:
            demo_cahce_file = None
            img_hash = m_id.split('-')[-1]
            if img_hash in current_app.config['IMG_HASH_APP_DEMO']: # 前端所用四个 demo 图片之一
                current_app.logger.info('task_restore_original_image() got request args: {}'.format(repr(request.args)))
                demo_cahce_file = os.path.join(current_app.config['DEMO_CACHE_DIR'], img_hash, 'image_norm.png')
            save_task_image_from_selected(m_id, current_app.config, current_app.logger, demo_cahce_file, 'image_norm')
        except Exception as e:
            current_app.logger.error('task_restore_original_image failed: {}'.format(e))
            data['m_id'] = m_id
            data['msg'] = str(e)
            return resp_error(data)
    
    return resp_result(data)


# 定义服务端可提供的图片编辑功能清单（必须）
@api.route("/media/functions", methods=["GET"])
@current_app.limiter.limit("1/second")
# @auth.login_required
def functions():
    """返回服务端支持的图片编辑功能清单。如果带参数 act，且其值为 ver 则只返回版本信息，否则返回全部数据。"""

    data = {}

    # 使用 worker.py 文件最后修改时间，作为功能配置信息版本号
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], '../../engine_v1/worker.py')
    filemt = time.localtime(os.stat(filename).st_mtime)  
    data["ver"] = time.strftime("%Y%m%d-%H%M%S", filemt)
    
    #print('--> request.args.get("act"): "%s"' %  request.args.get("act"))
    if request.args.get("act") != "ver":
        # 从引擎获取功能配置信息
        result = current_app.mm_client.shared_obj_func_call(
                        'engine_controller', 'engine_functions', ())
        #current_app.logger.info('call engine_functions return: {}'.format(result))
        if result['return'] == 'success' and result['data'] is not None:
            # 根据性别筛选结果后输出
            image_sex = request.args.get("sex")
            #print('--> image_sex:', image_sex)
            if image_sex not in ('female', 'male'):
                image_sex = 'all'
            
            functions_editor = []
            functions_art = []
            functions_fun = []
            for item in result['data']['functions']:
                if item['sex'] in ('all', image_sex): # 首先过滤群组性别
                    if item['func_group'][0:2] != '__': # Editor 功能组
                        item_editor = item.copy()
                        item_editor['func_list'] = \
                            [i for i in item['func_list'] if i['func_class'] == 'fc_editor']
                        functions_editor.append(item_editor)
                    elif item['func_group'][0:5] == '__art': # Art 功能组
                        item_art = item.copy()
                        item_art['func_list'] = \
                            [i for i in item['func_list'] if i['func_class'] == 'fc_art']
                        functions_art.append(item_art)
                    elif item['func_group'] == '__fun': # Fun 功能列表，不分组
                        for i in item['func_list']:
                            #print('--> i:', i)
                            if i['sex'] in ('all', image_sex): #再过滤子项性别
                                if i['func_class'] == 'fc_fun': #FIXME: 貌似没必要？能否去掉
                                    i['func_group'] = item['func_group']
                                    functions_fun.append(i)
                    else:
                        print('unknown func_group {}'.format(item['func_group']))
            data['functions_editor'] = functions_editor
            data['functions_art'] = functions_art
            data['functions_fun'] = functions_fun

            current_app.logger.info('return functions_editor: {}..., '
                                    'functions_art: {}..., functions_fun: {}...'
                                    .format(str(data['functions_editor'])[:200], 
                                          str(data['functions_art'])[:200],
                                          str(data['functions_fun'])[:200]))

    return resp_result(data)


def __get_func_args_from_request_args(request):
    func_group = request.args.get('func_group')
    func_class = request.args.get('func_class')
    func_name = request.args.get('func_name')
    func_params = request.args.get('func_params')
    if func_params and type(func_params) is str \
    and len(func_params.split(',')) > 0:
        func_param0 = func_params.split(',')[0]
    else:
        func_param0 = None
    
    return func_group, func_class, func_name, func_param0
