# -*- coding: utf-8 -*-
__author__ = "vedasky"
__copyright__ = "Copyright 2019"

import os
import argparse
import json
import cv2
import numpy as np
from skimage import transform, util
from os.path import join
from PIL import Image, ImageFilter
import torch
import torchvision.transforms as transforms

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend, exec_esrgan
from app.engine_v1.utils import image_convert_rgb, image_resize_default, image_blend, \
    image_ndarray_to_pil, image_pil_to_ndarray, image_cv2_to_pil, image_pil_to_cv2, \
    cv2_sharpen_gaus
#from app.engine_v1.utils.esrgan import adapter as esrgan_adapter

from .. import check_if_save_demo_icon
from .model import BiSeNet


script_dir = os.path.dirname(os.path.abspath(__file__))
SAVE_ICON_DIR = os.path.join(app_config.STATIC_FOLDER, 'ui_data/modules/fcmkp')

# 是否开启超解析处理
ENABLE_ESRGAN = False  # 若开启，人脸图片会先缩放为标准尺寸进行处理，然后再超解析扩展为原尺寸
ENABLE_MASK = False # 若开启，会应用边缘模糊的人脸掩模图做进一步处理


def init_model(gpu_id=-1):
    # model init
    net = BiSeNet(n_classes=19)
    if gpu_id >= 0:
        #print('--> gpu_id:', gpu_id)
        with torch.cuda.device(gpu_id):
            net = net.cuda()
    ckp = os.path.join(app_config.MODEL_DIR, 'face_makeup_pt/cp/79999_iter.pth')
    net.load_state_dict(torch.load(ckp))
    net.eval()

    to_tensor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])

    model = {}
    model['net'] = net
    model['to_tensor'] = to_tensor
    model['model_size'] = 512 # 默认为 512，其他大小是否可处理未知
    model['gpu_id'] = gpu_id
    #model['filterBlur'] = MyGaussianBlur(radius=9, bounds=(0,0,_w,_w))
    model['filterBlur'] = MyGaussianBlur(radius=4)

    #if ENABLE_ESRGAN:
    #    model['esrgan'] = esrgan_adapter.init_model(
    #                              gpu_id=app_config.ENGINE_GPU_ID['esrgan'])

    logger.info('face_makeup_pt init_model done! gpu_id: {}'.format(gpu_id))
    return model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
    Returns:
        image_output: 处理后的图片数据
    """

    if 'img_hash' not in face_data: # 本引擎只能处理人脸图片
        return None

    # ！！直接使用 pil 原图而不是 face_data 中的人脸图做处理
    
    # 如果 image 尺寸不等于模型标准尺寸，则缩放为标准尺寸再处理
    _img_w, _img_h = image.size[0:2]
    _h = engine_model['model_size']
    if _img_h > _h:
        _img_pil = image_resize_default(image, _h)
    else:
        _img_pil = image
    _img_cv2 = image_pil_to_cv2(_img_pil)

    # 开始处理人脸上妆

    # 根据输入参数获取要修改的人脸区域及处理方式
    func_name, func_arg = func_name, func_params[0]
    edit_area = []
    for i in func_params[1]:
        if i == 'skin': # 肤色
            edit_area.extend(['face', 'l_ear', 'r_ear', 'nose', 'l_brow', 'r_brow',
                    'u_lip', 'l_lip', 'neck'])
        elif i == 'lips': # 嘴唇
            edit_area.extend(['u_lip', 'l_lip'])
        else:
            edit_area.append(i)
    logger.info('func_name: {}, func_arg: {}, func_params: {}, edit_area: {}'
                .format(func_name, func_arg, func_params, edit_area))
    
    # 人脸解析器 - 内置 face-parsing.PyTorch：总共 18 个人脸部分（当前使用）
    # 正脸效果较好，侧脸或者小脸不佳
    # 1 'face', 2 'l_brow', 3 'r_brow', 4 'l_eye', 5 'r_eye', 
    # 6 'eye_g', 7 'l_ear', 8 'r_ear', 9 'ear_r', 10 'nose', 
    # 11 'mouth', 12 'u_lip', 13 'l_lip', 14 'neck', 15 'neck_l', 
    # 16 'cloth', 17 'hair', 18 'hat'
    face_area_map = { # 取值从数字 1 开始依次增加；0 为背景部分
        'face': 1,
        'l_brow': 2,
        'r_brow': 3,
        'l_eye': 4,
        'r_eye': 5,
        'eye_g': 6,
        'l_ear': 7,
        'r_ear': 8,
        'ear_r': 9,
        'nose': 10,
        'teeth': 11,
        'u_lip': 12,
        'l_lip': 13,
        'neck': 14,
        'neck_l': 15,
        'cloth': 16,
        'hair': 17,
        'hat': 18
    }
    # 首先得到人脸解析图
    face_areas = list(face_area_map.keys())
    parsing, mask_pil = evaluate(_img_pil, engine_model, face_areas, edit_area)
    parsing = cv2.resize(
        parsing, _img_cv2.shape[0:2], interpolation=cv2.INTER_NEAREST)
    if ENABLE_MASK and mask_pil:
        mask_pil = image_resize_default(mask_pil, _img_cv2.shape[0])
    
    _img_out = _img_cv2
    
    if func_name == 'chg_color': # 着色处理

        parts = [] # 需处理的人脸部分列表
        colors = [] # 各人脸部分相应颜色列表
        # colors 取值数量应与 parts 一致。
        
        # 设定着色参数
        def __set_color(part, color):
            if type(part) is list:
                for i in part:
                    parts.append(face_area_map[i])
                    colors.append(color)
            else:
                parts.append(face_area_map[part])
                colors.append(color)
        
        # 颜色示例 b,g,r：
        # [230, 50, 20] # 蓝
        # [10, 250, 10] # 绿
        # [10, 50, 250] # 红
        # [20, 70, 180] # 唇红
        #print('--> func_params:', func_params)
        for p in edit_area:
          __set_color(p, func_params[2])
        if func_arg in ('avatar', 'hawk', 'red'): # 肤色系列 1
            __set_color(['u_lip', 'l_lip'], [20, 70, 180])
            c1, c2 = 0, 1 # 只修改蓝夜色
        elif func_arg in ('jade', 'golden'): # 肤色系列 2
            __set_color(['u_lip', 'l_lip'], [20, 70, 180])
            c1, c2 = 0, 2 # 修改蓝绿夜色
        else: # 部分着色，如发色
            c1, c2 = 0, 1 # 默认只修改蓝夜色
        
        # 置换指定区域颜色
        for part, color in zip(parts, colors):
            print('--> change color to {} for {}'.format(color, part))
            _img_out = change_color(_img_out, parsing, part, color, c1, c2)

    # 转换输出图从 cv2 到 PIL.Image
    _img_out_pil = image_cv2_to_pil(_img_out)

    if ENABLE_MASK:
        # 使用边缘模糊后的掩模图进行修正
        _img_out_pil.paste(_img_out_pil, (0, 0), mask_pil)

    # 将返回图片缩放为原尺寸
    if _img_h > _h:
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
            check_if_save_demo_icon(_img_out_pil, SAVE_ICON_DIR, func_arg)

    return _img_out_pil


def evaluate(image_pil, engine_model, face_areas, edit_area):

    net = engine_model['net']
    to_tensor = engine_model['to_tensor']
    model_size = engine_model['model_size']
    filterBlur = engine_model['filterBlur']

    with torch.no_grad():
        image = image_pil.resize((model_size, model_size), Image.BILINEAR)
        img = to_tensor(image)
        img = torch.unsqueeze(img, 0)
        if engine_model['gpu_id'] >= 0:
            img = img.cuda()
        out = net(img)[0]
        parsing = out.squeeze(0).cpu().numpy().argmax(0)
        #print('--> parsing:', parsing)
        print('--> unique parsing:', np.unique(parsing))

        # from .test import vis_parsing_maps
        # if not os.path.exists(respth):
        #     os.makedirs(respth)
        # vis_parsing_maps(image, parsing, stride=1, save_im=False, save_path=osp.join(respth, dspth))

        # 对人脸解析掩模进行高斯模糊，以平滑边缘使图像处理结果更自然
        im_pil = None
        if ENABLE_MASK:
            im_pil = Image.fromarray(np.uint8(parsing))
            #im_pil.save('/app/app/xxx.jpg')
            # 设置调色板参数只使用黑白色：所需部分为 255，其他为 0
            pallete = [0, 0, 0] # 背景色
            for i in face_areas:
                if i in edit_area:
                    pallete.extend([255, 255, 255])
                else:
                    pallete.extend([0, 0, 0])
            im_pil.putpalette(pallete)  # mode->p 上色
            im_pil = im_pil.convert('L')  # p->L 返回的为掩模，所以灰度化
            im_pil = im_pil.filter(filterBlur) # 进行高斯模糊
            #im_pil.save('/app/app/yyy.jpg')
            #parsing = image_pil_to_cv2(im_pil)

        return parsing, im_pil


def change_color(image, parsing, part=17, color=[230, 50, 20], c1=0, c2=1):
    """ 采用夜色替换法实现变更指定颜色
        由于人脸主色调一般偏红，所以尽量只修改b或者b和g，这样效果好过渡自然。
    """

    b, g, r = color

    # 首先生成原图大小的指定单色图
    tar_color = np.zeros_like(image)
    tar_color[:, :, 0] = b
    tar_color[:, :, 1] = g
    tar_color[:, :, 2] = r

    # 把图像从RGB转到HSV夜色空间
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    tar_hsv = cv2.cvtColor(tar_color, cv2.COLOR_BGR2HSV)

    if part == 12 or part == 13: # 唇色替换：其主色调为红色，为突出调色效果只修改蓝绿色
        image_hsv[:, :, 0:2] = tar_hsv[:, :, 0:2]
    elif part == 17: # 发色替换：一般只需替换蓝色通道
        image_hsv[:, :, 0] = tar_hsv[:, :, 0]
        #for i in range(3):
        #    b = image_hsv[:, :, i]
        #    b[b<24] = tar_hsv[:, :, 0][b<24] # 直接替换通道色中的暗色部分
        #    break # 只需替换第一个通道
    else: # 其他部位如肤色颜色替换
        # 换色方法1：替换指定颜色通道（较好）
        image_hsv[:, :, c1:c2] = tar_hsv[:, :, c1:c2] # 根据输入参数替换夜色
        #image_hsv[:, :, c1:c2] = image_hsv[:, :, c1:c2] * 0.3 + tar_hsv[:, :, c1:c2] * 0.7
    
        # 换色方法2：全色替换亮色法（不佳）
        #for i in range(3):
        #    b = image_hsv[:, :, i]
        #    #b[b>196] = tar_hsv[:, :, 0][b>196] # 直接替换通道色中的亮色部分
        #    b[b>196] = b[b>196] * 0.1 + tar_hsv[:, :, 0][b>196] * 0.9 # alpha 替换通道色中的亮色部分
        
        # 换色方法3：全色阿尔法混合（不佳）
        #alpha = 0.5
        #image_hsv[:, :, 0:3] = image_hsv[:, :, 0:3] * alpha + tar_hsv[:, :, 0:3] * (1 - alpha)

    changed = cv2.cvtColor(image_hsv, cv2.COLOR_HSV2BGR)

    #if part == 17: # 头发锐化
    #    changed = cv2_sharpen_gaus(changed)

    # 非编辑部分保留原样
    changed[parsing != part] = image[parsing != part]

    return changed


class MyGaussianBlur(ImageFilter.Filter):
    """PIL高斯模糊过滤器
    示例：MyGaussianBlur(radius=9, bounds=(0,0,_w,_w)) # 除了边缘9/2？像素外，其它做模糊
    """
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
