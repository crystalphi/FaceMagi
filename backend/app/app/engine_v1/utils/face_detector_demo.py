#coding=utf-8
# Many examples on how to do face landmarks using dlib, here is just one:
# https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

# OpenCV - Image manipulation library, Haar classifier and LBP Classifier
# DLib - Machine learning library, HOG with linear classifier, image pyramid and sloding window detection scheme.
# This also has facial landmarks.

# 从测试来看 OpenCV 的结果更适合本项目

import pathlib
import sys
import time
import cv2
import dlib
import numpy as np
from enum import Enum

# Tried only using opencv and adjusting parameters. With the standard font face
# XML there were dissapointing results even when adjusting the two parameters
# given for detectMultiScale method. Hence this now tries to use both open CV image processing library
# and the dlib machine learning library to compare the differences and which
# one could be used. Might be that some specific training is required. We will
# have to see.

OPENCV_BOUNDING_COLOUR = (0, 255, 0)
OPENCV_BOUNDING_THICKNESS = 3
DLIB_BOUNDING_COLOUR = (255, 0, 0)
DLIB_BOUNDING_THICKNESS = 2

# https://github.com/davisking/dlib/blob/master/dlib/image_processing/frontal_face_detector.h details
# what the idx face types are, and we will enumerate them for easy reading. So
# we will convert from numeric value to the text enum shown here for easy reading.


class dlib_face_type(Enum):
    front = 0
    left = 1
    right = 2
    rotated_left = 3
    rotated_right = 4

# Simple test function to simply print filename for now. In future we will process it properly.
# Using attribute as a kind of static variable, although better is to create a class for this. But
# this is a simple test to check out capabilities so will improve later.

