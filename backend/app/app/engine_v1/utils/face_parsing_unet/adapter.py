# encoding=utf-8

import sys
import os
import glob
import cv2
import numpy as np
import torch
from torch.autograd import Variable
from PIL import Image, ImageFilter
# from . import unet
# from . import r18unet
from . import mobileunet

from app.engine_v1 import app_config, logger
from app.engine_v1.utils import image_ndarray_to_pil, image_pil_to_ndarray


def init_model(gpu_id=0):
    # _model= unet.UNet(11)
    # _model = r18unet.ResNetUNet(11)
    _model = mobileunet.MobileUNet(11)

    save_path = os.path.join(app_config.MODEL_DIR, 'face_parsing/model_80.pth')
    state_dict = torch.load(save_path)
    from collections import OrderedDict
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        namekey = k[7:]
        new_state_dict[namekey] = v
    _model.load_state_dict(new_state_dict)

    if gpu_id >= 0:
        with torch.cuda.device(gpu_id):
            _model = _model.cuda()
    _model.eval()

    model = {}
    model['model'] = _model
    model['face_areas'] = ('face', 'l_brow', 'r_brow', 
                          'l_eye', 'r_eye', 'nose', 'u_lip', 
                          'in_mouth', 'l_lip', 'hair')
    _w = app_config.FACE_MIN_SIZE
    model['filterBlur'] = MyGaussianBlur(radius=9, bounds=(0,0,_w,_w))

    logger.info('face_parsing init_model done! gpu_id: {}'.format(gpu_id))
    return model


def getFaceMask(image_pil, engine_model, edit_area=[]):
    model = engine_model['model']
    filterBlur = engine_model['filterBlur']
    face_areas = engine_model['face_areas']

    # 根据所需的人脸部分，动态设置调色板参数：所需部分为 255，其他为 0
    ''' # 调色板取值示例（本函数中只使用黑白色）：
    pallete = [0, 0, 0, #background
        0, 0 ,0,  #face
        0, 0, 0,  #left eyebrow
        0, 0, 0,  #right eyebrow
        0, 0, 0,  #left eye
        0, 0, 0,  #right eye
        0, 0, 0,  #nose
        0, 0, 0,  #upper lip
        0, 0, 0,  #in mouth
        0, 0, 0,  #lower lip
        255, 255, 255]; #hair
    '''
    pallete = [0, 0, 0]
    for i in face_areas:
        if i in edit_area:
            pallete.extend([255, 255, 255])
        else:
            pallete.extend([0, 0, 0])

    # 将四通道图片转化为RGB三通道
    image_pil = image_pil.convert('RGB')
    # image_pil.save('/app/app/dbg_0.jpg')
    size = image_pil.size

    # 将 pil 图片转换为 cv2 格式
    #frame = image_pil_to_ndarray(image_pil)
    frame = cv2.cvtColor(np.asarray(image_pil), cv2.COLOR_RGB2BGR)
    # print(frame.dtype)  uint8
    # print(frame.shape)  256,256,3

    # 缩放为模型支持的大小，然后做人脸解析
    img = cv2.resize(frame, (224, 224)).astype(np.float32)
    img /= 255
    img = img.transpose((2, 0, 1))
    img_tensor = torch.from_numpy(img)
    img_tensor = torch.unsqueeze(img_tensor, 0)
    img_variable = Variable(img_tensor).cuda()
    img_out = model(img_variable)
    # print(img_out.shape)  1 11 224 224

    img_out_norm = torch.squeeze(img_out, 0)
    prob, classmap = torch.max(img_out_norm, 0)

    classmap_np = classmap.data.cpu().numpy()
    # print(type(classmap_np))
    im_pil = Image.fromarray(np.uint8(classmap_np))
    #im_pil.save('/app/app/dbg_1.jpg')
    # print(im_pil.mode)  # mode :L gray
    # print(im_pil.size)  224
    im_pil.putpalette(pallete)  # mode->p 上色
    # print(im_pil.size)  224

    '''
    # 将黑色背景改为透明
    datas = im_pil.getdata()
    newData = list()
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((0, 0, 0, 255))
        else:
            newData.append(item)
    im_pil.putdata(newData)
    '''

    # 再次缩放恢复为原图尺寸
    im_pil = im_pil.resize(size, Image.ANTIALIAS)

    # im_pil = im_pil.convert('RGBA')  #p->rgb (follow pallete bgr)
    im_pil = im_pil.convert('L')  # p->L 返回的为掩模，所以灰度化
    #im_pil.save('/app/app/dbg_2.jpg')

    # 进行高斯模糊，以消除缩放导致的锯齿
    im_pil = im_pil.filter(filterBlur)
    #im_pil.save('/app/app/dbg_3.jpg')

    return im_pil


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)
