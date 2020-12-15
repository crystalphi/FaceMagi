# -*- coding: utf-8 -*-
""" 工作引擎模块包。本文件主要定义其处理入口函数及通用部分。
"""

import os
import time
import multiprocessing
import logging
from logging.handlers import RotatingFileHandler
from PIL import Image
from PIL import ImageDraw

from app.config import config, set_logger
from app.engine_v1.utils import image_convert_rgb, \
    image_resize_default, image_blend


app_config = config[os.environ.get("FLASK_ENV") or "default"]()

# 设置日志参数，默认终端输出
multiprocessing.log_to_stderr()
logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)
set_logger(logger, app_config.LOG_PATH_ENGINE_INFO, app_config.LOG_PATH_ENGINE_ERROR,
                   app_config.LOG_FILE_MAX_BYTES, app_config.LOG_FILE_BACKUP_COUNT)


def image_process_wrap(image, face_data=None, entry_process_image=None, engine_model=None,
                      func_class='fc_editor', func_group=None, func_name=None, func_params=None,
                      output_size_w=400, output_size_h=500, worker=None):
    """ 本函数包括两个功能：
      1、face_data 为空时做图片预处理，主要是缩放为标准大小；
      2、face_data 非空时做图片编辑处理，回调函数进行处理。
    输出尺寸比例（output_size_w : output_size_h）应为 4:5，如 400x500 或 720x900。
    """

    if not image:
        raise Exception('image_process_wrap(): input image cannot be None!')
    
    # 1. 将 png 等图片统一转为 jpg 格式
    image = image_convert_rgb(image)

    # 2. 根据图片尺寸判断是否归一化，并做相应的缩放裁剪
    output_size_w, output_size_h = app_config.OUTPUT_SIZE_EDITOR # 归一化后的标准尺寸
    img_w, img_h = image.size
    print('func_class: {}; img_w: {}, img_h: {}; output size w: {}, h: {}'
          .format(func_class, img_w, img_h, output_size_w, output_size_h))
    
    needNormalize = False # 是否需要进行进行归一化
    if img_w != output_size_w or img_h != output_size_h:
        needNormalize = True
    
    if needNormalize:
        # 图片裁剪为最大 output_size_w,output_size_h：大图片缩放裁剪、保留短边；小图片保持原尺寸
        if img_w > output_size_w:  # 过宽的，等比缩小为输出宽度 output_size_w
            newWidth = output_size_w
            newHeight = int(float(output_size_w) / img_w * img_h)
            image = image.resize((newWidth, newHeight), Image.ANTIALIAS)
            #image = image.thumbnail((newWidth, newHeight), Image.ANTIALIAS)
        img_w, img_h = image.size
        if img_h > output_size_h:  # 过高的，居中裁剪为输出高度 output_size_h
            x0 = 0
            y0 = int((img_h - output_size_h) / 2)
            x1 = output_size_w
            y1 = y0 + output_size_h
            image = image.crop((x0, y0, x1, y1))
        img_w, img_h = image.size
    
    # 3. 居中扩展为正方形，宽高都为 output_size_h
    # image_norm = Image.new('RGBA', (output_size_h, output_size_h)) # 带透明信息
    image_norm = Image.new('RGB', (output_size_h, output_size_h),
                        (255, 255, 255))  # 不带透明信息
    x = int((output_size_h - img_w) / 2)
    y = int((output_size_h - img_h) / 2)
    image_norm.paste(image, (x, y))

    image_out = image_norm
    # 4. 将上述正方形图片交给引擎处理
    if entry_process_image and hasattr(entry_process_image, '__call__'):
        #for v in func_params:
        #    print('--> Optional argument (*args): ', v)
        ## 如果输入参数中有 **func_kwargs，则可以如下读取：
        #for k, v in func_kwargs.items():
        #    print('--> Optional argument %s (*kwargs): %s' % (k, v))

        # 调用引擎回调函数对图片进行处理
        #logger.info('call {}, func_name: {}, func_params: {}'.format(entry_process_image, func_name, func_params))
        image_out = entry_process_image(image_norm, face_data, 
                                        engine_model, func_name, func_params, worker=worker)
        if not image_out:
            image_norm.close()
            return None

    # 4. 处理后的图片再去扩展，恢复为步骤 1 后的尺寸（最大output_size_w,output_size_h），保存后返回给客户端
    img_w, img_h = output_size_w, output_size_h  # 使用指定输出尺寸，替代步骤 1 后的尺寸
    x0 = int((output_size_h - img_w) / 2)
    y0 = int((output_size_h - img_h) / 2)
    x1 = x0 + img_w
    y1 = y0 + img_h
    image_out = image_out.crop((x0, y0, x1, y1))
    image_norm.close()

    #logger.info('image wrap process done!')

    # 根据任务类型返回不同大小的输出图片
    if func_class == 'fc_fun':
        _img_w, _img_h = app_config.OUTPUT_SIZE_FUN
        image_out = image_resize_default(image_out, _img_h)
    
    return image_out


