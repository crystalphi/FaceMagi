#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# deep feat interp 的产品化功能封装

from __future__ import division
from __future__ import with_statement
from __future__ import print_function

import time
import json
import os.path
import argparse
import numpy as np
from PIL import Image

from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend
from app.api_v1.common import get_request_data, set_result_image, resp_result, resp_error

from .zzz import deepmodels
from .zzz import alignface
from .zzz import imageutils
from .zzz import utils


def init_model(gpu_id=-1):

    # configure by command-line arguments
    parser = argparse.ArgumentParser(description='Generate high resolution face transformations.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--backend', type=str, default='torch',
                        choices=['torch', 'caffe+scipy'], help='reconstruction implementation')
    parser.add_argument('--device_id', type=int, default=-1,
                        help='zero-indexed CUDA device')
    parser.add_argument('--K', type=int, default=15, # default 100
                        help='number of nearest neighbors')
    parser.add_argument('--scaling', type=str, default='none',
                        choices=['none', 'beta'], help='type of step scaling')
    parser.add_argument('--iter', type=int, default=50, # default 500
                        help='number of reconstruction iterations')
    parser.add_argument('--postprocess', type=str, default='mask',
                        help='comma-separated list of postprocessing operations')
    parser.add_argument('--delta', type=str, default='2.5', #0.0-5.0
                        help='comma-separated list of interpolation steps')
    parser.add_argument('--output_format', type=str, default='png',
                        choices=['png', 'jpg'], help='output image format')
    parser.add_argument('--comment', type=str, default='',
                        help='the comment is appended to the output filename')
    parser.add_argument('--extradata', action='store_true',
                        default=False, help='extra data is saved')
    parser.add_argument('--output', type=str, default='',
                        help='output is written to this pathname')
    parser.add_argument('--include_original', action='store_true', default=False,
                        help='the first column of the output is the original image')

    config = parser.parse_args()
    if gpu_id >= 0:
        config.device_id = gpu_id
    logger.info('deep_feat_interp config: {}'.format(json.dumps(config.__dict__)))

    # load models
    if config.backend == 'torch':
        from . import deepmodels_torch
        _model = deepmodels_torch.vgg19g_torch(device_id=config.device_id)
    elif config.backend == 'caffe+scipy':
        _model = deepmodels.vgg19g(device_id=config.device_id)
    else:
        raise ValueError('Unknown backend')
    classifier = deepmodels.facemodel_attributes()
    
    face_d, face_p = alignface.load_face_detector(predictor_path=os.path.join(
            app_config.MODEL_DIR, 'shape_predictor_68_face_landmarks.dat'))

    model = {}
    model['config'] = config
    model['model'] = _model
    model['classifier'] = classifier
    model['face_d'] = face_d
    model['face_p'] = face_p

    logger.info('deep_feat_interp init_model done! gpu_id: {}'
                .format(gpu_id))
    return model


