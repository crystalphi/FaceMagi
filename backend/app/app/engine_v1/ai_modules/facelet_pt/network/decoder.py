'''
Note: The decoder is slightly different from the original paper. In this implementation, the decoder only learns the
difference between the original image and the edited image. In practice it works better and easier to train.
'''

import re
import torch
from torch import nn
from ..util import util
from ..global_vars import *
from . import base_network


class vgg_decoder(base_network.BaseModel, nn.Module):
    def __init__(self, pretrained=True):
        super(vgg_decoder, self).__init__()
        self._define_model()
        if pretrained:
            print('loading pretrained weights of VGG decoder')
            #state_dict = torch.utils.model_zoo.load_url(model_urls['vgg_decoder_res'], model_dir='facelet_bank')
            state_dict = util.load_from_url(model_urls['vgg_decoder_res'], save_dir='facelet_bank')
            
            # 为了在 torch 0.4 中加载 0.3 训练的模型，已修改了 Vgg_recon 模型代码中的关键字
            # 故此这里也需要对读取的模型字段做同样的修改，方可加载成功
            import re
            state_dict = {re.sub(r'conv(\.)(\d)','conv_\g<2>',k):v for k,v in state_dict.items()}
            state_dict = {re.sub(r'norm(\.)(\d)','norm_\g<2>',k):v for k,v in state_dict.items()}
            state_dict = {re.sub(r'relu(\.)(\d)','relu_\g<2>',k):v for k,v in state_dict.items()}
            state_dict = {re.sub(r'drop(\.)(\d)','drop_\g<2>',k):v for k,v in state_dict.items()}
            state_dict = {k.replace('unpool.conv','unpool_conv'):v for k,v in state_dict.items()}
            state_dict = {k.replace('unpool.norm','unpool_norm'):v for k,v in state_dict.items()}
            state_dict = {k.replace('interp.conv','interp_conv'):v for k,v in state_dict.items()}
            state_dict = {k.replace('interp.norm','interp_norm'):v for k,v in state_dict.items()}
            
            model_dict = self.model.state_dict()
            model_dict.update(state_dict)
            #print('model_dict type: %s, keys: %s' % (type(model_dict), model_dict.keys()))
            self.model.load_state_dict(model_dict)

    def _define_model(self):
        self.model = base_network.Vgg_recon()

    def forward(self, fy, img=None):
        fy = [util.toVariable(f) for f in fy]
        y = self.model.forward(fy)
        y = y + img
        return y

    def load(self, pretrain_path, epoch_label='latest'):
        self.load_network(pretrain_path, self.model, 'recon', epoch_label)
