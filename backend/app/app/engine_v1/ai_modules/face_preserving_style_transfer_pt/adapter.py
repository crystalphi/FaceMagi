# -*- coding: utf-8 -*-

import os
import sys
import pathlib
import argparse
import torch
from torchvision import transforms
from PIL import Image
#from PIL import ImageEnhance

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray, image_tensor_to_pil
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .src.image_transform_net import ImageTransformNet
from .src import utils


script_dir = os.path.dirname(os.path.abspath(__file__))

# 是否开启超解析处理
ENABLE_ESRGAN = False  # 若开启，人脸图片会先缩放为标准尺寸进行处理，然后再超解析扩展为原尺寸


def init_model(gpu_id=-1, style='manga-face'):

    # Should computation be done on the GPU if available?
    use_cuda = gpu_id >= 0 and torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    # Load the style transfer model
    model_path = os.path.join(app_config.MODEL_DIR, 
            'face_preserving_style_transfer_pt/models/{}.pth'.format(style))
    with torch.no_grad():
        img_transform = utils.load_model(model_path, ImageTransformNet()).to(device)
    logger.info("Loading the style transfer model ({}) ... Done.".format(style))
    
    engine_model = {}
    engine_model['device'] = device
    engine_model['img_transform'] = img_transform
    engine_model['model_size'] = 500 # 该模型对输入尺寸没要求，故此指定为标准大小

    #if ENABLE_ESRGAN:
    #    engine_model['esrgan'] = esrgan_adapter.init_model(
    #                                      gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    logger.info('face_preserving_style_transfer_pt init_model done! gpu_id: {}'.format(gpu_id))

    return engine_model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
    Returns:
        image_output: 处理后的图片数据
    """

    # ！！与其他引擎处理方式稍有不同：这里直接使用 pil 原图而不是 face_data 中的人脸图做处理

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

    return _img_out_pil


def engine_process_image(engine_model, image, func_name):
    device = engine_model['device']
    img_transform = engine_model['img_transform']

    content_image = load_pil_image_tensor(image, 1).to(device)
    
    with torch.no_grad():
        stylized_img = img_transform(content_image).cpu()
        image_return = save_image_tensor(stylized_img)

    return image_return


def load_pil_image_tensor(image_pil, batch_size):
    """Load an pil image for torch."""
    image_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x * 255)])
    # Repeat the image so it matches the batch size for loss computations
    return image_transform(image_pil)[:3].repeat(batch_size, 1, 1, 1)


def save_image_tensor(image_tensor):
    """Save a tensor of an image."""
    image_array = image_tensor.clone().squeeze(0).numpy().clip(0, 255)
    image_pil = Image.fromarray(image_array.transpose(1, 2, 0).astype("uint8"))
    return image_pil
