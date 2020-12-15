# -*- coding: utf-8 -*-
"""
model: Functions related to Deep Learning model.
api: api views used by Flask server.
"""
__author__ = "vedasky"
__copyright__ = "Copyright 2019"

import os
import argparse
import json
#import cv2
import numpy as np
from skimage import transform, util
from os.path import join
from PIL import Image

import torch

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .attgan import AttGAN
from .data import check_attribute_conflict, MyTestData
from .helpers import Progressbar
from .util import find_model, save_image


script_dir = os.path.dirname(os.path.abspath(__file__))

# 是否开启超解析处理
ENABLE_ESRGAN = True  # 若开启，人脸图片会先缩放为标准尺寸进行处理，然后再超解析扩展为原尺寸


def init_model(experiment_name='384_shortcut1_inject0_none_hq', gpu_id=-1):
    """Function that loads Deep Learning model.
    Args: 
        experiment_name: 384_shortcut1_inject0_none_hq, 384_shortcut1_inject1_none_hq 或其他
    Returns:
        model: Loaded Deep Learning model.
    """

    with open(join(script_dir, 'output', experiment_name, 'setting.txt'), 'r') as f:
        args = json.load(f, object_hook=lambda d: argparse.Namespace(**d))
    logger.info('torch version: {}'.format(torch.version.__version__))

    args.gpu_id = gpu_id
    args.load_epoch = 'latest'
    args.num_test = None
    args.my_data = './data/my'
    args.my_attr = './data/list_attr_my.txt'
    logger.info('args: {}'.format(args))

    os.makedirs(join(script_dir, args.my_data), exist_ok=True)

    attgan = AttGAN(args)
    attgan.load(find_model(
        join(script_dir, 'output', args.experiment_name, 'checkpoint'), args.load_epoch))
    attgan.eval()

    model = {}
    model['attgan'] = attgan
    model['args'] = args
    model['model_size'] = 384 # attgan_pt 所用的模型尺寸为384

    #if ENABLE_ESRGAN:
    #    model['esrgan'] = esrgan_adapter.init_model(gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    logger.info('attgan_pt init_model done! gpu_id: {}'.format(gpu_id))
    return model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
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

        face_image_orig = image_ndarray_to_pil(_img_np)

        # 如果 face_image 尺寸大于模型标准尺寸，则缩放为标准尺寸再处理
        _img_w, _img_h = w, h
        _h = engine_model['model_size']
        if _img_h != _h:
            _img = image_resize_default(image_ndarray_to_pil(_img_np), _h)
            _img_np = image_pil_to_ndarray(_img)

        # 使用 face_image 构造测试数据集，包括内容、特征和大小
        logger.info('face_image attr: {}, h {}. model size: {}.'.format(face_data['attr'], h, _h))
        _test_dataset = MyTestData(_img_np, face_data['attr'], _h)

        # 处理图片
        # test_atts 为目的特征列表；test_ints 为相应特征处理强度，取值 0~1
        test_atts, test_ints = func_name, func_params[0]
        logger.info('func_params: {}, test_atts: {}, test_ints: {}'
                    .format(func_params, test_atts, test_ints))
        _img_out_pil = attgan_multi_process(
            engine_model, _test_dataset, test_atts, test_ints)

        # 如果为调试模式，则保存生成的人脸图片做分析用，产品化部署不需要
        #if app_config.DEBUG:
        #    out_file = os.path.join(script_dir, 'new_face.jpg')
        #    _img_out_pil.save(out_file)
        #    print('new image saved to {:s} done!'.format(out_file))

        # 将返回图片缩放为原尺寸
        if _img_h != _h:
            if _img_h > _h and ENABLE_ESRGAN:
                #_img_out_pil = esrgan_adapter.process_image(
                #    _img_out_pil, engine_model['esrgan'], w, h)
                # 调用管理进程共享对象接口处理
                ret = exec_esrgan(_img_out_pil, _img_w, _img_h, worker)
                if ret:
                    _img_out_pil = ret
                else:
                    _img_out_pil = image_resize_default(_img_out_pil, _img_h)
        else:
            _img_out_pil = image_resize_default(_img_out_pil, _img_h)

        # 将新旧人脸混合后贴回原图
        x = x + int((image.size[0] - app_config.OUTPUT_SIZE_EDITOR[0]) / 2)
        y = y + int((image.size[1] - app_config.OUTPUT_SIZE_EDITOR[1]) / 2)
        edit_area = func_params[1]
        image_output = face_image_blend(image, _img_out_pil,
                                        face_image_orig, x, y, w, h, edit_area, worker)

    return image_output


def attgan_multi_process(model, test_dataset, test_atts, test_ints):
    attgan = model['attgan']
    args = model['args']

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1, num_workers=args.num_workers,
        shuffle=False, drop_last=False
    )
    if args.num_test is None:
        print('Testing images:', len(test_dataset))
    else:
        print('Testing images:', min(len(test_dataset), args.num_test))

    image_return = None

    for idx, (img_a, att_a) in enumerate(test_dataloader):
        if args.num_test is not None and idx == args.num_test:
            break

        if args.gpu_id >= 0:
            with torch.cuda.device(args.gpu_id):
                img_a = img_a.cuda()
                att_a = att_a.cuda()
        att_a = att_a.type(torch.float)
        att_b = att_a.clone()

        for a in test_atts:
            i = args.attrs.index(a)
            att_b[:, i] = 1 - att_b[:, i]
            att_b = check_attribute_conflict(att_b, args.attrs[i], args.attrs)

        with torch.no_grad():
            att_b_ = (att_b * 2 - 1) * args.thres_int
            for a, i in zip(test_atts, test_ints):
                att_b_[..., args.attrs.index(
                    a)] = att_b_[..., args.attrs.index(a)] * i / args.thres_int
            samples = []
            img_a_new = attgan.G(img_a, att_b_)
            img_a_new = (img_a_new + img_a) / 2  # 将新旧人脸做 alpha 混合，以使图片更自然
            samples.append(img_a_new)
            samples = torch.cat(samples, dim=3)
            image_return = save_image(samples, nrow=1, normalize=True,
                                      range=(-1., 1.), scale_each=False)

    # 读取和返回处理后的图片
    return image_return
