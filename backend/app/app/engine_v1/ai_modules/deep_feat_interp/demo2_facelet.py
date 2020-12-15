# -*- coding: utf-8 -*-  

'''
This script aims to extract attribute vectors from images. It is modified by the demo2.py.

NOTE: it works with the DFI project (https://github.com/paulu/deepfeatinterp) rather than this project.
Please copy this script to the root folder of DFI project before runing it.

Please use
python demo2_facelet.py -h
to see the help of options.

For more details, please see readme.md.
'''
from __future__ import division
from __future__ import with_statement
from __future__ import print_function

import time
import numpy
import json
import os.path
import argparse
import alignface
import imageutils
import utils
from tqdm import tqdm
import glob
import deepmodels



def fit_submanifold_landmarks_to_image(template, original, Xlm, face_d, face_p, landmarks=list(range(68))):
    '''
    Fit the submanifold to the template and take the top-K.

    Xlm is a N x 68 x 2 list of landmarks.
    '''
    lossX = numpy.empty((len(Xlm),), dtype=numpy.float64)
    MX = numpy.empty((len(Xlm), 2, 3), dtype=numpy.float64)
    nfail = 0
    for i in range(len(Xlm)):
        lm = Xlm[i]
        try:
            M, loss = alignface.fit_face_landmarks(Xlm[i], template, landmarks=landmarks, image_dims=original.shape[:2])
            lossX[i] = loss
            MX[i] = M
        except alignface.FitError:
            lossX[i] = float('inf')
            MX[i] = 0
            nfail += 1
    if nfail > 1:
        print('fit submanifold, {} errors.'.format(nfail))
    a = numpy.argsort(lossX)
    return a, lossX, MX


