# -*- coding: utf-8 -*-
# Facelet_Bank 的产品化功能封装

import os
import sys
import io
import time
import glob
import cv2
import argparse
import numpy as np
from imageio import imread, imsave, imwrite
from PIL import Image
#from PIL import ImageEnhance

import torch
from torch.utils.data import DataLoader

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
                                image_blend, image_ndarray_to_pil, image_pil_to_ndarray
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .network.base_network import VGG
from .network.decoder import vgg_decoder
from .network.facelet_net import Facelet
from .data.testData import untransform
from .util import util, test_parse
from .data.testData import ImageDataset


script_dir = os.path.dirname(os.path.abspath(__file__))

# 是否开启超解析处理
ENABLE_ESRGAN = False # 若开启，人脸图片会先缩放为标准尺寸进行处理，然后再超解析扩展为原尺寸


def init_model(gpu_id=-1, effect=None):

    parser = test_parse.ArgumentParser()
    args = parser.parse_args()
    args.local_model = True
    args.pretrained = not args.local_model
    if gpu_id >= 0:
        args.gpu_id = gpu_id
    
    if effect not in ('facehair', 'feminization', 'masculinization', 'older', 'younger'):
        raise Exception('unsupported effect: {}'.format(effect))
    
    # 不同 effect 是在一个子进程中加载好，还是分为不同子进程加载好？
    # 分析结论：不同进程可能更合适，可以更好地并行处理，发挥多进程和多显卡的优势。
    facelet = Facelet(args)
    if args.local_model:
        #pretrain_path = 'checkpoints'
        pretrain_path = 'facelet_bank'
        pretrain_path = os.path.join(app_config.MODEL_DIR, pretrain_path)
        facelet.load(effect, pretrain_path)
    
    vgg = VGG()
    
    logger.info('torch version: {}'.format(torch.version.__version__))
    decoder = vgg_decoder()
    
    if args.gpu_id >= 0:
        with torch.cuda.device(args.gpu_id):
            #vgg = vgg.cuda()
            vgg = torch.nn.DataParallel(vgg).cuda()
            facelet = facelet.cuda()
            decoder = decoder.cuda()

    model = {}
    model['args'] = args
    model['vgg'] = vgg
    model['facelet'] = facelet
    model['decoder'] = decoder
    model['model_size'] = 384

    #if ENABLE_ESRGAN:
    #    model['esrgan'] = esrgan_adapter.init_model(gpu_id=app_config.ENGINE_GPU_ID['esrgan'])
    
    logger.info('facelet_pt init_model done! gpu_id: {}, effect: {}'
                .format(gpu_id, effect))
    return model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
    Returns:
        image_output: 处理后的图片数据
    注意：对于 facelet_pt 来说，由于引擎是根据 effect 分别在子进程中加载的，所以这里 func_name 没用到
    """

    logger.info('call process_image. func_name: "{}", func_params: "{}"'
                .format(func_name, func_params))

    # 处理和替换图片中的人脸部分
    if 'face_image' in face_data:
        _img_np = face_data['face_image']
        x = face_data['x']
        y = face_data['y']
        w = face_data['w']
        h = face_data['h']
        
        face_image_orig = image_ndarray_to_pil(_img_np)
        
        # 由于真实处理过程使用CPU执行太慢，笔记本上运行会导致任务超时，故暂时用 sleep 模拟之
        run_fake = False # 笔记本上运行设为 True，开发和生产服务器上为 False
        if run_fake:
            time.sleep(3)
            _img_out_pil = image_ndarray_to_pil(_img_np)
        else:
            # 如果 face_image 尺寸大于模型标准尺寸，则缩放为标准尺寸再处理
            _img_w, _img_h = w, h
            _h = engine_model['model_size']
            if _img_h != _h:
                _img = image_resize_default(image_ndarray_to_pil(_img_np), _h)
                _img_np = image_pil_to_ndarray(_img)
            
            _img_out = engine_process_image(engine_model, _img_np,
                                            func_name, func_params)
            
            # ndarray/Tensor 转成PIL.Image
            _img_out_pil = image_ndarray_to_pil(_img_out)
            
            # 如果为调试模式，则保存生成的人脸图片做分析用，产品化部署不需要
            if app_config.DEBUG:
                out_file = os.path.join(script_dir, 'new_face.jpg')
                _img_out_pil.save(out_file)
                print('new image saved to {:s} done!'.format(out_file))

            # 将返回图片缩放为原尺寸
            if _img_h != _h:
                if _img_h > _h and ENABLE_ESRGAN:
                    #_img_out_pil = esrgan_adapter.process_image(
                    #          _img_out_pil, engine_model['esrgan'], w, h)
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
        edit_area = []
        image_output = face_image_blend(image, _img_out_pil,
                                        face_image_orig, x, y, w, h, edit_area, worker)

    return image_output


def engine_process_image(model, face_image, func_name, func_params):
    """
    face_image：人脸图片内容，tensor/ndarray
    """
    args = model['args']
    vgg = model['vgg']
    facelet = model['facelet']
    decoder = model['decoder']

    image_list = [face_image]
    dataset = ImageDataset(image_list, scale=util.str2numlist(args.size))
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False, num_workers=0)
    
    output = None
    for data in dataloader:
        image, image_shape = data
        image = util.toVariable(image)
        if args.gpu_id >= 0:
            with torch.cuda.device(args.gpu_id):
                image = image.cuda()
        
        vgg_feat = vgg.forward(image)
        w = facelet.forward(vgg_feat)
        #strength = args.strength
        strength = func_params[0]
        #print('--> effect strength:', strength)
        vgg_feat_transformed = [vgg_feat_ + strength * w_ for vgg_feat_, w_ in zip(vgg_feat, w)]
        output = decoder.forward(vgg_feat_transformed, image)
        output = untransform(output.data[0].cpu())
        #imwrite(os.path.join(script_dir, 'f1.jpg'), output)
        output = util.center_crop(output, (image_shape[0][0], image_shape[1][0]))
        #imwrite(os.path.join(script_dir, 'f2.jpg'), output)

        break
    
    return output


def preprocess(img):
    return (img / 255. - 0.5) * 2


def deprocess(img):
    return (img + 1) / 2


if __name__ == '__main__':

    img_input_filename = os.path.join(script_dir, '../../../static/attgan_pt/vvdd-11.jpg')
    img_input = cv2.imread(img_input_filename)
    img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)

    model = init_model()

    result = engine_process_image(model, img_input, None)

    imsave('result.jpg', result)
