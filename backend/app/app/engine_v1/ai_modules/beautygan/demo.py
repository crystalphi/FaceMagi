# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import io
import os
import sys
import glob
import cv2
import argparse
from imageio import imread, imsave
from PIL import Image
from flask import current_app, Blueprint, jsonify, request

api = Blueprint('beautygan_api', __name__)
script_dir = os.path.dirname(os.path.abspath(__file__))


def init_model(gpu_id=-1, img_size=256):

    tf.reset_default_graph()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph(
        os.path.join(script_dir, 'model', 'model.meta'))
    saver.restore(sess, tf.train.latest_checkpoint(
        os.path.join(script_dir, 'model')))

    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name('X:0')
    Y = graph.get_tensor_by_name('Y:0')
    Xs = graph.get_tensor_by_name('generator/xs:0')

    model = {}
    model['sess'] = sess
    model['X'] = X
    model['Y'] = Y
    model['Xs'] = Xs

    model['img_size'] = img_size
    print('set img_size: {0}'.format(img_size))

    makeup_files = glob.glob(os.path.join(script_dir, 'imgs', 'makeup', '*.*'))
    print('--> makeup_files: {0}'.format(makeup_files))
    model['makeups'] = {makeup_files[i].split('/')[-1].split('.')[0]: cv2.resize(
        imread(makeup_files[i]), (img_size, img_size)) for i in range(len(makeup_files))}
    print('loaded makeups: {0}'.format(model['makeups'].keys()))

    return model


def beautygan_process(model, face_image, makeup_name):
    img_size = model['img_size']

    no_makeup = cv2.resize(face_image, (img_size, img_size))
    X_img = np.expand_dims(preprocess(no_makeup), 0)

    makeup = model['makeups'][makeup_name]
    Y_img = np.expand_dims(preprocess(makeup), 0)
    Xs_ = model['sess'].run(model['Xs'], feed_dict={
                            model['X']: X_img, model['Y']: Y_img})
    Xs_ = deprocess(Xs_)
    #image_return = Image.fromarray(Xs_[0], mode="RGB") # FIXME: 这里返回的图片是乱码
    image_return = Image.fromarray(makeup / 255., mode="RGB")
    print('--> type(image_return): {0}'.format(type(image_return)))
    
    # 如果为调试模式，则保存生成的人脸图片做分析用，产品化部署不需要
    if True:
        out_file = os.path.join(script_dir, 'new_face.jpg')
        image_return.save(out_file)
        print('new image saved to {:s} done!'.format(out_file))

    return image_return


def preprocess(img):
    return (img / 255. - 0.5) * 2


def deprocess(img):
    return (img + 1) / 2


if __name__ == '__main__':

    img_size = 256

    img_input_filename = os.path.join('imgs', 'no_makeup', 'vvdd-11.jpg')
    img_input = cv2.imread(img_input_filename)
    img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2RGB)
    no_makeup = cv2.resize(img_input, (img_size, img_size))

    makeups = glob.glob(os.path.join('imgs', 'makeup', '*.*'))

    result = np.ones((2 * img_size, (len(makeups) + 1) * img_size, 3))
    result[img_size: 2 * img_size, :img_size] = no_makeup / 255.

    model = init_model()

    X_img = np.expand_dims(preprocess(no_makeup), 0)
    for i in range(len(makeups)):
        makeup = cv2.resize(imread(makeups[i]), (img_size, img_size))
        Y_img = np.expand_dims(preprocess(makeup), 0)
        Xs_ = model['sess'].run(model['Xs'], feed_dict={
                                model['X']: X_img, model['Y']: Y_img})
        Xs_ = deprocess(Xs_)
        result[:img_size, (i + 1) * img_size: (i + 2)
               * img_size] = makeup / 255.
        result[img_size: 2 * img_size,
               (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]
        
        if True:
            #img = makeup / 255.
            img = Xs_[0]
            #img = result
            img = tf.image.encode_jpeg(img * 255).eval(session=model['sess'])
            #image_return = Image.fromarray(img * 255, mode="RGB")
            image_return = Image.open(io.BytesIO(img))
            out_file = os.path.join(script_dir, 'new_face.jpg')
            image_return.save(out_file)
            print('new image saved to {:s} done!'.format(out_file))
        break

    imsave('result.jpg', result)

