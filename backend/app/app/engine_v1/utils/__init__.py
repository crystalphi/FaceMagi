# -*- coding: utf-8 -*-

import os
import sys
import io
import cv2
import json
import tempfile
import numpy as np
from PIL import Image
from torchvision import transforms
from skimage.filters import gaussian


def list_all_files(rootdir, recursion=False):
    _files = []
    list = os.listdir(rootdir) # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir,list[i])
        if os.path.isdir(path) and recursion:
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
            _files.append(path)
    return _files


def image_convert_rgb(image):
    """将 png 等图片统一转为 jpg 格式"""

    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    return image


def image_resize_default(image, img_h_max=1800):
    """对过大的PIL图片进行等比缩小处理"""

    img_w, img_h = image.size
    #print('--> img_w: {0}, img_h: {1}'.format(img_w, img_h))
    if img_h != img_h_max:
        # or Image.BICUBIC
        image = image.resize(
            (int(img_w * (float(img_h_max) / img_h)), img_h_max), Image.ANTIALIAS)

    return image


def image_resize_cv2(image_cv2, img_h_max=1800):
    """对过大的cv2图片进行等比缩小处理"""

    img_w, img_h = image_cv2.shape[0:2]
    #print('--> img_w: {0}, img_h: {1}'.format(img_w, img_h))
    if img_h > img_h_max:
        image = cv2.resize(
            image_cv2, (int(img_w * (float(img_h_max) / img_h)), img_h_max), interpolation=cv2.INTER_NEAREST)  # default: INTER_LINEAR

    return image


def image_blend(image1, image2, alpha=0.5, image_2_tpbg=False):
    """图片合并，需要相同大小"""

    image1 = image1.convert('RGBA')
    image2 = image2.convert('RGBA')
    if image_2_tpbg:
        image2 = image_transparent_bg(image2)  # FIXME: 这种方式效果很有限

    return Image.blend(image1, image2, alpha)


def image_transparent_bg(img):
    """以第一个像素为准，相同色改为透明"""

    img = img.convert('RGBA')
    L, H = img.size
    color_0 = img.getpixel((0, 0))
    for h in range(H):  # FIXME: 这种循环方式效率低，需修改
        for l in range(L):
            dot = (l, h)
            color_1 = img.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                img.putpixel(dot, color_1)

    return img


def pil_to_skimage(img):
    """
    Convert PIL image to a Skimage image
    :param img: PIL image object
    :return: Skimage image object
    """
    # Get the absolute path of the working directory
    #abspath = os.path.dirname(__file__)
    abspath = '/tmp'

    # Create a temp file to store the image
    temp = tempfile.NamedTemporaryFile(
        suffix=".jpg", delete=False, dir=abspath)

    # Save the image into the temp file
    img.save(temp.name, 'JPEG')

    # Read the image as a SciKit image object
    import skimage
    ski_img = skimage.io.imread(temp.name, plugin='pil')

    # Close the file
    temp.close()

    # Delete the file
    os.remove(temp.name)

    # skimage.io.imsave('/app/xxx.jpg',ski_img)
    return ski_img


def image_pil_to_cv2(image_pil):
    """PIL.Image转换成OpenCV格式"""
    image_cv2 = cv2.cvtColor(np.asarray(image_pil), cv2.COLOR_RGB2BGR)
    return image_cv2


def image_cv2_to_pil(image_cv2):
    """OpenCV转换成PIL.Image格式"""
    image_pil = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB))
    return image_pil


def image_pil_to_ndarray(image_pil):
    """PIL.Image 转成 ndarray"""
    return np.asarray(image_pil)


def image_ndarray_to_pil(image_np):
    """ndarray 转成 PIL.Image"""
    return Image.fromarray(image_np)


def image_pil_to_tensor(image_pil):
    """PIL.Image 转成 pytorch tensor"""
    return transforms.ToTensor()(image_pil)


def image_tensor_to_pil(image_tensor):
    """pytorch tensor 转成 PIL.Image"""
    return transforms.ToPILImage()(image_tensor).convert('RGB')


# -----------------------------------------------
# 以下为基于 OpenCV 2 的图像处理函数集合
# -----------------------------------------------

def cv2_image_filter(img):  # 计算图像梯度（高反差像素）
    x = cv2.Sobel(img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(img, cv2.CV_16S, 0, 1)

    absx = cv2.convertScaleAbs(x)
    absy = cv2.convertScaleAbs(y)
    dist = cv2.addWeighted(absx, 0.5, absy, 0.5, 0)

    return dist


def cv2_add_image(img1, img2, alpha, gamma=0):
    """ 按照 alpha 比率合并两张图片
        函数要求两张图必须是同一个size
        alpha，beta，gamma可调
    """
    h, w, _ = img1.shape
    if img2.shape[0] != h or img2.shape[1] != w:
        img2 = cv2.resize(img2, (w, h), interpolation=cv2.INTER_AREA)
    beta = 1 - alpha
    img_add = cv2.addWeighted(img1, alpha, img2, beta, gamma)

    return img_add


def cv2_normalize(img):
    """对比度增强 - 采用直方图正规化方式"""
    # image_out = cv2.normalize(img, dst=None,
    #                        alpha=350, beta=10, norm_type=cv2.NORM_MINMAX)
    image_out = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return image_out


def cv2_sharpen_gaus(img):
    """图片锐化 - 基于高斯方法。适合锐化头发等"""
    img = img * 1.0
    gauss_out = gaussian(img, sigma=5, multichannel=True)

    alpha = 1.5
    img_out = (img - gauss_out) * alpha + img

    img_out = img_out / 255.0

    mask_1 = img_out < 0
    mask_2 = img_out > 1

    img_out = img_out * (1 - mask_1)
    img_out = img_out * (1 - mask_2) + mask_2
    img_out = np.clip(img_out, 0, 1)
    img_out = img_out * 255

    return np.array(img_out, dtype=np.uint8)


def cv2_sharpen_kernel(img, k_idx=2):
    """图像锐化 - 基于自定义卷积核。适合锐化模糊但平滑的图像"""
    kernels = [
        np.array([
            [-1, -1, -1],
            [-1, 9, -1],
            [-1, -1, -1]]),
        np.array([
            [1, 1, 1],
            [1, -7, 1],
            [1, 1, 1]]),
        np.array([
            [-1, -1, -1, -1, -1],
            [-1, 2, 2, 2, -1],
            [-1, 2, 8, 2, -1],
            [-1, 2, 2, 2, -1],
            [-1, -1, -1, -1, -1]])/8.0
    ]

    if k_idx not in range(3):
        return img

    return cv2.filter2D(img, -1, kernels[k_idx])
