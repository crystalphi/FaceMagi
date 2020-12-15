# -*- coding: utf-8 -*-
# TODO: 本模型在泛化、合并及性能上不及 BeautyGAN-using-web-camra，且为 TF 框架，应替代之

import tensorflow as tf
import numpy as np
import os
import sys
import io
import time
import glob
import cv2
import argparse
from imageio import imread, imsave
from PIL import Image
#from PIL import ImageEnhance

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray, list_all_files
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .. import check_if_save_demo_icon


script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_ICON_DIR = os.path.join(app_config.STATIC_FOLDER, 'ui_data/modules/btg')

# 是否开启超解析处理
ENABLE_ESRGAN = True


def init_model(gpu_id=-1, model_size=256): #default model_size 256

    tf.reset_default_graph()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph(
        os.path.join(script_dir, 'model', 'model.meta'))
    saver.restore(sess, tf.train.latest_checkpoint(
        os.path.join(script_dir, 'model')))

    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name('X:0')
    Y = graph.get_tensor_by_name('Y:0')
    Xs = graph.get_tensor_by_name('generator/xs:0')

    model = {}
    model['sess'] = sess
    model['X'] = X
    model['Y'] = Y
    model['Xs'] = Xs

    model['model_size'] = model_size
    print('set model_size: {0}'.format(model_size))

    makeup_files = glob.glob(os.path.join(script_dir, 'imgs', 'makeup', '*.*'))
    #print('--> makeup_files: {0}'.format(makeup_files))
    model['makeups'] = {makeup_files[i].split('/')[-1].split('.')[0]: cv2.resize(
        imread(makeup_files[i]), (model_size, model_size)) for i in range(len(makeup_files))}
    for k in model['makeups']:
        model['makeups'][k] = cv2.cvtColor(model['makeups'][k], cv2.COLOR_RGBA2RGB)
    
    model['all_styles'] = get_all_styles()
    
    #if ENABLE_ESRGAN:
    #    model['esrgan'] = esrgan_adapter.init_model(gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    logger.info('beautygan init_model done! gpu_id: {}, loaded makeups: {}'
                .format(gpu_id, model['makeups'].keys()))
    return model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
    Returns:
        image_output: 处理后的图片数据
    """

    if 'img_hash' not in face_data: # 本引擎只能处理人脸图片
        return None
    else:
        #return process_image_xxx(image, face_data, engine_model, func_name, func_params, worker)
        return process_image_yyy(image, face_data, engine_model, func_name, func_params, worker)


def process_image_xxx(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理（直接处理整张图片）
    Returns:
        image_output: 处理后的图片数据
    """

    # 处理和替换图片中的人脸部分
    # ！！直接使用 pil 原图而不是 face_data 中的人脸图做处理
    
    # 如果 image 尺寸不等于模型标准尺寸，则缩放为标准尺寸再处理
    _img_w, _img_h = image.size[0:2]
    _h = engine_model['model_size']
    if _img_h != _h:
        _img_pil = image_resize_default(image, _h)
    else:
        _img_pil = image
    _img_np = image_pil_to_ndarray(_img_pil)

    # 处理图片（返回的已经是 PIL Image）
    _img_out_pil = engine_process_image(engine_model, _img_np, func_name)

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
            check_if_save_demo_icon(_img_out_pil, SAVE_ICON_DIR, func_name)

    # 将新旧人脸混合后贴回原图
    x, y = 0, 0
    w, h = image.size[0], image.size[1]
    edit_area = func_params[1]
    _img_out_pil = face_image_blend(_img_out_pil, _img_out_pil,
                                    image, x, y, w, h, edit_area, worker)

    return _img_out_pil


