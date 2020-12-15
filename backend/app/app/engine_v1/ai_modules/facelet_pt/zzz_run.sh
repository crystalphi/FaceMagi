#!/bin/bash

echo '注意：由于该项所用的 vgg_decoder 只能在 torch-0.3.1 上加载，而该版本 torch 不支持 py3.7，所以这里统一使用 py3.6/3.5'
#echo 'python3.6 -m pip install torch-0.3.1-cp36-cp36m-linux_x86_64.whl'
echo 'pip install torch==0.3.1 && pip install torchvision==0.2.0'
echo ''


#INPUT_IMAGE=examples/input.png
#IMAGE_SIZE=800,600

#INPUT_IMAGE=examples/jdas-07.jpg
#INPUT_IMAGE=examples/vvdd-11.jpg
INPUT_IMAGE=examples/three-ladies.jpg
IMAGE_SIZE=1000,816

echo "处理图片：${INPUT_IMAGE} ${IMAGE_SIZE}"


#EFFECT=older
EFFECT=younger
#EFFECT=facehair
#EFFECT=feminization
#EFFECT=masculinization

echo "应用特征：${EFFECT}"


ON_DEVICE='-cpu'
ON_DEVICE='' # use gpu

if [ "${ON_DEVICE}" == "-cpu" ]; then
    echo "使用设备：CPU"
else
    echo "使用设备：GPU"
fi


USE_MODEL='--local_model'
USE_MODEL='' # use pre-trained model

if [ "${USE_MODEL}" == "--local_model" ]; then
    echo "使用模型：本地训练模型"
else
    echo "使用模型：预训练模型"
fi

STRENGTH=6
echo "处理强度：${STRENGTH}"


PYTHON=python3
time $PYTHON test_facelet_net.py test_image --input_path $INPUT_IMAGE --effect $EFFECT --strength $STRENGTH --size $IMAGE_SIZE $USE_MODEL $ON_DEVICE

