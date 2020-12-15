import numpy as np
import cv2
import caffe
import os
import random
from pandas.io.parsers import read_csv

lm_name = '../../data/CelebA/list/train_full.txt'
ln_name = '../../data/CelebA/list/val_full.txt'
mean_file = '../../data/pretrained/ResNet_mean.binaryproto'
prefix = '../../data/'
proto_data = open(mean_file, "rb").read()
a = caffe.io.caffe_pb2.BlobProto.FromString(proto_data)
mean = caffe.io.blobproto_to_array(a)[0]
target_height = 224
target_width = 224
attri_num = 40


def img_path_to_parse(img_path):
    result = img_path
    result = result.replace('img_align_celeba', 'img_celeba_pix2pix')
    result = result.replace('.jpg', '_synthesized_image.jpg')
    return result


def pre_process(color_img, is_mirror=False):
    resized_img = cv2.resize(color_img, (target_width, target_height))
    if is_mirror:
        flip_img = cv2.flip(resized_img, 1)
        return np.transpose(flip_img, (2, 0, 1)) - mean
    else:
        return np.transpose(resized_img, (2, 0, 1)) - mean


class TrainLayer(caffe.Layer):

    total_namelist = []
    attri_array =[]
    img_num = 0
    batch = 20

    def setup(self, bottom, top):
        filename = lm_name
        det_df = read_csv(filename, sep=' ', header=None)
        self.total_namelist = det_df[det_df.columns[0]].values
        self.img_num = len(self.total_namelist)
        self.attri_array = np.zeros((self.img_num, attri_num))
        attr_f = open(lm_name, 'r')
        attr_line = attr_f.readline().strip().split()
        i = 0
        while attr_line:
            for j in range(0, attri_num):
                value = int(float(attr_line[j + 1]))
                self.attri_array[i, j] = value
            attr_line = attr_f.readline().strip().split()
            i += 1
        top[0].reshape(self.batch, 3, target_height, target_width)
        top[1].reshape(self.batch, 3, target_height, target_width)
        top[2].reshape(self.batch, attri_num)

    def reshape(self, bottom, top):
        pass

    def forward(self, bottom, top):
        for i in range(self.batch):
            idx = random.randint(0, self.img_num-1)
            img_path = os.path.join(prefix, self.total_namelist[idx])
            parse_path = img_path_to_parse(img_path)
            im = cv2.imread(img_path)
            parse_im = cv2.imread(parse_path)
            assert im is not None
            if im is not None:
                is_mirror = random.random() >= 0.5
                top[0].data[i] = pre_process(im, is_mirror)
                top[1].data[i] = pre_process(parse_im, is_mirror)
                top[2].data[i] = self.attri_array[idx]


class ValLayer(caffe.Layer):

    total_namelist = []
    attri_array = []
    img_num = 0
    batch = 20

    def setup(self, bottom, top):
        filename = ln_name
        det_df = read_csv(filename,sep=' ', header=None)
        self.total_namelist = det_df[det_df.columns[0]].values
        self.img_num = len(self.total_namelist)
        self.attri_array = np.zeros((self.img_num, attri_num))
        attr_f = open(ln_name, 'r')
        attr_line = attr_f.readline().strip().split()
        i = 0
        while attr_line:
            for j in range(0, attri_num):
                value = int(float(attr_line[j + 1]))
                self.attri_array[i, j] = value
            attr_line = attr_f.readline().strip().split()
            i += 1
        top[0].reshape(self.batch, 3, target_height, target_width)
        top[1].reshape(self.batch, 3, target_height, target_width)
        top[2].reshape(self.batch, attri_num)

    def reshape(self, bottom, top):
        pass

    def forward(self, bottom, top):
        for i in range(self.batch):
            idx = random.randint(0, self.img_num-1)
            img_path = os.path.join(prefix, self.total_namelist[idx])
            parse_path = img_path_to_parse(img_path)
            im = cv2.imread(img_path)
            parse_im = cv2.imread(parse_path)
            assert im is not None
            if im is not None:
                is_mirror = random.random() >= 0.5
                top[0].data[i] = pre_process(im, is_mirror)
                top[1].data[i] = pre_process(parse_im, is_mirror)
                top[2].data[i] = self.attri_array[idx]

    def backward(self, top, propagate_down, bottom):
        pass
