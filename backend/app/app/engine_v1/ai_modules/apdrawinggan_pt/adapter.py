# -*- coding: utf-8 -*-
# !! 尚未完成，请勿使用！

import os
import sys
from PIL import Image
#from PIL import ImageEnhance

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, \
    image_blend, image_ndarray_to_pil, image_pil_to_ndarray
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .options.test_options import TestOptions
from .data import CreateDataLoader
from .models import create_model
from .util.visualizer import save_images
from .util import html


script_dir = os.path.dirname(os.path.abspath(__file__))

# 是否开启超解析处理
ENABLE_ESRGAN = False  # 若开启，人脸图片会先缩放为标准尺寸进行处理，然后再超解析扩展为原尺寸


def init_model(gpu_id=-1):

    opt = TestOptions().parse()
    opt.num_threads = 1   # test code only supports num_threads = 1
    opt.batch_size = 1  # test code only supports batch_size = 1
    opt.serial_batches = True  # no shuffle
    opt.no_flip = True  # no flip
    opt.display_id = -1  # no visdom display
    opt.gpu_ids = [gpu_id]

    model = create_model(opt)
    model.setup(opt)

    engine_model = {}
    engine_model['opt'] = opt
    engine_model['model'] = model
    engine_model['model_size'] = opt.fineSize # default 512

    logger.info('apdrawinggan_pt init_model done! gpu_id: {}'.format(gpu_id))

    #if ENABLE_ESRGAN:
    #    engine_model['esrgan'] = esrgan_adapter.init_model(
    #                                      gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

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
    opt = engine_model['opt']
    model = engine_model['model']

    data_loader = CreateDataLoader(opt)
    #dataset = data_loader.load_data()
    dataset = data_loader.load_image_data(image) #TODO: 该方法尚未实现，代码难整合
    for i, data in enumerate(dataset):
        if i >= opt.how_many:
            # test code only supports batch_size = 1, how_many means how many test images to run
            break
        model.set_input(data)
        model.test()
        visuals = model.get_current_visuals() #in test the loadSize is set to the same as fineSize
        img_path = model.get_image_paths()
        #save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)

    return image_return
