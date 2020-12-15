# -*- coding: utf-8 -*-
# 定义 api 和 engine 都需要的通用函数

import os
import hashlib
import datetime
import shutil
import pickle
import PIL
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from flask import current_app, Blueprint, jsonify, request


def save_task_obj_data(obj_data, file_name, m_id=None, config=None, logger=None):
    """根据配置保存结果图片到本地存储或云存储（flask 和引擎后端都可以调用）
    obj_data：PIL 形式图片内容，或者 python 对象
    file_name：文件名称，必须与配置保持一致
    m_id：资源标识（在本函数内生成），格式：年月日-小时-分钟-hash，创建时当前时间
    """

    if not config or not logger:
        raise Exception('config or logger MUST be set!')
    
    #print('--> type(obj_data):', type(obj_data))
    data_is_image = issubclass(type(obj_data), PIL.Image.Image)
    if not data_is_image and not m_id:
        raise Exception('data is not image, m_id cannot be None')

    if 'STORAGE_TYPE' in dir(config): # in engine
        storage_type = config.STORAGE_TYPE
        upload_folder = config.UPLOAD_FOLDER
        file_name_values = config.SAVE_FILE_NAME.values()
    else: # in Flask
        storage_type = config['STORAGE_TYPE']
        upload_folder = config['UPLOAD_FOLDER']
        file_name_values = config['SAVE_FILE_NAME'].values()
    
    if file_name not in file_name_values:
        raise Exception('invalid file name: {}'.format(file_name))
    
    # 本地文件存储
    if storage_type == 'local':

        if m_id and not m_id_valid(m_id):
            raise Exception('invalid m_id: {}'.format(m_id))
        
        # 如果为图片且 m_id 为空，则根据时间和图片哈希生成 m_id
        if data_is_image and not m_id:
            cur = datetime.datetime.now()
            cur_date = '%4d%02d%02d' % (cur.year, cur.month, cur.day)
            cur_hour = '%02d' % (cur.hour)
            cur_min = '%02d' % (cur.minute)

            # 根据图片内容生成文件哈希
            #image_np = np.array(obj_data) * np.random.randint(10)
            image_np = obj_data.tobytes()
            file_hash = hashlib.md5(image_np).hexdigest()
            
            m_id = cur_date + '-' + cur_hour + '-' + cur_min + '-' + file_hash
        
        # 根据 m_id 生成存储路径。格式：年月日/小时/分钟/hashxxx/image_xxx.jpg
        file_dir = join(upload_folder, m_id.replace('-', '/'))
        full_name = join(file_dir, file_name)
        
        if data_is_image:
            # 判断存储目录，不存在则创建。
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            # 保存图片到文件
            obj_data.save(full_name, quality=95)
        else:
            with open(full_name, 'wb') as file:
                # 保存其他数据人脸信息到文件
                pickle.dump(obj_data, file)
        
        logger.info('obj_data saved to local file: %s' % full_name)
        
    # amazon s3 云存储
    elif storage_type == 'amz_s3':
        logger.debug('not supported yet.')
        #TODO: 实现该云存储方式支持
    
    # 其他存储方式
    else:
        logger.debug('unkown storage type.')

    return m_id


def save_task_image_from_selected(m_id, config=None, logger=None, demo_cahce_file=None, selected='image_temp'):
    """将 m_id 对应资源目录下的选定图片（如 image_temp 图片）保存为 image_save（flask 和引擎后端都可以调用）
    m_id：资源标识（在本函数内生成），格式：年月日-小时-分钟-hash，创建时当前时间
    """

    if not config or not logger:
        raise Exception('config or logger MUST be set!')
    
    if 'STORAGE_TYPE' in dir(config): # in engine
        storage_type = config.STORAGE_TYPE
        upload_folder = config.UPLOAD_FOLDER
    else: # in Flask
        storage_type = config['STORAGE_TYPE']
        upload_folder = config['UPLOAD_FOLDER']
    
    # 本地文件存储
    if storage_type == 'local':

        if m_id and not m_id_valid(m_id):
            raise Exception('invalid m_id: {}'.format(m_id))
        
        file_dir = join(upload_folder, m_id.replace('-', '/')) # 根据 m_id 生成存储路径
        # 如果是 demo 图片，则从缓存目录中拷贝过去
        if demo_cahce_file:
            file_from = demo_cahce_file
            print('--> save task image from demo cache file')
            #shutil.copyfile(file_from, join(file_dir, config['SAVE_FILE_NAME'][selected]))
        else:
            file_from = join(file_dir, config['SAVE_FILE_NAME'][selected])
        file_to = join(file_dir, config['SAVE_FILE_NAME']['image_save'])
        shutil.copyfile(file_from, file_to)
        
        logger.info('temp image saved to local file: %s' % file_to)
        
    # amazon s3 云存储
    elif storage_type == 'amz_s3':
        logger.debug('not supported yet.')
        #TODO: 实现该云存储方式支持
    
    # 其他存储方式
    else:
        logger.debug('unkown storage type.')

    return m_id


def load_task_obj_data(file_name, m_id, config=None, logger=None):
    """根据 m_id 从本地或云存储中读取图片等内容（主要被后端调用）
    m_id 格式为：年月日-小时-分钟-hash，存储目录从其解析而来，文件名称在配置中有定义
    """

    if not config or not logger:
        raise Exception('config or logger MUST be set!')
    
    obj_data = None

    if 'STORAGE_TYPE' in dir(config): # in engine
        storage_type = config.STORAGE_TYPE
        upload_folder = config.UPLOAD_FOLDER
    else: # in Flask
        storage_type = config['STORAGE_TYPE']
        upload_folder = config['UPLOAD_FOLDER']
    
    # 本地文件存储
    if storage_type == 'local':
        # 根据 m_id 生成文件路径，并读取之
        if m_id and not m_id_valid(m_id):
            raise Exception('invalid m_id: {}'.format(m_id))
        file_dir = join(upload_folder, m_id.replace('-', '/'))
        full_name = join(file_dir, file_name)
        if full_name.rsplit('.', 1)[1].lower() in config.UPLOAD_ALLOWED_EXTS:
            obj_data = Image.open(full_name, "r")
        else:
            with open(full_name, 'rb') as file:
                obj_data = pickle.load(file)
        logger.info('obj_data loaded from local file: %s' % full_name)
    
    # amazon s3 云存储
    elif storage_type== 'amz_s3':
        logger.debug('not supported yet.')
        #TODO: 实现该云存储方式支持
    
    # 其他存储方式
    else:
        logger.debug('unkown storage type.')
    
    return obj_data
    

def m_id_valid(m_id):
    """判断 m_id 资源标识取值是否合法
    m_id 格式：年月日-小时-分钟-hash"""

    if m_id.count('-') != 3 or m_id.count('--') > 0:
        return False
    else:
        return True
    

def make_cache_file_name(func_class=None, func_group=None, func_name=None, func_args=None):
    """根据 task 的 func_xxx 等参数，生成图片处理结果缓存文件名"""

    cache_file_name = 'result'
    if func_class:
        cache_file_name += '-' + func_class
    if func_group:
        cache_file_name += '-' + func_group
    if func_name:
        cache_file_name += '-' + func_name
    if func_args:
        cache_file_name += '-' + str(func_args)
    
    cache_file_name += '.png'

    return cache_file_name
