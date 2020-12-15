# -*- coding: utf-8 -*-

import os
import dlib # 人脸识别的库dlib
import cv2 # 图像处理的库OpenCv
import numpy as np
from functools import partial

from app.engine_v1 import app_config, logger


class FaceDetector(object):
    """调用 dlib 等方法检测人脸地图"""

    def __init__(self, engine="opencv"):
        self.engine = engine  # opencv or dlib
        if self.engine == "dlib":
            # dlib预测器
            self.__dlib_face_detector = dlib.get_frontal_face_detector()
            dlib_landmarks_path = os.path.join(
                app_config.MODEL_DIR, 'shape_predictor_68_face_landmarks.dat')
            self.__dlib_shape_predictor = dlib.shape_predictor(
                dlib_landmarks_path)
            logger.info('Face detect engine %s initialized.' % engine)
        elif self.engine == "opencv":
            haar_classifier = cv2.CascadeClassifier(os.path.join(app_config.MODEL_DIR, 'haarcascade_frontalface_default.xml'))
            # lbp_classifier = cv2.CascadeClassifier(os.path.join(app_config.MODEL_DIR, 'lbpcascade_frontalface.xml'))
            self.__opencv_face_detector=haar_classifier
            # self.__opencv_face_detector = lbp_classifier
            logger.info('Face detect engine %s initialized.' % engine)
        else:
            raise(Exception(
                'Unknown face detect engine: %s. Only opencv or dlib allowed!' % engine))

    def __get_dlib_faces(self, img):
        dlib_faces=self.__dlib_face_detector(img, 1)  # or (img, 0)
        if len(dlib_faces) == 0:
            print("No faces")
            return None
        else:
            logger.debug("%d faces detected." % len(dlib_faces))
            faces=[]
            for k, d in enumerate(dlib_faces):
                x=d.left()
                y=d.top()
                w=d.right() - d.left()
                h=d.bottom() - d.top()
                faces.append((x, y, w, h))
            return faces

    def __get_dlib_landmarks(self, img):
        dlib_faces=self.__get_dlib_faces(img)
        landmarks=[]
        for idx in dlib_faces:
            landmarks.append(self.__dlib_shape_predictor(img, dlib_faces[idx]))
        return landmarks

    def __get_opencv_faces(self, img, min_size):
        detection_image=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        bb_col=(0, 255, 0)
        bb_thickness=3
        scale_factor=1.2
        min_neighbours=6

        # Returns ROI of face as a tuple
        opencv_faces=self.__opencv_face_detector.detectMultiScale(
            detection_image, scale_factor, min_neighbours)

        faces=[]
        if len(opencv_faces) != 0:
            img_h, img_w=img.shape[:2]
            for (x, y, w, h) in opencv_faces:
                x, y, w, h=self.__adjust_face_area(
                    img_w, img_h, x, y, w, h, min_size)
                logger.debug(
                    'opencv found face: x:{0}, y:{1}, w:{2}, h:{3}. img_w:{4}, img_h:{5}'.format(x, y, w, h, img_w, img_h))
                # cv2.rectangle(img, (x, y), (x+w, y+h), bb_col, bb_thickness) # 人脸加方框
                faces.append((x, y, w, h))

        return faces

    # Simple function to iterate all directories and files, and pass it to be processed.
    # cwd - The pathlib.PATH for the current directory to be processed
    # process_image_fn(file) - the function to be called with the pathlib.PATH of the file

    def __adjust_face_area(self, img_w, img_h, fc_x, fc_y, fc_w, fc_h, min_size):
        '''
        由于 dlib 或 opencv 识别出来的面部区域都过小，所以需要放大。方法如下。
        根据项目需求调整坐标：
            如面部比例小于 0.5，则范围放大 1 倍，如果仍小于模型尺寸则放大到一致，如果越界则平移；
            如面部比例大于 0.5，则范围放大至图片短边长，如果越界则平移。
        '''
        def new_position(img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio):
            fc_x -= int(fc_w * (1 / ratio - 1) / 2)
            fc_y -= int(fc_h * (1 / ratio - 1) / 2)
            fc_w=int(fc_w / ratio)  # 按指定比例扩展人脸区域宽度
            fc_h=int(fc_h / ratio)  # 按指定比例扩展人脸区域高度
            if fc_x < 0:
                fc_x=0  # 扩展后如果越过左边界，则平移，与左边界对齐
            if fc_x + fc_w > img_w:
                fc_x=img_w - fc_w  # 扩展后如果越过右边界，则平移，与右边界对齐
            if fc_y < 0:
                fc_y=0  # 扩展后如果越过上边界，则平移，与上边界对齐
            if fc_y + fc_h > img_h:
                fc_y=img_h - fc_h  # 扩展后如果越过下边界，则平移，与下边界对齐
            return fc_x, fc_y, fc_w, fc_h

        ratio_w=fc_w / float(img_w)
        ratio_h=fc_h / float(img_h)
        if ratio_w <= 0.5 and ratio_h <= 0.5:
            ratio=0.5
            if fc_w / 0.5 < min_size:
                ratio=fc_w / float(min_size)
            fc_x, fc_y, fc_w, fc_h=new_position(
                img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio)
        elif ratio_w >= ratio_h:
            # 扩展人脸区域到原图宽度，高度等比扩展
            fc_x, fc_y, fc_w, fc_h=new_position(
                img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio_w)
        else:
            # 扩展人脸区域到原图高度，宽度等比扩展
            fc_x, fc_y, fc_w, fc_h=new_position(
                img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio_h)

        return fc_x, fc_y, fc_w, fc_h


    def __get_opencv_landmarks(self, img):
        # TODO:
        return None

    def get_faces(self, img, min_size):
        if self.engine == "dlib":
            return self.__get_dlib_faces(img)
        elif self.engine == "opencv":
            return self.__get_opencv_faces(img, min_size)
        else:
            return None

    def get_landmarks(self, img):
        if self.engine == "dlib":
            return self.__get_dlib_landmarks(img)
        elif self.engine == "opencv":
            return self.__get_opencv_landmarks(img)
        else:
            return None

    def get_faces_images(self, img, min_size):
        faces=self.get_faces(img, min_size)
        if not faces:
            return []

        face_images=[]
        for (x, y, w, h) in faces:
            # 截取人脸图像
            img_new=img[y:(y+h), x:(x+w)].copy()
            face_images.append((x, y, w, h, img_new))

        return face_images

if __name__ == '__main__':

    # face_detector = FaceDetector(engine="dlib")
    face_detector = FaceDetector(engine = "opencv")

    # 读取图像
    img = cv2.imread("../../static/attgan_pt/vvdd-11.jpg")
    # logger.debug("img/shape:", img.shape)

    # 人脸检测
    faces_images=face_detector.get_faces_images(img, 384)
    logger.debug("got %d faces_images" % len(faces_images))
    # landmarks = face_detector.get_landmarks(img)
    # print("landmarks:", landmarks)

    idx=0
    for (x, y, w, h, img_new) in faces_images:
        # cv2.imshow("face_"+str(idx), img_blank)
        cv2.imwrite("img_face_"+str(idx)+".jpg", img_new)
        idx += 1
    # cv2.waitKey(0)
