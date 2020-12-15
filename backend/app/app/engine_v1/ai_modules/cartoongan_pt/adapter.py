# -*- coding: utf-8 -*-

import torch
import os
import argparse
from PIL import Image
#from PIL import ImageEnhance
import numpy as np
from imageio import imread, imsave
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.utils as vutils

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .network.Transformer import Transformer
from .. import check_if_save_demo_icon


script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_ICON_DIR = os.path.join(app_config.STATIC_FOLDER, 'ui_data/modules/ctg')

# 是否开启超解析处理
ENABLE_ESRGAN = False  # 若开启，将采用超解析而不是简单方式对图片进行缩放


def init_model(gpu_id=-1, style='Hayao'):

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', default='test_img')
    parser.add_argument('--load_size', default=360)  # 默认模型处理尺寸 450（越大所需显存越多，默认时为3.6G）
    parser.add_argument('--model_path', default='./pretrained_model')
    parser.add_argument('--style', default='Hayao')
    parser.add_argument('--output_dir', default='test_output')
    parser.add_argument('--gpu', type=int, default=0)
    opt = parser.parse_args()
    opt.gpu = gpu_id
    opt.style = style

    # load pretrained model
    model = Transformer()
    model.load_state_dict(torch.load(os.path.join(
        script_dir, opt.model_path, opt.style + '_net_G_float.pth')))
    model.eval()

    if opt.gpu > -1:
        print('GPU mode')
        model.cuda()
    else:
        print('CPU mode')
        model.float()

    engine_model = {}
    engine_model['opt'] = opt
    engine_model['model'] = model
    engine_model['model_size'] = opt.load_size

    #if ENABLE_ESRGAN:
    #    engine_model['esrgan'] = esrgan_adapter.init_model(
    #        gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    logger.info(
        'cartoongan_pt init_model done! gpu_id: {}, style: {}'.format(gpu_id, style))
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


def engine_process_image(engine_model, image, func_name):
    opt = engine_model['opt']
    model = engine_model['model']

    input_image = np.asarray(image)
    # RGB -> BGR
    input_image = input_image[:, :, [2, 1, 0]]
    input_image = transforms.ToTensor()(input_image).unsqueeze(0)

    # preprocess, (-1, 1)
    input_image = -1 + 2 * input_image
    if opt.gpu > -1:
        input_image = Variable(input_image).cuda()
    else:
        input_image = Variable(input_image).float()

    # forward
    output_image = model(input_image)
    output_image = output_image[0]

    # BGR -> RGB
    output_image = output_image[[2, 1, 0], :, :]
    # deprocess, (0, 1)
    output_image = output_image.data.cpu().float() * 0.5 + 0.5

    # save
    #file_save = os.path.join('/app/app/debug_' + opt.style + '.jpg')
    #vutils.save_image(output_image, file_save)
    #print('--> image saved to {}'.format(file_save))

    # tensor -> PIL
    grid = vutils.make_grid(output_image, nrow=8, padding=2, pad_value=0,
                            normalize=False, range=None, scale_each=False)
    ndarr = grid.mul(255).clamp(0, 255).byte().permute(1, 2, 0).cpu().numpy()
    image_return = Image.fromarray(ndarr)

    return image_return
