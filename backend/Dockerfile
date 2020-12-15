FROM nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04

# ==================================================================
# 1. 系统相关配置
# ------------------------------------------------------------------

ENV PYTHONUNBUFFERED 1
ENV LD_LIBRARY_PATH "${LD_LIBRARY_PATH}:/usr/local/cuda/lib64"
ENV CUDA_HOME=/usr/local/cuda

# https://askubuntu.com/questions/863053/sudo-apt-get-update-error-404-on-16-04
RUN rm /etc/apt/sources.list.d/*

# 指定使用国内源（在国外产品化部署时应取消下面两行）
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN mkdir -p ~/.pip && echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple" > ~/.pip/pip.conf

#RUN apt-get upgrade -y

# install basic dependencies and develop library
RUN apt-get clean && apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        telnet \
        vim \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libjasper-dev \
        libavformat-dev \
        libpq-dev \
        libatlas-base-dev \
        libboost-all-dev \
        libgflags-dev \
        libgoogle-glog-dev \
        libhdf5-serial-dev \
        libleveldb-dev \
        liblmdb-dev \
        libprotobuf-dev \
        libsnappy-dev \
        libssl-dev \
        libffi-dev \
        libgtk2.0-dev \
        libavcodec-dev \
        libv4l-dev
RUN apt-get install -y --no-install-recommends \
        python3-dev \
        python3-pip \
        protobuf-compiler \
        gfortran \
        iputils-ping \ 
    && rm -rf /var/lib/apt/lists/*

# install common python packages
RUN pip3 install --upgrade pip
RUN pip3 install setuptools Cython
RUN pip3 install setuptools -U

# install boost
#RUN wget -O ~/boost.tar.gz https://dl.bintray.com/boostorg/release/1.65.1/source/boost_1_65_1.tar.gz \
#    && tar -zxf ~/boost.tar.gz -C ~ \
#    && cd ~/boost_* \
#    && ./bootstrap.sh --with-python=python3.5 \
#    && ./b2 install --prefix=/usr/local
RUN apt-get install -y --no-install-recommends libboost-all-dev

# install opencv
WORKDIR /
ENV OPENCV_VERSION="3.4.7"
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz
RUN tar zxvf ${OPENCV_VERSION}.tar.gz
RUN mkdir -p /opencv-${OPENCV_VERSION}/cmake_binary && cd /opencv-${OPENCV_VERSION}/cmake_binary \
    && cmake -DBUILD_TIFF=ON \
      -DBUILD_opencv_java=OFF \
      -DWITH_CUDA=OFF \
      -DENABLE_AVX=OFF \
      -DWITH_OPENGL=OFF \
      -DWITH_OPENCL=OFF \
      -DWITH_IPP=OFF \
      -DWITH_TBB=OFF \
      -DWITH_EIGEN=OFF \
      -DWITH_V4L=OFF \
      -DBUILD_TESTS=OFF \
      -DBUILD_PERF_TESTS=OFF \
      -DCMAKE_BUILD_TYPE=RELEASE \
      -DCMAKE_INSTALL_PREFIX=$(python3 -c "import sys; print(sys.prefix)") \
      -DPYTHON_EXECUTABLE=$(which python3) \
      -DPYTHON_INCLUDE_DIR=$(python3 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
      -DPYTHON_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") .. \
    && make -j8 \
    && make install \
    && rm /${OPENCV_VERSION}.tar.gz \
    && rm -r /opencv-${OPENCV_VERSION}

# install dlib
#RUN git clone --branch v19.16 https://github.com/davisking/dlib.git ~/dlib \
RUN wget -c http://dlib.net/files/dlib-19.16.tar.bz2 \
    && tar -jxvf dlib-19.16.tar.bz2 -C ~/ \
    && cd ~/dlib-19.16 \
    && python3 setup.py install --no DLIB_USE_CUDA --no USE_AVX_INSTRUCTIONS --yes USE_SSE4_INSTRUCTIONS \
    && cd ~

# clean installation
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ==================================================================
# 2. Caffe 相关配置（CPU 版）
# ------------------------------------------------------------------

ENV CAFFE_ROOT=/opt/caffe
ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
WORKDIR $CAFFE_ROOT

RUN git clone https://github.com/weiliu89/caffe.git . && git checkout ssd
RUN cd python && for req in $(cat requirements.txt) pydot; do pip3 install $req; done && cd ..

RUN apt-get update && apt-get install -y liblapack-dev liblapack3 libopenblas-base \
        libopenblas-dev libsm6 libxext6 swig libigraph0-dev \
    && ln -s /usr/lib/x86_64-linux-gnu/libhdf5_serial.so.10.1.0 /usr/lib/x86_64-linux-gnu/libhdf5.so \
    && ln -s /usr/lib/x86_64-linux-gnu/libhdf5_serial_hl.so.10.0.2 /usr/lib/x86_64-linux-gnu/libhdf5_hl.so \
    && ln -s /usr/lib/x86_64-linux-gnu/libboost_python-py35.so /usr/lib/x86_64-linux-gnu/libboost_python3.so

COPY misc/caffe/Makefile $CAFFE_ROOT/Makefile
COPY misc/caffe/Makefile.config $CAFFE_ROOT/Makefile.config
RUN python3 -V && export CPLUS_INCLUDE_PATH=/usr/include/python3.5 \
    && make clean \
    && make -j8 && make py && make test -j8

ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig

# ==================================================================
# 3. 项目相关配置
# ------------------------------------------------------------------

RUN groupadd -r app -g 1000 \
    && useradd -u 1000 -r -g app -m -s /sbin/nologin app \
    && mkdir -p /app

# install python packages from app's requirements.txt
# 主要为比较稳定的相关基础软件包
#RUN echo "[global]\nindex-url = https://mirrors.ustc.edu.cn/pypi/web/simple" > ~/.pip/pip.conf
COPY requirements.txt /tmp
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

#RUN pip3 install conda==4.3.13 conda-build==2.1.5

# 安装 AI 相关的大型软件包
# torch 1.0 以下推荐安装 0.4.1。
RUN pip3 install torch==0.4.1 torchvision==0.2.1
RUN pip3 install mxnet==1.5.0
#tensorflow-gpu 版本必须小于等于 1.5，否则无法在 DL580-G7 docker 上运行，因为硬件不支持 AVX 指令
RUN pip3 install tensorflow==1.5 \
    tensorflow-estimator==1.14.0rc1 \
    tensorlayer==2.1.0 \
    tensorpack==0.9.5

# app 相关安装配置

COPY ./app /app
# or RUN git clone https://abc.com/app.git
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app/app/"

# 其他补充 py 软件包
RUN apt-get update && apt-get install -y curl net-tools libevent-dev file \
    strace gdb \
    && apt-get clean

# 其他补充系统软件包
RUN pip3 install supervisor eventlet redis huey \
    && mkdir -p /var/log/supervisor
COPY misc/sv_gunicorn.conf /etc/supervisor/supervisord.conf

# 安装 DFI 所需的 lutorpy 软件包（注意：由于某些所需的 git 扩展包已失效，导致编译失败，故此注释掉）
# 必须先注释掉 install.sh 中的几个 torch 扩展包才能编译通过。之后通过 luarocks 再安装。
#RUN git clone https://github.com/torch/distro.git ~/torch --recursive \
#    && cd ~/torch && ./clean.sh \
#    && sed -i 's/sudo //' install-deps && bash ./install-deps \
#    && sed -i '135s/^/#/' install.sh && sed -i '136s/^/#/' install.sh \
#    && sed -i '144s/^/#/' install.sh && sed -i '145s/^/#/' install.sh \
#    && sed -i '153s/^/#/' install.sh && ./install.sh -b \
#    && /root/torch/install/bin/luarocks install cutorch \
#    && /root/torch/install/bin/luarocks install cunn \
#    && /root/torch/install/bin/luarocks install cudnn \
#    && pip3 install git+https://github.com/imodpasteur/lutorpy.git
# 如果直接使用 luarocks install 失败，可以尝试离线安装：
# git clone https://github.com/soumith/cudnn.torch -b R5
# cd cudnn.torch && luarocks make

RUN cd .. \
    && wget -c https://developer.download.nvidia.cn/compute/machine-learning/repos/ubuntu1404/x86_64/libcudnn5_5.1.10-1+cuda8.0_amd64.deb && dpkg -i libcudnn5_5.1.10-1+cuda8.0_amd64.deb \
    && wget -c https://developer.download.nvidia.cn/compute/machine-learning/repos/ubuntu1404/x86_64/libcudnn5-dev_5.1.10-1+cuda8.0_amd64.deb && dpkg -i libcudnn5-dev_5.1.10-1+cuda8.0_amd64.deb

RUN echo 'Docker built OK!'

# 对外端口及启动程序设置
EXPOSE 5000

# 其他补充设置
# 1. DFI
RUN mkdir -p /root/.torch/models \
    && ln -sf /app/app/engine_v1/models_release/deep_feat_interp/vgg19g-4aff041b.pth /root/.torch/models/vgg19g-4aff041b.pth
# 2. 其他补充
RUN pip3 install execnet Authlib flask_limiter face-alignment
#RUN mkdir -p /root/.face_alignment/data && ln -s /app/app/engine_v1/models_release/face_alignment/2DFAN-4.pth.tar /root/.face_alignment/data/2DFAN-4.pth.tar

#CMD ["/bin/bash"]
#CMD ["gunicorn", "--bind", ":5000", "--workers", "3", "--reload", "server:app"]
CMD ["/usr/local/bin/supervisord"]