def find_faces(file):
    str_file_path = file.absolute().as_posix()

    image = cv2.imread(str_file_path)
    if image is None:
        print('Failed to load image {0}.'.format(file))
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # First process and update the opencv faces
    num_opencv_faces = find_opencv_faces(gray_image, image)

    # Now lest see what dlib finds for faces
    num_dlib_faces = find_dlib_faces(gray_image, image)

    print('{0} opencv and {1} dlib faces found in {2}'.format(
        num_opencv_faces, num_dlib_faces, file))

    if num_opencv_faces > 0 or num_dlib_faces > 0:
        cv2.namedWindow(str_file_path, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(str_file_path, 600, 600)
        cv2.imshow(str_file_path, image)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

# Remember to get landmarks trained data from http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
# See http://dlib.net/face_landmark_detection.py.html for more details.

def find_dlib_faces(detection_image,
                    image,
                    bb_col=OPENCV_BOUNDING_COLOUR,
                    bb_thickness=OPENCV_BOUNDING_THICKNESS,
                    scale_factor=1.2,
                    min_neighbours=6):

    if not hasattr(find_faces, "dlib_face_detector"):
        dlib_face_detector = dlib.get_frontal_face_detector()
        dlib_face_predictor = dlib.shape_predictor(
            '../../models_release/shape_predictor_68_face_landmarks.dat')

    # Upsample is set to 1 which should make this see more faces. Not sure if this is needed yet
    #dlib_faces = dlib_face_detector(detection_image, 1)
    # See http://dlib.net/face_detector.py.html where the example with scores and sub detectors are detailed.
    dlib_faces, scores, idx = dlib_face_detector.run(detection_image, 1, 0)

    dlib_face_count = len(dlib_faces)
    if dlib_face_count != 0:
        for facenum, bb in enumerate(dlib_faces):
            print('Face {0}:{1}, score={2}, facetype={3}...'.format(
                facenum, bb, scores[facenum], dlib_face_type(idx[facenum])))

            # We will draw the bounding box for each face
            cv2.rectangle(image, (bb.left(), bb.top()), (bb.right(
            ), bb.bottom()), DLIB_BOUNDING_COLOUR, DLIB_BOUNDING_THICKNESS)

            # in addition lets show the facial landmarks to see if it can tell good and bad faces
            shapes = dlib_face_predictor(detection_image, bb)

            # initialize the np list of (x, y)-coordinates
            coords = np.zeros((68, 2), dtype=np.dtype)

            # loop over the 68 facial landmarks and convert them
            # to a 2-tuple of (x, y)-coordinates
            for i in range(0, 68):
                coords[i] = (shapes.part(i).x, shapes.part(i).y)

            if (len(coords) > 0):
                print('{0} facial landmarks found for ...'.format(len(coords)))
                for (x, y) in coords:
                    cv2.circle(image, (x, y), 1, (0, 0, 255), 2)

    return dlib_face_count


def find_opencv_faces(detection_image,
                      image,
                      bb_col=OPENCV_BOUNDING_COLOUR,
                      bb_thickness=OPENCV_BOUNDING_THICKNESS,
                      scale_factor=1.2,
                      min_neighbours=6):

    if not hasattr(find_faces, "opencv_face_classifier"):
        #haar_classifier = cv2.CascadeClassifier('../../models_release/haarcascade_frontalface_default.xml')
        lbp_classifier = cv2.CascadeClassifier(
            '../../models_release/lbpcascade_frontalface.xml')
        opencv_face_classifier = lbp_classifier

    # Returns ROI of face as a tuple
    opencv_faces = opencv_face_classifier.detectMultiScale(
        detection_image, scale_factor, min_neighbours)

    faces_detected = len(opencv_faces)
    if len(opencv_faces) != 0:
        img_h, img_w = image.shape[:2]
        for (x, y, w, h) in opencv_faces:
            x, y, w, h = adjust_face_area(img_w, img_h, x, y, w, h)
            print('img_w: %d, img_h: %d, x:%d, y:%d, w:%d, h:%d' % (img_w, img_h, x, y, w, h))
            print(
                'opencv found face: x:{0}, y:{1}, w:{2}, h:{3}'.format(x, y, w, h))
            cv2.rectangle(image, (x, y), (x+w, y+h), bb_col, bb_thickness)

    return faces_detected

# Simple function to iterate all directories and files, and pass it to be processed.
# cwd - The pathlib.PATH for the current directory to be processed
# process_image_fn(file) - the function to be called with the pathlib.PATH of the file

def adjust_face_area(img_w, img_h, fc_x, fc_y, fc_w, fc_h):
    '''
    由于 dlib 或 opencv 识别出来的面部区域都过小，所以需要放大。方法如下。
    根据项目需求调整坐标：
         如面部比例小于 0.5，则范围放大 1 倍，如果越界则平移；
         如面部比例大于 0.5，则范围放大至图片短边长，如果越界则平移。
    '''
    def new_position(img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio):
        fc_x -= int(fc_w * (1 / ratio - 1) / 2)
        fc_y -= int(fc_h * (1 / ratio - 1) / 2)
        fc_w = int(fc_w / ratio) # 按指定比例扩展人脸区域宽度
        fc_h = int(fc_h / ratio) # 按指定比例扩展人脸区域高度
        if fc_x < 0:
            fc_x = 0 # 扩展后如果越过左边界，则平移，与左边界对齐
        if fc_x + fc_w > img_w:
            fc_x = img_w - fc_w # 扩展后如果越过右边界，则平移，与右边界对齐
        if fc_y < 0:
            fc_y = 0 # 扩展后如果越过上边界，则平移，与上边界对齐
        if fc_y + fc_h > img_h:
            fc_y = img_h - fc_h # 扩展后如果越过下边界，则平移，与下边界对齐
        return fc_x, fc_y, fc_w, fc_h

    ratio_w = fc_w / float(img_w)
    ratio_h = fc_h / float(img_h)
    if ratio_w <= 0.5 and ratio_h <= 0.5:
        fc_x, fc_y, fc_w, fc_h = new_position(img_w, img_h, fc_x, fc_y, fc_w, fc_h, 0.5)
    elif ratio_w >= ratio_h:
        # 扩展人脸区域到原图宽度，高度等比扩展
        fc_x, fc_y, fc_w, fc_h = new_position(img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio_w)
    else:
        # 扩展人脸区域到原图高度，宽度等比扩展
        fc_x, fc_y, fc_w, fc_h = new_position(img_w, img_h, fc_x, fc_y, fc_w, fc_h, ratio_h)
    
    return fc_x, fc_y, fc_w, fc_h

def process_all_files(cwd, process_image_fn):
    '''Recursively go through all files in all directories and process each one'''
    filecount = 0

    # Create a path for the current working directory
    cwd = pathlib.Path(cwd)

    # Process all files first
    for afile in [d for d in cwd.iterdir() if d.is_file()]:
        process_image_fn(afile.resolve())
        filecount += 1

    # And then iterate all sub directories
    for dir in [d for d in cwd.iterdir() if d.is_dir()]:
        filecount += process_all_files(dir, process_image_fn)

    # Make sure we update how many files processed
    return filecount


# If this is called individually we can iterate the current working directory,
# or the required directory can be supplied as an argument if required.
if __name__ == '__main__':

    # Default is current working directory
    #cwd = pathlib.Path.cwd()
    cwd = pathlib.PurePosixPath('../../static/attgan_pt/')

    # Directory argument supplied
    if len(sys.argv) == 2:
        cwd = pathlib.Path(sys.argv[1])
        if cwd.exists() and cwd.is_dir():
            cwd = pathlib.Path(sys.argv[1])
        else:
            print('ERROR: "{0}" is not a directory.'.format(sys.argv[1]))
            exit(1)

    print('\n -- Processing all files in "{0}" -- \n'.format(cwd))
    start = time.clock()
    print('"{0}" files processed in {1} seconds.\n'.format(
        process_all_files(cwd, find_faces), time.clock()))
