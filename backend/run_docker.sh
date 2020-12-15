# 构建镜像
echo '重建镜像(如有更新): docker-compose build web'

echo '如果需要进入控制台，可以另起终端执行：docker exec -it backend_py_web_1 /bin/bash'
echo '如果需要验证 docker 内显卡加速，可以另起终端执行：nvidia-docker run nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04 nvidia-smi'

# 执行构建镜像，(重新)创建服务，启动服务，并关联服务相关容器等一系列操作
echo '开始执行：docker-compose up [web]'
#docker-compose stop web
docker-compose stop 
#docker-compose up web
docker-compose up
# 产品部署时需使用下面这行，以开启 nginx 服务支持
#docker-compose --compatibility up

# 仅启动服务，不进行（重新）创建
#docker-compose run web

# 启动服务，执行 bash 控制台
#（注意：这里貌似没有应用 yml 中的配置，建议修改 yml 文件中的 cmd 后使用上述 up 命令替代）
#docker-compose run --rm web bash

