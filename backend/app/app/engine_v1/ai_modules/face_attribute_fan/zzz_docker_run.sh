echo '初始化该容器时，还需要进 bash 执行 如下手工操作：'
echo 'pip install opencv-python'
echo 'pip install numpy==1.15.0'
echo '然后另起终端，执行 docker ps 和 docker commit ... 保存修改。具体见下面代码示例。'

#$ docker ps
#	CONTAINER ID    IMAGE           COMMAND         CREATED         STATUS          PORTS       NAMES
#	96621f37028c    0ef2e08ed3fa    "/bin/bash"     3 minutes ago   Up 3 minutes                thirsty_torvalds
#
# 得到CONTAINER ID，再提交
#$ docker commit 96621f37028c 0ef2e08ed3fa
#	sha256:919694de9dda0f070de8839284e0a3b8f03e9bf88207111e144986d3aaefb2a9


#docker run -it -v $(pwd):/opt/work bvlc/caffe:cpu bash 

USE_SCRIPT=./demo_single_path.sh
#USE_SCRIPT=./demo_dual_path.sh
docker run -it -v $(pwd)/../../../../..:/opt/work bvlc/caffe:cpu bash -c "cd /opt/work/datasets/CelebA/tools/01-attribute-prediction/01-FaceAttribute-FAN && bash $USE_SCRIPT"

sed 's/^\.\/data\/demo\///g' result/demo_result.list | sed 's/ 1/  1/g' | sed 's/ 0/ -1/g' > result/demo_result_final.list

echo ''
echo '面部特征判断结果已输出到文件：result/demo_result_final.list'
echo '请将相应的行手工导入目标文件：../../../Anno/list_attr_celeba.txt'
