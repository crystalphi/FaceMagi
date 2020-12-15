import glob
import cv2
import time
import os.path as osp
import numpy as np
import torch
from torchvision import transforms

# 兼容 torch < 0.4
import torch._utils
try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2

from app.engine_v1.utils import image_convert_rgb, image_resize_default, image_blend
from app.engine_v1 import app_config, logger, image_process_wrap, face_image_blend

import app.engine_v1.utils.esrgan.RRDBNet_arch as arch


def init_model(gpu_id=-1):
    # RRDB_ESRGAN_x4.pth OR RRDB_PSNR_x4.pth
    #print('--> app_config.MODEL_DIR:', app_config.MODEL_DIR)
    model_path = osp.join(app_config.MODEL_DIR, 'ESRGAN_models/RRDB_ESRGAN_x4.pth')
    
    _model = arch.RRDBNet(3, 3, 64, 23, gc=32)
    _model.load_state_dict(torch.load(model_path), strict=True)
    _model.eval()

    if torch.__version__ >= '0.4':
        _model = _model.to(torch.device('cuda')) # or 'cpu'
    else:
        _model = _model.cuda()

    model = {}
    model['model'] = _model

    logger.info('esrgan init_model DONE! gpu_id: {}'.format(gpu_id))
    return model


def process_image(image, engine_model, output_w, output_h):
    # 如果输入尺寸大于等于输出尺寸，则不必做超解析
    in_w, in_h = image.size
    if in_h >= output_h:
        return image

    t1 = time.time()
    image = np.array(image).astype(np.uint8) # pil to numpy.array

    image = image * 1.0 / 255
    image = torch.from_numpy(np.transpose(image[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = image.unsqueeze(0)
    
    model = engine_model['model']

    if torch.__version__ >= '0.4':
        img_LR = img_LR.to(torch.device('cuda'))
        with torch.no_grad():
            output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    else:
        from torch.autograd import Variable
        img_LR = Variable(img_LR, volatile=True)
        img_LR = img_LR.cuda()
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round().astype(np.uint8)

    output = transforms.ToPILImage()(output) # numpy.array to pil
    output = image_resize_default(output, output_h)
    
    t2 = time.time()
    print('--> esrgan: {}s used'.format(t2-t1))
    #print('--> type(output): {}'.format(type(output)))
    logger.info('esrgan process image, input size: {} w, {} h, output size: {} w, {} h'
                .format(in_w, in_h, output.size[0], output.size[1]))

    return output