def process_image_yyy(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理（截取人脸部分做替换处理）
    Returns:
        image_output: 处理后的图片数据
    """

    # 处理和替换图片中的人脸部分
    if 'face_image' in face_data:
        _img_np = face_data['face_image']
        x = face_data['x']
        y = face_data['y']
        w = face_data['w']
        h = face_data['h']
        img_hash = face_data['img_hash']

        face_image_orig = image_ndarray_to_pil(_img_np)

        # 如果 face_image 尺寸大于模型标准尺寸，则缩放为标准尺寸再处理
        _img_w, _img_h = w, h
        _h = engine_model['model_size']
        _img = image_ndarray_to_pil(_img_np)
        if _img_h != _h:
            _img = image_resize_default(_img, _h)
            _img_np = image_pil_to_ndarray(_img)

        # 处理图片（返回的已经是 PIL Image）
        _img_out_pil = engine_process_image(engine_model, _img_np, func_name)

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
                check_if_save_demo_icon(_img_out_pil, SAVE_ICON_DIR, func_name)

        # 将新旧人脸混合后贴回原图
        x = x + int((image.size[0] - app_config.OUTPUT_SIZE_EDITOR[0]) / 2)
        y = y + int((image.size[1] - app_config.OUTPUT_SIZE_EDITOR[1]) / 2)
        edit_area = func_params[1]
        image_output = face_image_blend(image, _img_out_pil,
                                        face_image_orig, x, y, w, h, edit_area, worker)

    return image_output


def engine_process_image(model, face_image, func_name):
    model_size = model['model_size']
    all_styles = model['all_styles']

    no_makeup = cv2.resize(face_image, (model_size, model_size))
    X_img = np.expand_dims(preprocess(no_makeup), 0)

    if func_name not in all_styles:
        raise Exception('no such style: {}'.format(func_name))

    makeup = model['makeups'][func_name]
    Y_img = np.expand_dims(preprocess(makeup), 0)
    print('--> run... X_img.shape: {}, Y_img.shape: {}'.format(X_img.shape, Y_img.shape))
    Xs_ = model['sess'].run(model['Xs'], feed_dict={
                            model['X']: X_img, model['Y']: Y_img})
    print('--> run ok')
    Xs_ = deprocess(Xs_)
    img = tf.image.encode_jpeg(Xs_[0] * 255).eval(session=model['sess'])
    image_return = Image.open(io.BytesIO(img))
    #print('--> type(image_return): {0}'.format(type(image_return)))
    
    return image_return


def preprocess(img):
    return (img / 255. - 0.5) * 2


def deprocess(img):
    return (img + 1) / 2


def get_all_styles():
    all_styles = {}
    style_files = list_all_files(os.path.join(script_dir, 'imgs/makeup'))
    for i in style_files:
        _key = i.split('/')[-1].split('.')[0]
        all_styles[_key] = i
    
    #print('--> all_styles:', all_styles)
    return all_styles


if __name__ == '__main__':

    model_size = 256

    img_input_filename = os.path.join('imgs', 'no_makeup', 'vvdd-11.jpg')
    img_input = cv2.imread(img_input_filename)
    img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
    no_makeup = cv2.resize(img_input, (model_size, model_size))

    makeups = glob.glob(os.path.join('imgs', 'makeup', '*.*'))

    result = np.ones((2 * model_size, (len(makeups) + 1) * model_size, 3))
    result[model_size: 2 * model_size, :model_size] = no_makeup / 255.

    model = init_model()

    X_img = np.expand_dims(preprocess(no_makeup), 0)
    for i in range(len(makeups)):
        makeup = cv2.resize(imread(makeups[i]), (model_size, model_size))
        Y_img = np.expand_dims(preprocess(makeup), 0)
        Xs_ = model['sess'].run(model['Xs'], feed_dict={
                                model['X']: X_img, model['Y']: Y_img})
        Xs_ = deprocess(Xs_)
        result[:model_size, (i + 1) * model_size: (i + 2)
               * model_size] = makeup / 255.
        result[model_size: 2 * model_size,
               (i + 1) * model_size: (i + 2) * model_size] = Xs_[0]
        
        if True:
            image_return = Image.fromarray(makeup / 255., mode="RGB")
            out_file = os.path.join(script_dir, 'new_face.jpg')
            image_return.save(out_file)
            print('new image saved to {:s} done!'.format(out_file))

    imsave('result.jpg', result)
