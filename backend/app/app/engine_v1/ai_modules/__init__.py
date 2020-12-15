# -*- coding: utf-8 -*-
__author__ = "vedasky"
__copyright__ = "Copyright 2019"

import os
import time
from app.engine_v1 import app_config, logger
from app.engine_v1.utils import image_resize_default


def check_if_save_demo_icon(img_pil, icon_dir, icon_name):
    """将 icon demo 图片的人脸处理结果保存为图标"""
    
    if app_config.DEMO_ICON_ENABLE:
        os.makedirs(icon_dir, exist_ok=True)
        icon_file = os.path.join(icon_dir, '{}.jpg'.format(icon_name))
        
        image_out = img_pil.copy()

        # 对于非人脸检测图，由于会扩展为正方形，处理后图片需要居中截取，否则会有边框，做图标不好看
        img_w, img_h = img_pil.size
        #print('--> img_w: %s, img_h: %s' % (img_w, img_h))
        if img_w >= 380:
            _sz = 380
            x0 = int((img_w - _sz) / 2)
            y0 = int((img_h - _sz) / 2)
            x1 = x0 + _sz
            y1 = y0 + _sz
            image_out = image_out.crop((x0, y0, x1, y1))
        
        icon_img_pil = image_resize_default(image_out, 200) # 缩放为前端所需图标大小
        icon_img_pil.save(icon_file)
        logger.info('icon demo image saved to icon {:s} done!'.format(icon_file))
