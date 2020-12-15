#!/bin/sh

export SECRET_KEY='JDD108@HAREKRISHNA'
export MODEL_DIR=`pwd`'/app/engine_v1/models_release'

#export FLASK_ENV='default'
#export FLASK_ENV='production' # 等同于 default
export FLASK_ENV='development'
#export FLASK_ENV='testing'

#python3 server.py # 使用 flask 进行 HTTP 服务，绑定 5000 端口

FLASK_DEBUG=1 gunicorn --bind=:5000 --worker-class=eventlet --reload --workers=1 server:app

# gunicorn 示例。logging初始化指定了一个日志文件，workers指定为8：
#gunicorn --bind=1.2.3.4:5000 --worker-class=eventlet --reload --workers=8 server:app
