# -*- coding: utf-8 -*-
""" 任务及引擎管理服务主进程。在 flask 之外，作为独立进程启动。
"""
__author__ = "vedasky"
__copyright__ = "Copyright 2019"

import os
import sys
#import io
#import time
#import numpy as np
#from skimage.io import imread
#from skimage import transform, util
#from keras.models import load_model

BASE_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), "..")
sys.path.append(BASE_DIR)

from app.engine_v1 import app_config, logger
from app.engine_v1.m_server import ManagerServer


if __name__ == '__main__':

    logger.info('')
    logger.info('-' * 40)
    logger.info('- Start Manager Server')
    logger.info('-' * 40)

    # to make sure multiprocess running on CUDA, you have to set start method as "spawn"
    #import multiprocessing as mp
    #mp.set_start_method('spawn')
    # or
    #import torch
    #torch.cuda.current_device()
    #torch.cuda._initialized = True
    # or
    #import torch
    #torch.multiprocessing.set_start_method('spawn')

    manager_server = ManagerServer()
    manager_server.run()

