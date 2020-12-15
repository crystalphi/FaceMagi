# -*- coding: utf-8 -*-

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
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .UGATIT import UGATIT
from .utils import show_all_variables, str2bool
from .. import check_if_save_demo_icon


script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_ICON_DIR = os.path.join(app_config.STATIC_FOLDER, 'ui_data/modules')

# 是否开启超解析处理
ENABLE_ESRGAN = False


def init_model(gpu_id=-1):

    args = parse_args()

    # open session
    #tf.reset_default_graph()
    sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
    gan = UGATIT(sess, args)

    # build graph
    gan.build_model()

    # show network architecture
    show_all_variables()

    # load checkpoint
    tf.global_variables_initializer().run(session=sess)
    gan.saver = tf.train.Saver()
    checkpoint_dir = os.path.join(app_config.MODEL_DIR, 'UGATIT/checkpoint-tf')
    could_load, checkpoint_counter = gan.load(checkpoint_dir)
    if could_load:
        logger.info(" [*] Load checkpoint SUCCESS")
    else :
        logger.error(" [!] Load checkpoint failed... {}".format(checkpoint_dir))

    model = {}
    model['args'] = args
    model['gan'] = gan
    model['model_size'] = 256 # default 256

    logger.info('ugatit init_model done! gpu_id: {}'.format(gpu_id))

    #if ENABLE_ESRGAN:
    #    model['esrgan'] = esrgan_adapter.init_model(gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    return model


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

    # 处理图片
    _img_out_pil = engine_process_image(engine_model, _img, func_name)

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

    return _img_out_pil


def engine_process_image(model, image, func_name):
    #args = model['args']
    gan = model['gan']

    image_return = gan.test_image(image)

    return image_return


def parse_args():
    desc = "Tensorflow implementation of U-GAT-IT"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--phase', type=str, default='test', help='[train / test]')
    parser.add_argument('--light', type=str2bool, default=False, help='[U-GAT-IT full version / U-GAT-IT light version]')
    parser.add_argument('--dataset', type=str, default='selfie2anime', help='dataset_name')

    parser.add_argument('--epoch', type=int, default=100, help='The number of epochs to run')
    parser.add_argument('--iteration', type=int, default=10000, help='The number of training iterations')
    parser.add_argument('--batch_size', type=int, default=1, help='The size of batch size')
    parser.add_argument('--print_freq', type=int, default=1000, help='The number of image_print_freq')
    parser.add_argument('--save_freq', type=int, default=1000, help='The number of ckpt_save_freq')
    parser.add_argument('--decay_flag', type=str2bool, default=True, help='The decay_flag')
    parser.add_argument('--decay_epoch', type=int, default=50, help='decay epoch')

    parser.add_argument('--lr', type=float, default=0.0001, help='The learning rate')
    parser.add_argument('--GP_ld', type=int, default=10, help='The gradient penalty lambda')
    parser.add_argument('--adv_weight', type=int, default=1, help='Weight about GAN')
    parser.add_argument('--cycle_weight', type=int, default=10, help='Weight about Cycle')
    parser.add_argument('--identity_weight', type=int, default=10, help='Weight about Identity')
    parser.add_argument('--cam_weight', type=int, default=1000, help='Weight about CAM')
    parser.add_argument('--gan_type', type=str, default='lsgan', help='[gan / lsgan / wgan-gp / wgan-lp / dragan / hinge]')

    parser.add_argument('--smoothing', type=str2bool, default=True, help='AdaLIN smoothing effect')

    parser.add_argument('--ch', type=int, default=64, help='base channel number per layer')
    parser.add_argument('--n_res', type=int, default=4, help='The number of resblock')
    parser.add_argument('--n_dis', type=int, default=6, help='The number of discriminator layer')
    parser.add_argument('--n_critic', type=int, default=1, help='The number of critic')
    parser.add_argument('--sn', type=str2bool, default=True, help='using spectral norm')

    parser.add_argument('--img_size', type=int, default=256, help='The size of image')
    parser.add_argument('--img_ch', type=int, default=3, help='The size of image channel')
    parser.add_argument('--augment_flag', type=str2bool, default=True, help='Image augmentation use or not')

    parser.add_argument('--checkpoint_dir', type=str, default='checkpoint',
                        help='Directory name to save the checkpoints')
    parser.add_argument('--result_dir', type=str, default='results',
                        help='Directory name to save the generated images')
    parser.add_argument('--log_dir', type=str, default='logs',
                        help='Directory name to save training logs')
    parser.add_argument('--sample_dir', type=str, default='samples',
                        help='Directory name to save the samples on training')

    return parser.parse_args()