def process_image(image, face_data, engine_model, func_name, func_params=None, worker=None):
    """ 对上传图片进行处理
    Returns:
        image_output: 处理后的图片数据
    """

    logger.info('call process_image. func_name: "{}", func_params: "{}", '
                'face_data["attr_dict"]: {}'
                .format(func_name, func_params, face_data["attr_dict"]))

    model = engine_model['model']
    classifier = engine_model['classifier']
    fields = classifier.fields()
    face_d = engine_model['face_d']
    face_p = engine_model['face_p']
    
    effect = func_name
    effect_options_a = ['older', 'younger', 'facehair', 'senior']
    effect_options_b = []
    #effect_options_b = ['Arched_Eyebrows', 'Big_Nose', 'Bushy_Eyebrows', 'Eyeglasses', 'Pale_Skin', 'Pointy_Nose', 'Smiling', 'asian', 'white', 'Wavy_Hair', 'child', 'shiny_skin', 'sunglasses', 'strong_nose_mouth_lines']
    effect_options_b.extend(fields)
    #print('--> effect_options_b:', effect_options_b)
    if effect not in effect_options_a + effect_options_b:
        raise Exception('unsupported effect: {}'.format(effect))
    
    image_output = image

    minimum_resolution = 200
    config = engine_model['config']
    postprocess = set(config.postprocess.split(','))
    # Set the free parameters
    K = config.K
    config.delta = str(func_params[0]) # 使用前端传入的参数
    delta_params = [float(x.strip()) for x in config.delta.split(',')]
    multi_num = 4 # 样本乘积倍数 default: 4

    t0 = time.time()
    
    xX = image
    print("processing test image {}...".format(xX))
    template, original = alignface.detect_landmarks(None, face_d, face_p, image=xX)
    image_dims = original.shape[:2]
    if min(image_dims) < minimum_resolution:
        s = float(minimum_resolution)/min(image_dims)
        image_dims = (int(round(image_dims[0]*s)), int(round(image_dims[1]*s)))
        original = imageutils.resize(original, image_dims)
    t1 = time.time()
    print('--> {} seconds to detect landmark'.format(int(t1-t0)))
    
    XF = model.mean_F([original])
    XA = classifier.score([xX])[0]
    print(xX, ', '.join(k for i, k in enumerate(fields) if XA[i] >= 0))
    t2 = time.time()
    print('--> {} seconds to get image score'.format(int(t2-t1)))

    # select positive and negative sets based on gender and mouth
    print("select positive and negative sets based on gender and mouth")
    # effect options:
    # '5_o_Clock_Shadow', 'Arched_Eyebrows', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips', 'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Bushy_Eyebrows', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'No_Beard', 'Pale_Skin', 'Pointy_Nose', 'Receding_Hairline', 'Sideburns','Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Lipstick', 'Young', 'asian', 'baby', 'black', 'brown_eyes', 'child', 'eyes_open', 'frowning', 'fully_visible_forehead', 'indian', 'middle_aged', 'mouth_closed', 'mouth_wide_open', 'no_eyewear', 'obstructed_forehead', 'partially_visible_forehead', 'senior', 'shiny_skin', 'strong_nose_mouth_lines', 'sunglasses', 'teeth_not_visible', 'white'
    _idx = fields.index
    _attr_dict = face_data['attr_dict']
    lambda_filter = lambda xa, idx, _true: xa[idx] >= 0 if _true else xa[idx] < 0
    # eg: lambda_filter(XA, _idx('Male'), _attr_dict['Male']))
    select_done = False
    # 先按标准特征过滤
    for option in effect_options_b:
        if effect == option:
            cP = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx(option), False)] # 负样本
            for x in ('Bald', 'Bangs'): # 为提升图片质量，补充刘海过滤
                if effect != x:
                    cP.append((_idx(x), _attr_dict[x]))
            cQ = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx(option), True)] # 正样本
            for x in ('Bald', 'Bangs'): # 为提升图片质量，补充刘海过滤
                if effect != x:
                    cQ.append((_idx(x), _attr_dict[x]))
            select_done = True
            break
    # 再按自定义特征过滤
    if not select_done:
        if effect == 'older':
            cP = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('Young'), True)]
            cQ = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('Young'), False)]
        elif effect == 'younger':
            cP = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('Young'), False)]
            cQ = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('Young'), True)]
        elif effect == 'facehair':
            cP = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('No_Beard'), True), (_idx('Mustache'), False)]
            cQ = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('No_Beard'), False), (_idx('Mustache'), True)]
        elif effect == 'senior':
            cP = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('senior'), False)]
            cQ = [(_idx('Male'), lambda_filter(XA, _idx('Male'), _attr_dict['Male'])),
                  (_idx('senior'), True)]
        else:
            raise ValueError('Unknown effect: {}'.format(effect))
    
    P = classifier.select(cP, XA)
    Q = classifier.select(cQ, XA)
    if len(P) < K*multi_num or len(Q) < K*multi_num:
        msg = '{}: Not enough images in database (|P|={}, |Q|={}).'.format(xX, len(P), len(Q))
        logger.warn(msg)
        raise Exception(msg)
    
    t3 = time.time()
    print('--> {} seconds to select images set'.format(int(t3-t2)))

    print("fit the best {} database images to input image".format(K*multi_num))
    Plm = classifier.lookup_landmarks(P[:K*multi_num])
    Qlm = classifier.lookup_landmarks(Q[:K*multi_num])
    idxP, lossP, MP = fit_submanifold_landmarks_to_image(
        template, original, Plm, face_d, face_p) # 耗时 5s
    idxQ, lossQ, MQ = fit_submanifold_landmarks_to_image(
        template, original, Qlm, face_d, face_p) # 耗时 5s
    t4 = time.time()
    print('--> {} seconds to fit {} images'.format(int(t4-t3), K*multi_num))

    print("use the {} best fitted images".format(K))
    xP = [P[i] for i in idxP[:K]]
    xQ = [Q[i] for i in idxQ[:K]]
    PF = model.mean_F(utils.warped_image_feed(
        xP, MP[idxP[:K]], image_dims)) # 耗时 3s
    QF = model.mean_F(utils.warped_image_feed(
        xQ, MQ[idxQ[:K]], image_dims)) # 耗时 3s
    if config.scaling == 'beta':
        WF = (QF-PF)/((QF-PF)**2).mean()
    elif config.scaling == 'none':
        WF = (QF-PF)
    t5 = time.time()
    print('--> {} seconds to mean_F {} best images'.format(int(t5-t4), K))

    print("for each interpolation step ...")
    max_iter = config.iter
    init = original
    result = []
    for delta in delta_params:
        print(xX, image_dims, delta, len(xP), len(xQ))
        t7 = time.time()
        Y = model.F_inverse(
            XF+WF*delta, max_iter=max_iter, initial_image=init) # 耗时 15s
        t8 = time.time()
        print('--> {} seconds to reconstruct at delta {}'.format(int(t8-t7), delta))
        result.append(Y)
        max_iter = config.iter//2
        init = Y
    result = np.asarray([result])
    original = np.asarray([original])
    X_mask = '-mask.png' #FIXME: 使用真实的 mask 地址，如果有的话
    if 'mask' in postprocess and os.path.exists(X_mask):
        mask = imageutils.resize(imageutils.read(X_mask), image_dims)
        result *= mask
        result += original*(1-mask)
    if 'color' in postprocess:
        result = utils.color_match(np.asarray([original]), result)
    if 'mask' in postprocess and os.path.exists(X_mask):
        result *= mask
        result += original*(1-mask)
    if config.include_original:
        m = imageutils.montage(np.concatenate(
            [np.expand_dims(original, 1), result], axis=1))
    else:
        m = imageutils.montage(result)
    
    image_output = Image.fromarray((m * 255).astype(np.uint8))

    t10 = time.time()
    print('{} seconds ({} seconds per image).'.format(
        int(t10-t0), int(t10-t0)/len(delta_params)))

    return image_output


