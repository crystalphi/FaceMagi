import os.path as osp
import glob
import cv2
import time
import numpy as np
import torch
import RRDBNet_arch as arch

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


model_path = 'models/RRDB_ESRGAN_x4.pth'  # models/RRDB_ESRGAN_x4.pth OR models/RRDB_PSNR_x4.pth

test_img_folder = 'LR/*'

model = arch.RRDBNet(3, 3, 64, 23, gc=32)
model.load_state_dict(torch.load(model_path), strict=True)
model.eval()

if torch.__version__ >= '0.4':
    device = torch.device('cuda')
    #device = torch.device('cpu')
    model = model.to(device)
else:
    model = model.cuda()
    #model = model.cpu()

print('Model path {:s}. \nTesting...'.format(model_path))

idx = 0
for path in glob.glob(test_img_folder):
    idx += 1
    base = osp.splitext(osp.basename(path))[0]
    print(idx, base)
    # read images
    t1 = time.time()
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    img = img * 1.0 / 255
    img = torch.from_numpy(np.transpose(img[:, :, [2, 1, 0]], (2, 0, 1))).float()
    img_LR = img.unsqueeze(0)
    
    if torch.__version__ >= '0.4':
        img_LR = img_LR.to(device)
        with torch.no_grad():
            output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    else:
        from torch.autograd import Variable
        img_LR = Variable(img_LR, volatile=True)
        img_LR = img_LR.cuda()
        #img_LR = img_LR.cpu()
        output = model(img_LR).data.squeeze().float().cpu().clamp_(0, 1).numpy()
    
    output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
    output = (output * 255.0).round()
    cv2.imwrite('results/{:s}_rlt.png'.format(base), output)
    t2 = time.time()
    print('{}s used'.format(t2-t1))