def face_image_blend(image_output, face_image_new, face_image_orig,
                       x, y, w, h, edit_area=None, worker=None):
    """替换输出图片中的人脸部分
    将新的人脸图与原人脸图按比例融合，然后平滑替换到输出图中指定位置"""

    logger.info('call face_image_blend. x, y, w, h: {}, {}, {}, {}'
                .format(x, y, w, h))
    #print('--> image_output.size: {}, face_image_new.size: {}, face_image_orig.size: {}'
    #      .format(image_output.size, face_image_new.size, face_image_orig.size))
    #print('--> type(image_output): {}, type(face_image_new): {}'
    #      .format(type(image_output), type(face_image_new)))
    
    # 将处理后的人脸缩放为检测时的尺寸，然后按照相应坐标替换到原图中
    face_image_new = image_resize_default(face_image_new, h)
    
    # 将处理后的人脸与原人脸做 alpha 混合，以平滑图像（会降低效果，暂无必要）
    #face_image_new = image_blend(face_image_orig, face_image_new, 0.7)
    
    # 设置掩模图片
    # 为减少不必要的修改、提高图片质量，可在task参数中设置要编辑的人脸区域
    logger.info('get face mask with area: {}'.format(edit_area))
    mask = None
    if edit_area != None:
        if len(edit_area) == 0: # 如未指定人脸部分，则使用人像全部
            edit_area = ['face', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 
                         'eye_g', 'l_ear', 'r_ear', 'ear_r', 'nose', 
                         'u_lip', 'l_lip', 'neck', 'neck_l', 'mouth',
                         'cloth', 'hat', 'hair']
        # 解析获取人脸掩模图片
        mask = mm_get_face_mask(face_image_new, edit_area, worker)
    if not mask:
        logger.info('call get_geometric_mask() to make mask')
        mask = get_geometric_mask(face_image_new) # 默认为椭圆型掩模图片

    # 参考掩模将处理后的人脸替换到图中
    #image_output.save('/app/app/dbg_image_output_1.png')
    image_output.paste(face_image_new, (x, y), mask)
    #image_output.save('/app/app/dbg_image_output_2.png')
    # 含义：使用变量mask对应的模板图像来填充所对应的区域。可以使用模式为“1”、“L”或者“RGBA”的图像作为模板图像。模板图像的尺寸必须与变量image对应的图像尺寸一致。如果变量mask对应图像的值为255，则模板图像的值直接被拷贝过来；如果变量mask对应图像的值为0，则保持当前图像的原始值。变量mask对应图像的其他值，将对两张图像的值进行透明融合。
    
    return image_output


def get_geometric_mask(face_image_new):
    """生成渐变椭圆形掩模"""
    w, h = face_image_new.size
    mask = Image.new('RGBA', (w,h), (255,0,0,0))
    pdraw = ImageDraw.Draw(mask)
    for i in range(32):
        pdraw.ellipse((0+i,0+i,w-i,h-i), fill=(255,8*i,8*i,8*i))
    return mask


def __mm_exec_task(t_type, args, worker):
    """调用管理进程的共享对象接口，执行超解析、人脸解析等任务。
    该函数为处理具体任务的基础函数。
    """

    # 添加超解析任务
    result = worker._mm_client.shared_obj_func_call(
        'shared_data_controller', 'add_task', (t_type, args))
    if result and result['return'] == 'success' and result['data'] is not None:
        t_id = result['data']
    else:
        logger.info('mm call shared_data_controller add_task({}...) failed.'.format(t_type))
        return None
    
    # 获取超解析结果
    time.sleep(1)
    for i in range(int(app_config.MM_TASK_EXPIRED * (1/0.2))):
        result = worker._mm_client.shared_obj_func_call(
            'shared_data_controller', 'get_task_result', (t_type, t_id))
        if result and result['return'] == 'success' and result['data'] is not None:
            return result['data']
        else:
            time.sleep(0.2)
    logger.info('mm call shared_data_controller get_task_result({}...): no result'.format(t_type))
    return None

def exec_esrgan(img_pil, img_w, img_h, worker):
    """调用管理进程的共享对象接口，获取超解析缩放图。
    该函数只在工作任务引擎子进程中调用。
    """
    
    return __mm_exec_task('esrgan', (img_pil, img_w, img_h), worker)

def mm_get_face_mask(face_image, edit_area, worker):
    """调用管理进程的共享对象接口，获取人脸掩码图。
    该函数只在工作任务引擎子进程中调用。
    """
    
    return __mm_exec_task('face_parsing', (face_image, edit_area), worker)


def save_cache_demo_image(img_pil, img_hash, cache_dir, cache_name):
    """将 app demo 图片处理结果保存为缓存文件"""

    if app_config.DEMO_CACHE_ENABLE:
        cache_dir = os.path.join(cache_dir, img_hash)
        os.makedirs(cache_dir, exist_ok=True)
        cache_file = os.path.join(cache_dir, cache_name)
        
        img_pil.save(cache_file)
        logger.info('saved result cache for demo image: {}'.format(cache_file))