def fit_submanifold_landmarks_to_image(template, original, Xlm, face_d, face_p, landmarks=list(range(68))):
    '''
    Fit the submanifold to the template and take the top-K.
    Xlm is a N x 68 x 2 list of landmarks.
    FIXME: 该操作耗时~5s，能否优化？减少 K 值能等比降低耗时。
    '''
    lossX = np.empty((len(Xlm),), dtype=np.float64)
    MX = np.empty((len(Xlm), 2, 3), dtype=np.float64)
    nfail = 0
    for i in range(len(Xlm)):
        lm = Xlm[i]
        try:
            M, loss = alignface.fit_face_landmarks(
                lm, template, landmarks=landmarks, image_dims=original.shape[:2])
            lossX[i] = loss
            MX[i] = M
        except alignface.FitError:
            lossX[i] = float('inf')
            MX[i] = 0
            nfail += 1
    if nfail > 1:
        print('fit submanifold, {} errors.'.format(nfail))
    a = np.argsort(lossX)
    return a, lossX, MX

'''
if __name__ == '__main__':

    import cv2
    from imageio import imread, imsave

    script_dir = os.path.dirname(os.path.abspath(__file__))

    img_input_filename = os.path.join(
        script_dir, '../../../static/attgan_pt/vvdd-11.jpg')
    img_input = cv2.imread(img_input_filename)
    img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)

    model = init_model()

    result = engine_process_image(model, img_input, None)

    imsave('result.jpg', result)
'''
