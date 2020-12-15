# FaceMagi 项目计划<!-- omit in toc -->

该项目为一款基于 App/Server 架构的照片修改艺术化软件。

- [1.项目概述](#1.项目概述)
- [2.任务清单](#2.任务清单)
- [3.竞品网评](#3.竞品网评)

## 1.项目概述

本项目的目标是在 [Flask] 上部署多个深度学习 [Deep Learning] 模型作为微服务。这些模型用于执行以人像为主的照片艺术处理，模型提前在 [Jupyter Notebook] 上训练好。[REST API] 用于与部署的模型通信。例如，发送要处理的图像并将生成的结果返回给客户机。

软件要实现的功能特性，主要参考了 Facetify, FaceApp 和 美颜相机 三款 App，取其中最受欢迎的功能点。
除了此之外，也参考了 [PhotoLab](https://photolab.me)。

A. 竞品对比表：

  > |     | Facetify       | FaceApp         | 美颜相机              | FaceMagi v1     |
  > | --- | -------------: | :-------------: | -------------------- | --------------- |
  > | 收费 | 收费订阅自动续期 | 收费订阅、自动续期 | 免费，页内广告、周边服务 | Yes             |
  > | 特色 | 换性、年龄      | 换性、年龄、排版   | 超清、美颜、美妆       | 换性、年龄、创意   |
  > | 界面 | 操作繁琐、不直观 | 操作顺手、功能清晰 | 操作流畅、拍照为主      | 操作顺手、功能清晰 |
  > | 美颜 | 丰富           | 较少（AI美颜为主） | 最丰富                | 丰富            |
  > | 美妆 | 丰富           | 较少（AI美妆为主） | 最丰富                | 丰富            |
  > | 滤镜 | 较少           | 丰富             | 最丰富                | 无              |
  > | 创意 | 丰富           | 丰富             | 一般                  | 丰富            |
  > | AI应用 | 多           | 多              | 一般                  | 多              |

B. 本应用规划实现功能：

- 美颜：【主要】瘦脸?、瘦身?、磨皮、微雕、祛斑、肤色、去黑眼圈、美牙等
- 美妆：【主要】美瞳、修眉
- 滤镜：【次要】经典常用滤镜，最好能本地执行
- 创意：【重点】变更胡子、发型、眼镜、种族，更换照片背景、风格等

这些功能均以 AI 实现为主，包括美颜美妆，以及变更性别、年龄、打扮，还有卡通化、照片风格、艺术创意等。

## 2.任务清单

- 一、技术预研：基本完成。

  - 主要事项：前后端程序框架、AI 技术选型、AI 模型训练和验证、docker 化验证、GPU 应用验证等。
  - 基本结论：
    - 设计功能特性对标 FaceApp，虽可实现但效果有差距、且耗用资源较多。
    - 故权衡效果与资源，采纳部分特性实现；同时补充卡通、风格转换等以作市场差异化。
    - 后续版本可以考虑逐渐补齐短板。
  - 本项目定义输出的标准图片大小为 400x500。
    - AI引擎模型支持的处理和输出大小推荐为 x384~x512，最低不低于 x256。
    - 若AI引擎处理图片大小低于 x384，则需要对图片做缩放或超解析处理。

- 二、产品开发：

  - [-] 1、前端开发：
    - [-] 功能特性：
      - [*] 用户身份：
        - [*] 自动用户注册：启动时检查用户登录状态，非用户则自动注册。
          - 用户名根据设备自动生成，如果有 AppleId 则与账号绑定。
        - [*] 用户登录，访问鉴权
      - [-] 图像处理（参考 FaceApp 界面）：
        - [*] EDITOR：大图，秒级处理，有免费有收费
        - [*] ART：大图，秒级处理，有免费有收费
        - [*] FUN：小图，快速处理，可分享，带广告
        - [ ] LAYOUTS：风格画册，可选（V2 版本考虑）
        - [*] 对当前图片的已处理结果做缓存，再次点击时直接使用；换图片时清除。
      - [-] 其他功能：
        - [*] 应用设置
        - [*] 社交分享（facebook/instgram/?? 参考竞品）
        - [*] 应用内购买：in-app purchases 支持
          - [*] 前端内购代码集成
        - [ ] 外部广告
        - [*] 下载和分享按钮迁移到图片范围内，且只在处理完毕后显示
        - [*] ！！配置中关闭使用 v3 版本编译器！原因：该编译器对自定义控件支持有问题，真机上 tap 事件不传递
        - [ ] TODO: demo 图片不检查是否有 vip 权限
        - [-] iphone 11 及 ipad 等发布必须机型界面调试
          - [*] iPhone 8/6s（4.9英寸屏以下）
          - [*] iPhone 8 Plus（5.5英寸屏）
          - [*] iPhone 11 Pro MAX（6.5英寸屏）
          - [ ] iPad Pro 2 代（12.9英寸屏）
          - [*] iPad Pro 3 代（12.9英寸屏）
    - [ ] 安全相关：
      - [ ] TODO: 日志清理：去除敏感信息
      - [ ] TODO: 代码检视：清理存在漏洞的代码

  - [-] 2、后端开发：
    - [-] 核心功能：
      - [-] Editor：照片级人脸特征修改
        - 计划支持特征列表（v1，具体与 FaceApp 功能对齐）：
          - smiles: 暂无 or ELEGANT
          - impression、age: AttGan + FLB（DFI 也可，但速度慢）
          - *beards*: FLB、AttGAN、ELEGANT 或 STGAN 支持
          - hair colors: AttGAN、ELEGANT 或 STGAN 支持
          - hair styles: AttGAN、ELEGANT 或 STGAN 支持
          - glasses: AttGAN、ELEGANT 或 STGAN 支持
          - *makeup*: BeautyGAN、FaceMakeup
        - 技术参考：
          - FaceApp 所支持的编辑功能列表：
            - 男性：
              - smiles: classic, wide, tight, upset
              - impression: holywood 1/2/3, wave 1/2
              - age: old, cool old, young 1/2
              - *beards*: hipster, full beard, goatee, mustache, shaved, grand goatee, lion, petite goatee
              - hair colors: black, blond, brown, red, tinted
              - hair styles: bangs 1/2, long, side swept, straight bangs, hitman, wavy, straight
              - glasses: glasses, sunglasses
              - *makeup*: makeup 1/2/3/4, matte, glossy, dark, bright, dark matte, dark glossy, bright matte, bright glossy
              - filters: 滤镜
              - lens blur: 对焦
              - background: 背景
              - overlay: 光斑
              - tatto: 纹身
              - vignette: 暗角
              - adjustments: 明暗、对比
              - crop: 裁剪
            - 女性：
              - smiles: 子项同男性，下面也是
              - impression
              - age
              - *makeup*
              - hair colors
              - hair styles
              - glasses
              - *beards*
              - 后面项同上述男性
          - CelebA 数据集支持特征列表（DFI 可编辑共计 50 个）：
            '5_o_Clock_Shadow', # 刚长出的双颊胡须
            'Arched_Eyebrows', # 柳叶眉
            'Bags_Under_Eyes', # 眼袋
            'Bald', # 秃头
            'Bangs', # 刘海
            'Big_Lips', # 大嘴唇
            'Big_Nose', # 大鼻子
            'Black_Hair', # 黑发
            'Blond_Hair', # 金发
            'Brown_Hair', # 棕发
            'Bushy_Eyebrows', # 浓眉
            'Eyeglasses', # 眼镜
            'Goatee', # 山羊胡子
            'Gray_Hair', # 灰发或白发
            'Heavy_Makeup', # 浓妆
            'Male', # 男性
            'Mouth_Slightly_Open', # 微微张开嘴巴
            'Mustache', # 胡子，髭
            'Narrow_Eyes', # 细长的眼睛
            'No_Beard', # 无胡子
            'Pale_Skin', # 苍白的皮肤
            'Pointy_Nose', # 尖鼻子
            'Receding_Hairline', # 发际线后移
            'Sideburns', # 连鬓胡子
            'Smiling', # 微笑
            'Straight_Hair', # 直发
            'Wavy_Hair', # 卷发
            'Wearing_Lipstick', # 涂了唇膏
            'Young', # 年轻人
            'asian', # 亚洲人
            'baby', # 婴儿
            'black', # 黑人
            'brown_eyes', # 褐色眼睛
            'child', # 小孩
            'eyes_open', # 眼睛张开
            'frowning', # 皱眉
            'fully_visible_forehead', # 前额完全可见
            'indian', # 印度人
            'middle_aged', # 中年人
            'mouth_closed', # 嘴巴闭合
            'mouth_wide_open', # 嘴巴大开
            'no_eyewear', # 没戴眼镜
            'obstructed_forehead', # 前额被阻碍
            'partially_visible_forehead', # 前额部分可见
            'senior', # 年长
            'shiny_skin', # 闪亮的皮肤
            'strong_nose_mouth_lines', # 强的鼻子嘴线
            'sunglasses', # 太阳镜
            'teeth_not_visible', # 牙齿不可见
            'white' # 白人
          - FLB 预训练模型已支持特征（5 个，基本上都是组合特征）：
            - facehair.pth # 面毛
            - feminization.pth # 女性化
            - masculinization.pth # 男性化
            - older.pth # 更年老
            - younger.pth # 更年轻
          - AttGAN-PyTorch x384 预训练模型所支持的特性为（13 个）：
            Bald, Bangs, Black_Hair, Blond_Hair, Brown_Hair, Bushy_Eyebrows, Eyeglasses, Male, Mouth_Slightly_Open, Mustache, No_Beard, Pale_Skin, Young
        - [-] 其他产品化特性：
          - [ ] 基于 FaceMakeup 实现头饰、纹身等（中式、日式、印式、EGirl等）
          - [-] 基于 BeautyGAN 实现分类美妆风格（只能应用到目标人脸的色调和唇色，不能应用眼影、纹饰等细节）
            - [ ] TODO: 有一种基于人脸掩码对齐移植的美妆方法，可以迁移人脸细节（v2 实现）
          - [*] 基于 ArbitraryStyleTransfer 精选适合风格
          - [*] 每个 esgan 占用~1.4G显存，放到独立进程中，采用进程间通讯
          - [ ] TODO: 产品化 BeautyGAN 模型尺寸需升级为 x384以上（v2 实现）
            - 当前为 x256，补充采用了超解析，但图像质量仍不够好
      - [*] Art：
        - [*] 卡通：Ugati、CartoonGAN
        - [*] 风格迁移：ArbitraryStyleTransfer、FacePreservingStyleTransfer
      - [*] Fun：从上述功能中摘选部分，生成小图（240x300）且加水印
      - [-] 用户身份认证：用户登录，访问鉴权
        - [*] v1 版本使用基于 Flask-HTTPAuth 和自定义算法的简单用户权限管理。v2 再考虑改进。
        - [*] 所有需要消耗资源的 API，客户端访问时需要先做用户权限校验。
        - [*] 设备登录管理：根据设备指纹自动注册和登录，采用基于时间戳的自定义校验算法。各后端服务器支持。
        - [ ] TODO: 用户信息管理：包括购买信息、级别及有效期等。由单独云主机提供提供（从后端服务器访问 V2）。
      - [-] 自动续费内购
        - v1 版本仅需支持苹果内购支付。v2 版再考虑小程序及安卓平台。
        - [*] 使用 iphone 6s 真机和新注册登记用户进行支付测试（官方要求）
        - [ ] 基于 Bluehost 实现苹果内购通知服务（非必须？js 或 php、python 待定，可参考相关开源项目）
      - [-] 其他功能：
        - [*] 代码重构，AI 相关结构迁移到 api_v1 下
        - [-] 图像相关自定义处理函数库，分别基于 PIL 及 cv2（V2 版本统一到 cv2 上）
        - [*] 更换四张 demo 图片，改为 4:5 的高清 AI 生成人脸图
        - [ ] ipad 上有些处理结果图，图像质量太差，想办法改进
          - [ ] TODO: arbitrary_style_transfer 里的有些图片不合适，换为风格鲜明的图片。
          - [ ] TODO: beautyGAN 目前只支持 x256，需升级为 x384。
          - [ ] TODO: 增加 photo2cartoon。
          - 后续版本只使用照片级模型或功能。
    - [-] 运维相关：
      - [*] 日志输出
      - [ ] 出错告警
      - [ ] 状态统计
      - [ ] 降级处理
    - [-] 安全相关：
      - [ ] 管理代码如数据库操作等，从 docker 中剥离
      - [ ] docker 中包含 AI 模型等必须资源，不对 docker 外目录进行写操作（生产环境下）

  - [-] 3、测试开发：
    - [-] 单元测试
    - [*] 系统测试
    - [ ] 性能及压力测试
    - [ ] 可靠性验证

  - [-] 4、性能优化：
    - [*] Gunicorn 使用异步工作进程。（v1版本）
    - [*] 后端重构，web 服务与 AI 服务做成共享任务队列方式，参考 pyxqueue。
    - [*] 工作引擎多进程并行处理，确保任务并发时尽快处理完成。
    - [*] DEMO 图片处理缓存化，若有缓存则直接返回，否则先处理再缓存。（v1版本）
    - [ ] 如果设备空闲，则将用户当前菜单中其他的免费功能提前处理，以便快速返回。（v2版本）
    - [ ] 面部特征提取从基于 caffe 的 face_attribute_fan 改为基于 torch 实现。（已实现？）
    - [ ] 使用 https 代替 http 以实现更高的安全性。（v2版本）
    - [ ] !!! TODO: 付费用户任务优先！
    - [*] 服务器地址启动时动态获取。
    - [ ] 打包前，将 4 张 demo 图片的每个功能，都在真机或模拟器上手工执行一次，以便生成缓存

- 三、运营部署

  - [-] 产品部署：
    - [-] 相关域名网站注册及配置：
      - [*] 注册 facemagi.com
      - [*] 基本配置索引（完成）及用户购买信息（v2）服务部署到上述域名
      - [ ] 修改网站首页，指向应用商店下载地址
    - [*] 后端服务部署到 amazon 海外云
      - [*] 服务器实例：
        - [*] 申请[美东区竞价实例](https://us-east-2.console.aws.amazon.com/ec2/v2/home)：
          机型：g4dn.2xlarge（16G 显存。这是最低需求，最好升级为 24G）
          系统：Deep Learning AMI (Ubuntu 16.04) Version 27.0 (ami-06a75cf9d3bbf4cd9)
          SSH密钥文件：ssh-key-facemagi.pem
          DNS：ec2-3-21-206-140.us-east-2.compute.amazonaws.com
        - [*] 上述实例的分区大小默认为 100G（已用约90G），需进入卷管理，将其扩展为 200G。
        - [*] 登录系统，安装和设置 nvidia-docker2（Deep Learning AMI 已自带）
          - 修改 /etc/docker/daemon.json 设置 "default-runtime": "nvidia"
          - 重启 docker 服务：sudo systemctl restart docker
          - 执行 nvidia-docker run nvidia/cuda:9.0-cudnn7-devel-ubuntu16.04 nvidia-smi 应正常输出
        - 修改安全组规则，允许外网访问 8087 端口
      - [-] 应用部署：
        - 1、采用镜像方式部署
          - 1.1、导出开发服务器上的 docker 镜像和容器到文件：
            docker export backend_py_web_1 > ./backend_py_web.tar
            单独导出镜像（可选）：docker save -o ./backend_py_web_img.tar backend_py_web:latest
          - 1.2、上传上述两文件以及源码 backend_py.tgz 和模型 models_release.tar
            - 购买了[半个月奶牛快传账号](https://d.amoyxm.com/38.html)，直接高速上传 15G 大文件
              用户名：yue123y@foxmail.com 密码：amoyxm.com [官网](ttps://cowtransfer.com)
            - 源码通过 bluehost 主机中转，其他挂奶牛快传
            - 上传完毕后，解压 backend_py.tgz 和 models_release.tar 到 ~/facemagi-docker
          - 1.3、导入镜像和容器文件：（购入或者构建选一即可，推荐构建）
            docker import - backend_py_web_1 < backend_py_web_img.tar
            单独导入镜像（可选）：docker load --input ./backend_py_web_img.tar
        - [*] 2、或采用源码部署（在线构建镜像和容器）：（在 amazon aws 上测试很快）
          - 修改 Dockerfile 将前几行中的使用国内源的两行注释掉
          - 修改 docker-compose.yml 将 web 容器的 command 注释掉
          - 执行 docker-compose build web 开始构建镜像和容器
            - 需要先重新安装 py2 的 pyopenssl 包：

              ```shell
              ls -l /usr/lib/python2.7/dist-packages/ | grep -i ssl
              #drwxr-xr-x  3 root root   4096 Jan  9 09:23 OpenSSL
              #drwxr-xr-x  2 root root   4096 Jan  9 09:23 pyOpenSSL-0.15.1.egg-info

              sudo rm -rf /usr/lib/python2.7/dist-packages/OpenSSL
              sudo rm -rf /usr/lib/python2.7/dist-packages/pyOpenSSL-0.15.1.egg-info

              sudo pip2 install pyopenssl --target=/usr/local/lib/python2.7/dist-packages

              ls -l /usr/local/lib/python2.7/dist-packages/ |grep -i ssl
              ```

        - [*] 3、执行 run_docker.sh 完成所需各 docker 容器初始化及启动加载
        - [*] 4、容器数据库初始化：
          - 首先创建数据库：登录 docker 控制台，执行：
            apt install mysql-client
            /app/create_database.sh
          - 更新生成数据表：执行 /app/db_upgrade.sh。
        - [*] 5、修改 config.py 配置，与服务器硬件的 cpu 核数、内存大小以及显存大小适配
          - 查看 docker ps 根据需要将 backend_py_mysql_1 替换为 backendpy_mysql_1
        - [*] 6、重新加载 docker 各容器
          - 添加开机自启动：插入到 /etc/rc.local 文件末尾的 exit 0 之前：
            cd /home/ubuntu/facemagi-docker/backend_py && ./run_docker.sh 2>&1 &
          - 手工调试：新开一个 screen，执行 run_docker.sh
        - [*] 7、修改 [配置索引文件](http://facemagi.com/config/base.cfg) 指向上述实例域名或 IP
        - [-] 8、预发布测试
          - [*] 从互联网使用浏览器访问该主机地址，应能看到返回的信息（Haribol!）
          - [*] 使用手机 app 进行真实场景测试（demo 及自拍图片，每个功能组都测试至少一次）
          - [*] 查看运行日志，可以直接查看 app/app/logs/engine_info.log 或 flask_info.log
          - 若想保存 docker 容器内容变更
            docker commit -m "updated cache images" -a "zzz" f0d3a5f4e81d backendpy_web
            docker inspect backendpy_web_1 #查看容器配置
        - 主机系统优化：最低显存 16G；内存最低 16G（需手工开启 swap 支持）
    - [-] APP 提交发布：
      - [*] 使用正式版本证书重新打生产包。
      - [*] 为了避免审核测试时并发过多导致访问失败，需临时关闭服务端 media.py 中的接口访问限制
      - [*] 审批完成后，根据商店链接更新 app 设置页面，以及官网首页。
      - [*] 完成 alpha 测试后择时上线。
      - [*] 初版发布后，添加自动订阅支付功能，测试完善后做二次发布。
      - [*] ugati 运行时若显存不够会报错并且进程挂死无法恢复：降低模型处理尺寸予以规避。

  - [ ] 产品运维：
    - [ ] TODO: 在各大社交平台注册产品账号，定期发布和互动。
    - [ ] TODO: 监控系统前后端运行情况：数据统计、状态图示、异常处理、趋势预测。
    - [ ] 上线后的修正与改进：
      - [ ] TODO: 改进超解析算法，增加去噪算法（denoise）。
      - [ ] TODO: !!! 启动时清除所有图片缓存。

## 3. 竞品网评

- FaceApp 评测（19年7月版）
  - 主要功能：笑容、印象、年龄、胡子、发色、发型、眼镜、打扮、滤镜、调焦、背景、刺青、边框、对齐、裁剪，这些功能动态加载、顺序排开，每个功能都可点进去引用或取消，其中的高级功能收费。
  - 产品试用：
    - 在武汉上传图片大约 50 秒，处理等待时间大约 2~30 秒。上传照片的速度比较慢，但上传一次就可以进行各种操作。
    - 另外，貌似初次试用上传较快，再次试用就很慢，针对新用户有优化？
    - 图片效果不错，返回的图片可以选择应用还是取消。对处理过的图片有本地缓存，同样操作会直接应用。
    - 年龄等约 1/3 的效果是免费的。根据上传的人像特征如性别，会显示不同的功能按钮。
  - 项目背景：FaceApp 为俄罗斯团队开发，7月发布版效果有大提升。网上流传效果图主要有体育、影视、政经明星的年龄、性别、表情图。用户上传图片在服务器上保留 48 小时。
  - 据[运营派文章](https://www.yunyingpai.com/product-operation/547509.html)分析：
    - 两年来，FaceApp也在不断的通过社交广告投放，测试各种功能是否有传播性。虽然FaceApp有28种功能，但真正火过的只有3种（年龄、发型、胡子？），剩下25种都以失败告终。
