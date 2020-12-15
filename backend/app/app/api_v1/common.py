# -*- coding: utf-8 -*-
# 定义 api 所需的通用函数

import os
import sys
import io
import re
import json
import PIL
import base64
import traceback
#import numpy as np
from os.path import join
from PIL import Image, ImageDraw, ImageFont
from flask import current_app, Blueprint, jsonify, request

from app.util import save_task_obj_data


def allowed_file(filename):
    # app端上传图片文件名称示例: file-1569144378390
    if not '.' in filename:
        return True # 由于app端上传图片文件无后缀，无法判断合法性，故直接允许
    else:
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['UPLOAD_ALLOWED_EXTS']


def get_request_data(request):
    """从 POST 表单数据中获取客户端上传图片及处理参数"""

    params = None
    image = None
    msg = None
    is_new_image = False # 是否为新提交图片

    #print('--> request:', request)
    #print('--> request.form:', request.form)
    #print('--> request.files:', request.files)
    if 'params' in request.form:
        params_str = request.form['params']
        try:
            params = json.loads(params_str)
            if type(params) is not dict:
                msg = 'loaded params must be a dict, now it is %s' % params
                params = None
        except Exception as e:
            #current_app.logger.exception(e)
            current_app.logger.info("json load error, params_str: {0}".format(params_str))
            msg = 'Input params must be valid json string. {0}'.format(e)
            current_app.logger.info(msg)
            params = None
    else:
        msg = 'No params found.'

    # 如有上传 m_id 则直接使用，否则保存上传图片并计算获取 m_id
    m_id = request.args.get("m_id")
    demo_idx = request.args.get("demo_idx")
    if m_id != None:
        current_app.logger.info('got m_id from request args: {}'.format(m_id))
    if demo_idx != None:
        is_new_image = True
        current_app.logger.info('got demo_idx from request args: {}'.format(demo_idx))
        demo_path = os.path.join(current_app.config['STATIC_FOLDER'],
                                'ui_data/face_demo/' + str(int(demo_idx) + 1) + '.jpg')
        image = Image.open(demo_path)
        m_id = save_task_obj_data(image, 
                                current_app.config['SAVE_FILE_NAME']['image_base'],
                                None, current_app.config, current_app.logger)
    elif 'image' in request.files: # 上传图片为文件形式
        is_new_image = True
        image_file = request.files['image']
        #print('--> image_file.filename:', image_file.filename)
        if not image_file or image_file.filename == '':
            msg = 'No selected image file'
        elif allowed_file(image_file.filename):
            try:
                image_bytes = io.BytesIO(request.files["image"].read())
                image = Image.open(image_bytes)
                request.files["image"].close()
                m_id = save_task_obj_data(image, 
                                        current_app.config['SAVE_FILE_NAME']['image_base'],
                                        None, current_app.config, current_app.logger)
            except Exception as e:
                current_app.logger.error('save image_base from file error: {}'.format(e))
                current_app.logger.info(traceback.format_exc(limit=5))
        else:
            msg = 'invalid image file'
    elif 'm_b64' in request.form: # 上传图片为 base64 字符串形式
        is_new_image = True
        try:
            result = re.search("data:image/(?P<ext>.*?);base64,(?P<data>.*)", 
                                request.form['m_b64'], re.DOTALL)
            if result:
                ext = result.groupdict().get("ext")
                if ext != 'png':
                    raise Exception("only png image supported!")
                img_data = result.groupdict().get("data")
            else:
                raise Exception("can not parse m_b64 string!")
            image_data = base64.urlsafe_b64decode(img_data)
            image_bytes = io.BytesIO(image_data)
            image = Image.open(image_bytes)
            m_id = save_task_obj_data(image, 
                                    current_app.config['SAVE_FILE_NAME']['image_base'],
                                    None, current_app.config, current_app.logger)
        except Exception as e:
            current_app.logger.error('save image_base from m_b64 error: {}'.format(e))
            current_app.logger.info(traceback.format_exc(limit=5))
    else:
        msg = 'No m_id or image data/file found'

    return m_id, params, msg, is_new_image


def set_result_image(data, image_output):
    """在结果中返回生成的图片尺寸及内容"""

    data["image_size"] = image_output.size
    data["image_data"] = image_to_base64(image_output)
    
    if current_app.config['DEBUG']: #仅在调试模式开启，便于查看处理结果
        file_name = join(current_app.config['UPLOAD_FOLDER'], "../../../image_output.jpg")
        image_output.save(file_name, quality=95)
        current_app.logger.debug('debug result image saved to local file: %s' % file_name)

    return data


def resp_result(data):
        """封装返回给客户端的正常信息"""

        result = {
            "errno": 0,
            "errmsg": "",
            "data": data
        }
        return jsonify(result)


def resp_error(errmsg):
        """封装返回给客户端的错误信息"""
        
        result = {
            "errno": 1,
            "errmsg": errmsg,
            "data": {}
        }
        return jsonify(result)


def read_local_image(sub_path, folder_type=None):
    """从本地文件系统读取指定路径的图片文件（主要用于直接返回 base64 格式图片，暂未使用）
      folder_type: 参考项目 config.py 中的定义，一般为：UPLOAD_FOLDER 或 STATIC_FOLDER
    """

    if folder_type:
        full_path = os.path.join(current_app.config[folder_type], sub_path)
    else:
        full_path = sub_path
    #print("--> current_app.config:[%s]: %s" % (folder_type, current_app.config[folder_type]))
    
    image = Image.open(full_path)
    
    return image


def image_to_base64(image):
    
    image_bytes = io.BytesIO()
    image = image.convert('RGB')
    image.save(image_bytes, format='JPEG') # 或 PNG，图片格式
    image_bytes = image_bytes.getvalue()   # 这个就是保存的图片字节流
    # 字节流转 Base64 字符串
    image_data = 'data:image/jpg;base64,' + base64.b64encode(image_bytes).decode('utf-8')
    
    return image_data


def image_add_watermark(img_pil, text=' FaceMagi'):
    """图片加水印"""
    
    img_rgba = img_pil.convert("RGBA")

    text_img = Image.new("RGBA", img_rgba.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_img)

    font = ImageFont.truetype('DejaVuSans.ttf', 32)  # 字体及字体大小
    #font = ImageFont.load_default()
    
    # 位置、文本、字体、颜色及透明度
    _w, _h = img_rgba.size
    text_position = (60, _h - 36)
    draw.text(text_position, text, font=font, fill=(256, 256, 224, 130))
    print("image_add_watermark() text info: {}".format(draw.textsize(text, font=font)))

    # 合成水印图片
    img_with_watermark = Image.alpha_composite(img_rgba, text_img)
    
    #img_with_watermark = img_with_watermark.convert("RGB")
    return img_with_watermark