if __name__ == '__main__':
    # configure by command-line arguments
    parser = argparse.ArgumentParser(description='Extracting attribute vector for facelet training',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-e', '--effect', type=str, default='facehair', help='desired transformation')
    parser.add_argument('-ip', '--input_path', type=str,default='images/celeba', help='the training image folder')
    parser.add_argument('-gpu', type=str, default='0', help='the gpu id to use')
    parser.add_argument('--backend', type=str, default='torch', choices=['torch', 'caffe+scipy'],
                        help='reconstruction implementation')
    parser.add_argument('--K', type=int, default=100, help='number of nearest neighbors')
    parser.add_argument('--delta', type=str, default='3.5', help='comma-separated list of interpolation steps')
    parser.add_argument('--npz_path', type=str, default='attribute_vector', help='the path to store npz data')
    parser.add_argument('--save_image', action='store_true', default=False, help='output image is saved')
    config = parser.parse_args()
    # print(json.dumps(config.__dict__))
    os.environ['CUDA_VISIBLE_DEVICES'] = config.gpu

    # load models
    if config.backend == 'torch':
        import deepmodels_torch
        model = deepmodels_torch.vgg19g_torch(device_id=0)
    elif config.backend == 'caffe+scipy':
        model = deepmodels.vgg19g(device_id=0)
    else:
        raise ValueError('Unknown backend')

    classifier = deepmodels.facemodel_attributes()
    fields = classifier.fields()
    print("classifier.fields:", fields)
    
    face_d, face_p = alignface.load_face_detector()
    
    # Set the free parameters
    K = config.K
    delta_params = [float(x.strip()) for x in config.delta.split(',')]
    X = glob.glob(config.input_path+'/*')
    t0 = time.time()
    opathlist = []

    timestamp = int(round(time.time()))

    # for each test image
    max_images_used = len(X)
    #max_images_used = len(X) if len(X) < 5000 else 5000
    print('set max_images_used = %d' % max_images_used)
    for i in tqdm(range(max_images_used)):
        xX = X[i]
        prefix_path = os.path.splitext(xX)[0]
        try:
            template, original = alignface.detect_landmarks(xX, face_d, face_p)
        except:
            print('%s face landmark detection error'% xX)
            continue
        image_dims = original.shape[:2]
        XF = model.mean_F([original])
        XA = classifier.score([xX])[0]
        #print('--> xX:%s, original:%s, XF:%s, XA:%s' % (xX, original, XF, XA))

        # select positive and negative sets based on gender and mouth

        # You can add other attributes here.
        idx_male = fields.index('Male')
        idx_young = fields.index('Young')
        idx_smiling = fields.index('Smiling')
        #print("--> index of Male, Smiling:", idx_male, idx_smiling)
        idx_no_beard = fields.index('No_Beard')
        idx_mustache = fields.index('Mustache')
        idx_senior = fields.index('senior')
        # 这里可以选取的 field 有 71 种，分别为：
        # ('5_o_Clock_Shadow', 'Arched_Eyebrows', 'Attractive', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips', 'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Blurry', 'Brown_Hair', 'Bushy_Eyebrows', 'Chubby', 'Double_Chin', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup', 'High_Cheekbones', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'Narrow_Eyes', 'No_Beard', 'Oval_Face', 'Pale_Skin', 'Pointy_Nose', 'Receding_Hairline', 'Rosy_Cheeks', 'Sideburns', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings', 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace', 'Wearing_Necktie', 'Young', 'asian', 'baby', 'black', 'brown_eyes', 'child', 'color_photo', 'eyes_open', 'flash', 'flushed_face', 'frowning', 'fully_visible_forehead', 'harsh_lighting', 'indian', 'middle_aged', 'mouth_closed', 'mouth_wide_open', 'no_eyewear', 'obstructed_forehead', 'outdoor', 'partially_visible_forehead', 'posed_photo', 'round_face', 'round_jaw', 'senior', 'shiny_skin', 'soft_lighting', 'square_face', 'strong_nose_mouth_lines', 'sunglasses', 'teeth_not_visible', 'white')

        # 注意：根据 deepmodels.py 中的代码逻辑，score 取值只能与 0 比较判断真假，与其他值比较会有逻辑错误
        if config.effect == 'older':
            cP = [(idx_male, XA[idx_male]>=0), (idx_young, True)]
            cQ = [(idx_male, XA[idx_male]>=0), (idx_young, False)]
        elif config.effect == 'younger':
            cP = [(idx_male, XA[idx_male]>=0), (idx_young, False)]
            cQ = [(idx_male, XA[idx_male]>=0), (idx_young, True)]
        elif config.effect == 'facehair':
            #cP = [(idx_male, XA[idx_male]>=0), (idx_smiling, XA[idx_smiling]>=0), (idx_no_beard, True), (idx_mustache, False)]
            cP = [(idx_male, XA[idx_male]>=0), (idx_no_beard, True), (idx_mustache, False)]
            #cQ = [(idx_male, XA[idx_male]>=0), (idx_smiling, XA[idx_smiling]>=0), (idx_no_beard, False), (idx_mustache, True)]
            cQ = [(idx_male, XA[idx_male]>=0), (idx_no_beard, False), (idx_mustache, True)]
        elif config.effect == 'senior':
            cP = [(idx_male, XA[idx_male]>=0), (idx_senior, False)]
            cQ = [(idx_male, XA[idx_male]>=0), (idx_senior, True)]
        else:
            raise ValueError('Unknown method')
        P = classifier.select(cP, XA)
        Q = classifier.select(cQ, XA)
        if len(P) < 4 * K or len(Q) < 4 * K:
            print('{}: Not enough images in database (|P|={}, |Q|={}).'.format(xX, len(P), len(Q)))
            continue
        #print('--> prefix_path:', prefix_path) #images/celeba/102103
        image_pre = prefix_path.split('/')[-1]
        print("image {}.jpg attr scores: \n{}".format(image_pre, classifier.lookup_scores(['images/facemodel/celeba/{}.jpg'.format(image_pre)])[0,:]))
        print("found enough images for image {}.jpg, scores[Male, Smiling, No_Beard, Mustache, senior]:".format(image_pre), classifier.lookup_scores(['images/facemodel/celeba/{}.jpg'.format(image_pre)])[0, [idx_male, idx_smiling, idx_no_beard, idx_mustache, idx_senior]])

        # fit the best 4K database images to input image
        Plm = classifier.lookup_landmarks(P[:4 * K])
        Qlm = classifier.lookup_landmarks(Q[:4 * K])
        idxP, lossP, MP = fit_submanifold_landmarks_to_image(template, original, Plm, face_d, face_p)
        idxQ, lossQ, MQ = fit_submanifold_landmarks_to_image(template, original, Qlm, face_d, face_p)
        # Use the K best fitted images
        xP = [P[i] for i in idxP[:K]]
        xQ = [Q[i] for i in idxQ[:K]]
        PF = model.mean_F(utils.warped_image_feed(xP, MP[idxP[:K]], image_dims))
        QF = model.mean_F(utils.warped_image_feed(xQ, MQ[idxQ[:K]], image_dims))
        #WF=(QF-PF)/((QF-PF)**2).mean() # beta scaling enabled
        WF = (QF - PF)

        file_save_path = os.path.join(config.npz_path, config.effect)
        if not os.path.exists(file_save_path):
            os.makedirs(file_save_path)
        file_name = os.path.basename(xX)
        file_name = file_name.split('.')[:-1]
        file_name = '.'.join(file_name)
        numpy.savez('{}/{}_{}.npz'.format(file_save_path, file_name, config.effect), WF=WF)


        if config.save_image: # True: make and save a image and then exit, False: just build npz files
            max_iter=500
            init=original
            # for each interpolation step
            result=[]
            for delta in delta_params:
              print(xX,image_dims,delta,len(xP),len(xQ))
              t2=time.time()
              Y=model.F_inverse(XF+WF*delta,max_iter=max_iter,initial_image=init)
              t3=time.time()
              print('{} minutes to reconstruct'.format((t3-t2)/60.0))
              result.append(Y)
              max_iter=500//2
              init=Y
            result=numpy.asarray([result])
            original=numpy.asarray([original])
            #m=imageutils.montage(numpy.concatenate([numpy.expand_dims(original,1),result],axis=1))
            m=imageutils.montage(result)
            opath='{}_{}_{}{}.{}'.format(prefix_path, timestamp, config.effect, '_', 'jpg')
            print('--> opath:', opath)
            imageutils.write(opath,m)
            break

