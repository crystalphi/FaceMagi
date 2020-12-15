import os
import numpy as np
import caffe
import cv2
import argparse
from os.path import join


script_dir = os.path.dirname(os.path.abspath(__file__))


def init_model(gpu_id=-1):
    model_path = join(script_dir, './outputs/single_path_resnet_celeba.caffemodel')
    prototxt_path = join(script_dir, './outputs/deploy_single.prototxt')
    mean_file = join(script_dir, './data/pretrained/ResNet_mean.binaryproto')
    
    if not os.path.isfile(model_path):
        raise IOError('%s model not found.\n' % model_path)
    
    if int(gpu_id) >= 0:
        caffe.set_mode_gpu()
        caffe.set_device(int(gpu_id))
    else:
        caffe.set_mode_cpu()
    
    net = caffe.Net(prototxt_path, model_path, caffe.TEST)
    proto_data = open(mean_file, "rb").read()
    a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
    mean = caffe.io.blobproto_to_array(a)[0]
    print('Loaded network {:s}'.format(model_path))

    model = {}
    model['net'] = net
    model['mean'] = mean

    return model

def __pre_process(color_img, mean, is_mirror=False):
    target_height = 224
    target_width = 224
    resized_img = cv2.resize(color_img, (target_width, target_height))
    if is_mirror:
        flip_img = cv2.flip(resized_img, 1)
        return np.transpose(flip_img, (2, 0, 1)) - mean
    else:
        return np.transpose(resized_img, (2, 0, 1)) - mean


def get_face_attrs(model, img, feature_layer='pred', attr_num=40):
    net = model['net']
    mean = model['mean']

    attr = np.zeros(attr_num, np.uint8)
    resized_img = __pre_process(img, mean)
    resized_img_2 = __pre_process(img, mean, True)
    net.blobs['data'].reshape(2, *resized_img.shape)
    net.blobs['data'].data[0] = resized_img
    net.blobs['data'].data[1] = resized_img_2
    out = net.forward()
    score = np.mean(out[feature_layer], axis=0)
    for j in range(0, attr_num):
        if score[j] >= 0.5:
            attr[j] = 1
        else:
            attr[j] = 0
    
    return attr


def main():
    gpu_id = -1 # or 0, 1 ...
    attr_num = 40
    test_file = "./data/demo/list/demo.list"
    pred_file = "./result/demo_result.list"
    root_folder = "./data"

    # ---loading model-----
    model = init_model(gpu_id)
    f = open(test_file, 'r')
    lines = f.readlines()
    out_f = open(pred_file, 'w')
    for idx, line in enumerate(lines):
        infos = line.strip().split()
        if idx % 100 == 0:
            print(idx)
        img_path = os.path.join(root_folder, infos[0])
        img = cv2.imread(img_path)
        if img is None:
            print('%s is None' % img_path)
            attr = None
        else:
            attr = get_face_attrs(model, img)
        out_line = img_path + ' '
        for index in range(attr_num):
            out_line += str(int(attr[index])) + ' '
        out_line += '\n'
        out_f.write(out_line)


if __name__ == '__main__':
    main()
