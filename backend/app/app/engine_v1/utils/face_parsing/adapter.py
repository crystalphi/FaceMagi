# encoding=utf-8

import sys
import os
import glob
import cv2
import numpy as np
from PIL import Image, ImageFilter
import torch
import torchvision.transforms as transforms

from app.engine_v1 import app_config, logger
from app.engine_v1.utils import image_ndarray_to_pil, image_pil_to_ndarray

from .model import BiSeNet


def init_model(gpu_id=-1):
    # model init
    _model = BiSeNet(n_classes=19)
    if gpu_id >= 0:
        #print('--> gpu_id:', gpu_id)
        with torch.cuda.device(gpu_id):
            _model = _model.cuda()
    model_path = os.path.join(app_config.MODEL_DIR, 'face_makeup_pt/cp/79999_iter.pth')
    _model.load_state_dict(torch.load(model_path))
    _model.eval()
    
    model = {}
    model['model'] = _model
    model['gpu_id'] = gpu_id
    
    to_tensor = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    model['to_tensor'] = to_tensor

    model['face_areas'] = ('face', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 
                           'eye_g', 'l_ear', 'r_ear', 'ear_r', 'nose', 
                           'mouth', 'u_lip', 'l_lip', 'neck', 'neck_l', 
                           'cloth', 'hair', 'hat')
    _w = app_config.FACE_MIN_SIZE
    #model['filterBlur'] = MyGaussianBlur(radius=9, bounds=(0,0,_w,_w))
    model['filterBlur'] = MyGaussianBlur(radius=6)

    logger.info('face_parsing init_model DONE! gpu_id: {}'.format(gpu_id))
    return model


def getFaceMask(image_pil, engine_model, edit_area=[]):
    model = engine_model['model']
    to_tensor = engine_model['to_tensor']
    filterBlur = engine_model['filterBlur']
    face_areas = engine_model['face_areas']

    # 根据所需的人脸部分，动态设置调色板参数
    # 本函数中只使用黑白色：所需部分为 255，其他为 0
    pallete = [0, 0, 0] #background
    for i in face_areas:
        if i in edit_area:
            pallete.extend([255, 255, 255])
        else:
            pallete.extend([0, 0, 0])

    # 将四通道图片转化为RGB三通道
    image_pil = image_pil.convert('RGB')
    # image_pil.save('/app/app/dbg_0.jpg')
    size = image_pil.size

    with torch.no_grad():
        image_pil = image_pil.resize((512, 512), Image.BILINEAR)
        img = to_tensor(image_pil)
        img = torch.unsqueeze(img, 0)
        if engine_model['gpu_id'] >= 0:
            img = img.cuda()
        out = model(img)[0]
        parsing_anno = out.squeeze(0).cpu().numpy().argmax(0)
        #print('--> unique parsing_anno:', np.unique(parsing_anno))
        '''
        vis_parsing_anno = parsing_anno.copy().astype(np.uint8)
        vis_parsing_anno = cv2.resize(vis_parsing_anno, None, fx=stride, fy=stride, interpolation=cv2.INTER_NEAREST)
        vis_parsing_anno_color = np.zeros((vis_parsing_anno.shape[0], vis_parsing_anno.shape[1], 3)) + 255

        num_of_class = np.max(vis_parsing_anno)
        for pi in range(1, num_of_class + 1):
            index = np.where(vis_parsing_anno == pi)
            vis_parsing_anno_color[index[0], index[1], :] = part_colors[pi]
        vis_parsing_anno_color = vis_parsing_anno_color.astype(np.uint8)
        cv2.imwrite('/app/app/dbg_3.png', vis_parsing_anno)
        '''

    #img_out_norm = torch.squeeze(out, 0)
    #prob, classmap = torch.max(img_out_norm, 0)
    #classmap_np = classmap.data.cpu().numpy()
    classmap_np = parsing_anno
    #print('--> type(classmap_np):', type(classmap_np))
    
    im_pil = Image.fromarray(np.uint8(classmap_np))
    #im_pil.save('/app/app/dbg_1.jpg')
    # print(im_pil.mode)  # mode :L gray
    # print(im_pil.size)  224
    im_pil.putpalette(pallete)  # mode->p 上色
    # print(im_pil.size)  224

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
