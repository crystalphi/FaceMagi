# -*- coding: utf-8 -*-

import os
import argparse
import numpy as np
import cv2
from imageio import imread, imsave
from PIL import Image
#from PIL import ImageEnhance

import tensorflow as tf

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray, list_all_files
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .style_transfer_net import StyleTransferNet
from .utils import get_images, save_image, save_images
from .. import check_if_save_demo_icon


script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_ICON_DIR = os.path.join(app_config.STATIC_FOLDER, 'ui_data/modules/ast')

# 是否开启超解析处理
ENABLE_ESRGAN = False  # 若开启，将采用超解析而不是简单方式对图片进行缩放


def init_model(gpu_id=-1, style='Hayao'):

    tf.Graph().as_default()
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

    # 这段代码只是用来查看 tf 的运行设备信息，没啥其他用途
    #a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    #b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    #c = tf.matmul(a, b)
    # print(sess.run(c))

    # build the dataflow graph
    content = tf.placeholder(tf.float32, shape=(1, None, None, 3), name='content')
    style = tf.placeholder(tf.float32, shape=(1, None, None, 3), name='style')

    encoder_path = os.path.join(app_config.MODEL_DIR, 'vgg19_normalised.npz')
    stn = StyleTransferNet(encoder_path)

    output_image = stn.transform(content, style)

    print(sess.run(tf.global_variables_initializer()))

    # restore the trained model and run the style transferring
    saver = tf.train.Saver()
    model_path = os.path.join(
        app_config.MODEL_DIR, 'arbitrary_style_transfer/models/style_weight_2e0.ckpt')
    saver.restore(sess, model_path)

    engine_model = {}
    engine_model['content'] = content
    engine_model['style'] = style
    engine_model['output_image'] = output_image
    engine_model['sess'] = sess
    engine_model['model_size'] = 500  # 模型未指定，使用标准大小 500（模型越大效果越好，耗时也越长）

    #if ENABLE_ESRGAN:
    #    engine_model['esrgan'] = esrgan_adapter.init_model(
    #        gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    logger.info(
        'arbitrary_style_transfer init_model done! gpu_id: {}, style: {}'.format(gpu_id, style))
    return engine_model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
    Returns:
        image_output: 处理后的图片数据
    """

    # ！！直接使用 pil 原图而不是 face_data 中的人脸图做处理

    # 如果 image 尺寸不等于模型标准尺寸，则缩放为标准尺寸再处理
    _img_w, _img_h = image.size[0:2]
    _h = engine_model['model_size']
    if _img_h != _h:
        _img = image_resize_default(image, _h)
    else:
        _img = image

    # 处理图片
    style_name = func_params[0]
    _img_out_pil = engine_process_image(engine_model, _img, style_name)

    # 将返回图片缩放为原尺寸
    if _img_h != _h:
        if _img_h > _h and ENABLE_ESRGAN:
            #_img_out_pil = esrgan_adapter.process_image(
            #    _img_out_pil, engine_model['esrgan'], _img_w, _img_h)
            # 调用管理进程共享对象接口处理
            ret = exec_esrgan(_img_out_pil, _img_w, _img_h, worker)
            if ret:
                _img_out_pil = ret
            else:
                _img_out_pil = image_resize_default(_img_out_pil, _img_h)
        else:
            _img_out_pil = image_resize_default(_img_out_pil, _img_h)

    # 检查是否为主demo，若是则将人脸处理结果保存为图标
    if 'img_hash' in face_data:
        img_hash = face_data['img_hash']
        if img_hash in app_config.IMG_HASH_ICON_DEMO: # 为生成界面图标用的指定图片
            check_if_save_demo_icon(_img_out_pil, SAVE_ICON_DIR, style_name)

    return _img_out_pil


def engine_process_image(engine_model, image, style_name):
    content = engine_model['content']
    style = engine_model['style']
    output_image = engine_model['output_image']
    sess = engine_model['sess']

    content_img = [image_pil_to_ndarray(image)]
    content_img = np.stack(content_img, axis=0)

    # 根据 style_name 获取风格图片路径
    _styles_dict = get_all_styles()
    if style_name not in _styles_dict:
        raise Exception('no such style: {}'.format(style_name))
    style_img = get_images(_styles_dict[style_name])

    logger.info('processing image with style %s' % style_name)
    result = sess.run(output_image,
                      feed_dict={content: content_img, style: style_img})

    _img_out = result[0].astype('uint8')
    #print('--> type of _img_out:', type(_img_out))
    image_return = image_ndarray_to_pil(_img_out)

    return image_return


def get_all_styles():
    styles_dict = {}
    style_files = list_all_files(os.path.join(script_dir, 'images/style'))
    for i in style_files:
        _key = i.split('/')[-1].split('.')[0]
        styles_dict[_key] = i
    
    #print('--> styles_dict:', styles_dict)
    return styles_dict
