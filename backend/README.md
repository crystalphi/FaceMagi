# FaceMagi 设计说明<!-- omit in toc -->

该项目主要用到了 [Python], [REST], [Flask], [Pytorch], [NGINX] 和 [Docker]。

- [1.依赖项](#3.依赖项)
  - [python虚拟环境](#python虚拟环境)
- [2.代码库目录结构](#4.代码库目录结构)
- [3.系统架构](#5.系统架构)
- [4.使用指南](#6.使用指南)
- [5.测试指导](#7.测试指导)
- [6.技术预研](#8.技术预研)
- [7.运维部署](#7.运维部署)

## 1.依赖项

项目代码在以下依赖基础上进行了测试：

- [Python] (3.6.8): 一种用于通用程序设计的解释性高级程序设计语言。
- [Flask] (1.0.2): 基于 Werkzeug 和 Jinja 2 的意图良好的 [Python] 微框架。
- [Gunicorn] (19.9.0): 用于 UNIX 系统的 [Python] [WSGI] HTTP 服务器。
- [NGINX] (1.15.12): 一个免费的、开源的、高性能 HTTP 服务器，支持反向代理和 IMAP/POP3 代理服务。
- [Docker] (18.09.6-ce): 一个开放平台，供开发人员和系统管理员在笔记本电脑、数据中心虚拟机或云上构建、发布和运行分布式应用程序。
- [Docker-Compose] (1.24.0): 用于定义和运行多容器 [Docker] 应用程序的工具。
- [Keras] (2.2.4): 一种高级神经网络 [API]，用 [Python] 编写，能在 [Tensorflow]、cntk 或 theano 之上运行。
- [Tensorflow] (1.13.1): 一个开源的深度学习 [Deep Learning] 库，用于使用数据流图进行高性能数值计算。
- [Pytorch] (1.1.0): 一个具有强 GPU 加速的张量和动态神经网络。
- [Matplotlib] (3.0.3): 用于 [Python] 及其数字数学扩展 [NumPy] 的绘图库。
- [NumPy] (1.16.3): [Python] 的一个库，添加了对大型多维数组和矩阵的支持，以及对这些数组进行操作的大量高级数学函数集合。
- [scikit-image] (0.15.0): 使用 [Python] 进行图像处理的算法集合。
- [Conda] (4.6.14): 包含在 [Python] 数据科学平台 [Anaconda] 中的包和虚拟环境管理器。

### python虚拟环境

虚拟环境 (<env_name>=**env_facemagi_backend**) 可以从 **environment.yml** 文件生成。所需的 **requirements.txt** 也在本代码目录下。

可以使用[conda]命令配置虚拟环境：

```bash
~/backend_py$ conda env create -f environment.yml
~/backend_py$ conda activate env_facemagi_backend
(env_facemagi_backend)~/backend_py$
```

## 2.代码库目录结构

代码库主文件夹包含：

```bash
backend_py
├── .env.example
├── app
│   ├── app
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── model.py
│   │   ├── static
│   │   │   └── 4.jpg
│   │   └── templates
│   │       └── dlflask.html
│   ├── facemagi
│   │   ├── __init__.py
│   ├── config.py
│   ├── Makefile
│   ├── mnist_model.h5
│   ├── server.py
│   └── tests
│       ├── __init__.py
│       ├── conftest.py
│       └── test_app.py
├── dlflask36.yaml
├── docker-compose.yml
├── Dockerfile
├── nginx
│   └── conf.d
│       └── local.conf
├── README.md
└── requirements.txt
```

每个 AI 模块子目录里，使用一个文件 adapter.py 做封装，主要包括两部分内容：

- 封装 AI 模型的初始化
- 封装模型的方法为 flask 的 URL

## 3.系统架构

设计原则：尽量简单，扁平化，便于扩展。减少部署和维护工作量。

使用 [docker-compose] 创建的系统架构，使用了两个不同的 [Docker] 容器，分别用于：

- [NGINX]
- [Flask]、[Gunicorn]、[supervisord] 和各 AI 服务进程。

对用户上传的图片视频，v1版使用本地存储，v2使用云存储（S3服务）。

该系统架构图示如下：

```bash
            _______            __________________
           |       |          |                  |
Client<──> | NGINX ├<─bridge─>| Gunicorn + Flask | <─S3 API─> [ S3 services ]
           |       |          |              |   |
            ¯¯¯¯¯¯¯           |       各AI服务进程 |
                              |                  |
                              |   (supervisord)  |
                              |                  |
                               ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
```

- 客户端（App、小程序）通过 https 访问后端服务器。
- docker 之间使用桥接网络通信。
- AI 服务进程与 Flask 进程之间采用任务队列方式。可选的任务队列框架有：
  - [ztq](https://github.com/easydo-cn/ztq/)：较老，中文，但 py3 支持有问题（不建议）
  - [huey](https://github.com/coleifer/huey)：较新，稍复杂，支持任务优先级（推荐）
  - [mrq](https://github.com/pricingassistant/mrq)：较新，提供任务面板

### 3.1 费用计算

以用户量 100w 计算，每天 1/10 的人使用，每天上传 10 张图片，每张图片平均 1MB，保存期为 1 天。
假定每张图片平均请求 20 次操作，则平均每天上传 1TB 数据，请求服务 2000w 次。

- 云主机计费：
  - 若每天按 10 小时处理完，每台 AWS 每小时处理 1w 次，则需要 200 台。（TODO: 要做性能测试）
  - 若用户分配不是很均匀，假定 10 倍比例，则每台 AWS 所需图片存储为 50G。
  - 可考虑腾讯云主机，弗州 S3.3XLARGE24 12核 24GB 1.5Gbps 1152元/月。或香港的 GPU 云主机 ~￥8K/月。
  - 长远可考虑香港托管 GPU 主机。

- S3 数据存储计费（v2）：则平均每天 1000GB 的存储，所需费用为：
  - 存储费用：1000 x 0.023 = $23/月。删除免费。
  - 请求费用：1m / 1000 x 0.005 = $5/天（PUT），1m x 20 / 1000 x 0.0004 = $8/天（GET），总计 $400/月。
  - 传输费用：1000 x 20 x 0.01 USD（美东AWS） = $200/天，总计 $6000/月。

## 4.使用指南

使用 [docker-compose] 在 [Flask] 服务器上运行 [Deep Learning] 模型的步骤和命令描述如下。

> *在执行 [docker-compose] 之前，强烈建议关闭其他应用程序以释放资源和端口，以避免潜在问题。然后可以执行 [docker-compose] 来构建服务。*

```bash
~/backend_py$ docker-compose build
```

下一步是执行 [docker-compose] up 命令。

```bash
~/backend_py$ docker-compose up
```

如果到最后一切正常，看起来应该类似于：

```bash
...
...
web_1_9b6c64fc338e | Using TensorFlow backend.
```

## 5.测试指导

有不同的方法来检查服务器是否正常运行。一种方法是打开浏览器（如 Chrome 或 Mozilla）并粘贴以下URL：

```bash
http://127.0.0.1/
```

Web浏览器应显示文本 “Deep Learning on Flask”。

[REST API] 可以使用 [pytest] 或 [curl] 来进行测试。

可以使用 [Makefile] 从 [Flask] [Docker] 容器内部对用 [pytest] 创建的 [Flask] 微服务执行测试：

```bash
~/backend_py$ docker exec -it deeplearning_flask_web_1 /bin/bash
~/app# make test
...
test_app.py ..                                                         [100%]
```

使用 [Docker] 容器外部的 [curl] 进行的 POST 测试如下所示：

```bash
~/backend_py$ curl -F file=@app/app/static/4.jpg -X POST 'http://127.0.0.1/api/predictlabel'
{
  "most_probable_label": "4",
  "predictions": [
    {
      "label": "0",
      "probability": "5.870073e-09"
    },
    {
      "label": "1",
      "probability": "1.0881397e-06"
    }
  ],
  "success": true
}
```

## 6.技术预研

本项目在技术预研中主要参考的项目有：

- 一、AI技术：实现换性、年龄化、卡通化、风格美颜、艺术化等
    （以下测试均尽可能使用x384分辨率图片；性能数据均为使用CPU的情况。AI 框架以 PyTorch 为主。）

  - **1 人脸特征迁移系列**：调整性别、年龄、发色、发型、胡子、肤色等
    - Github 检索关键字：
      - Face / Facial [Attribute] Editing / Transfer / Manipulation
      - face gan
      - Deep Feature Interpolation
    - 产品化建议：
      - 输出图片标准大小为：400x500，演示图片大小为：240x300。
      - 尽量都使用 x384 模型。对于不支持 x384 的统一按 x256 训练和处理，然后在输出时做超解析扩展。
      - 对人脸检测、特征识别、分割、对齐、融合等大部分模型都会用到的处理，可以参考变脸项目将其通用化。
        - 融合研究 DFI 怎么做的？可以参考 digital-makeup 中的代码
        - 面部特征标注处理，可使用 01-FaceAttribute-FAN 或 DFI 等其他 torch 版本。

    - [**【产品 1-?】Facelet_Bank**](https://github.com/yingcong/Facelet_Bank)
      - 进展：测试较好，港大项目。torch 版本：0.3.1。数据集依赖于上述 DFI 项目。必须人脸对齐：否，支持CPU推理：是。有预训练模型。CPU 模式大约 ~1pic/40s-10m，GPU ~1pic/20s。
        - 其他特征模型可自行训练，依赖于 DFI 项目生成的特征矢量文件（使用 python2 + torch-0.3.1 + torchvision-0.2.1）。
        - 自训练模型处理性能：
          - 特征矢量生成：使用 DFI 生成每种上述特征的 3k 个 npz 矢量文件，在 G7 上约耗时 20h。
          - 特征模型训练：在 FaceletBank 中使用上面生成的矢量文件训练出 .pth 模型文件，在 G7 上约耗时 10h。
        - 预训练模型工作良好，但自训练的无效，原因待查。问题分析：训练不足？还是代码或数据问题？如果是代码问题是逻辑还是参数？已反馈作者，未回复。
          - 预训练基础上再训练保存后也无效，使用原始代码做训练和验证也一样无效。因为数据样本及数量不同？
          - 考虑到在 DFI 目录下 Demo 验证有效，问题多半在 FLB 这边，如果不是代码原因，则训练相关的可能性较大。
          - 将 DFI 中 attribute_vector 下的矢量样本，从 x512 改为 x448，验证结果类似。
      - 优点：
        - 图片质量及性能较好，支持多属性混合，泛化效果较好，支持多人脸。
        - **批量化处理时速度很快，12张高分图也只要~15秒**。
      - 缺点：
        - 自训练尚未验证通过。
        - 预训练模型仅支持 conda py3.5/3.6 & pytorch 0.3.1
      - 结论：
        - **根据目前分析情况，v1先使用预训练模型实现产品化，暂不做其他特征**。
        - 运行时所需显存：~2GB x 5（占用显存太多，可根据情况进行功能裁剪）
        - 方便时继续跟进训练失败原因。可增强其他创意类独特功能，以作差异化。
          - TODO: 使用 x256 进行训练，能否训练好？且在 2 天内完成？
        - 或可发展替代方案：
          - 其他 DFI 方案：暂无合适的其他 DFI 项目，具体情况参见下面相关 DFI 项目说明。

    - [**【产品 1-1】AttGAN-PyTorch**](https://github.com/elvisyjlin/AttGAN-PyTorch)：
      - 进展：测试尚可。torch 版本：0.4.1。必须人脸对齐：是，支持CPU推理：是。支持多属性混合，有x384高解析模型。对于样本外图片，需使用腾讯的 FaceAttribute-FAN 预先做特征标注，否则不理想。效果略差于 tf 版本，或许要更多训练。~1pic/5s。
        - Colab 训练验证：由于 GDrive 空间及 colab 内存限制，只使用 Celeba-HD 前 5w 张图，而且 batch_size 得设为 16 才能开始跑，最后仍然由于内存不足原因退出。
        - 本地训练：
          - 训练 x256 有效。显存约占用 8G。使用 CelebA-HQ  每个迭代GPU需要大约15分钟、CPU约35分钟，默认要训练200个迭代。随着训练次数的增加，其间进行验证可以看到生成的图片越来越清晰。
          - 训练 x384 无效。过程貌似正常，但输出模型测试无效。运行了25小时，可见到 loss 不断减少，但验证时只得到乱码图片，原因未知。同样参数，改为 x256 进行训练，几轮之后即可见部分效果。训练不足？或代码问题？
        - 训练 x512 失败，显存不够，可能要 32G 显存。且貌似代码中最高只能支持到 x512？
      - 优点：
        - 代码简洁规整，支持多 CPU/GPU 训练。性能较好，推理所需显存较少（<2GB）。
        - 训练 x384 模型，一个 epoch GPU需24分钟（CPU约54小时，）。减少 bs，所需显存可以明显降低。
      - 缺点：
        - 预训练模型工作尚可，但有部分纹理不自然现象。x384 模型也不能满足照片级要求，效果不及 FLB 和 DFI。
        - 只能处理正方形图片，之后要自行做图片融合，效果可能难理想，需研究融合算法。
      - 结论：
        - 自训练模型暂不满足要求。**可先使用 x384 预训练模型做产品化**。
        - 运行时所需显存：~3GB
        - 预训练模型支持 13 种特性：Bald, Bangs, Black_Hair, Blond_Hair, Brown_Hair, Bushy_Eyebrows, Eyeglasses, Male, Mouth_Slightly_Open, Mustache, No_Beard, Pale_Skin, Young
          - 其中 发色、刘海、嘴型、肤色 效果较好

    - [**STGAN-pytorch**](https://github.com/bluestyle97/STGAN-pytorch)
      - 进展：测试尚可。STGAN 非官方实现。代码简练规整。
        - 训练过程中会周期输出效果图，无需太长时间即有明显效果。尚未使用样本外图片单独测试。
        - 程序挑选特征图片集时考虑区分男女和眼镜类型，否则可能导致某些特征效果不明显。
        - 使用 x256 HQ数据集训练，一天可迭代 40w 次。
        - 使用 x384 HQ数据集训练：
          - 显存：其他默认参数，若设置 bs>2 或者 *_conv_dim>64，则显存不足。（有条件时再修改验证）
          - 耗时：单1080Ti，每2w次迭代写一次模型，耗时约40分钟。需训练至少 60w 迭代。
          - 结果：
            - bs设为2勉强可训练，显存几耗尽，训练批次也需更多才见效果。连续训练了4天，迭代次数为 42w/58w/68w/74w 的效果不错，越往后的越好。但刘海和眼镜效果不佳，胡子要到 50w 次以上才开始有效。
            - 样本外测试结果一般，胡子、肤色、年龄、性别效果较显著，刘海基本无效且图片有格纹，整体有不同程度偏色金发图片尤其显著。应与训练参数有关，可想办法改进，如增大 bs 和 *_conv_dim 等。
          - 总的来说，训练时间越长图片质量越好。建议训练时间最好 3 天以上。
        - 使用 x512 HQ数据集训练失败，显存不足（所需显存可能 24G 以上）。
        - 如果模型效果好，可考虑使用 DFI 中的特征识别器重新生成 70 特征标识文本，扩展功能。
      - 优点：
        - 容易训练，效果明显。
        - 代码质量较高。性能较好。~3s/pic GPU。
        - 支持多特征模型。
      - 缺点：产品化代码需要较多修改。
      - 结论：
        - 输出图片质量一般，部分有杂纹，不推荐产品化。金发、白肤色效果较好，若有必要也可考虑产品化。
        - 运行时所需显存：~5GB。性能较好：~3s/pic GPU。训练相对容易。
        - 自训练模型分析结论：
          - 与 AttGAN 和 ELEGANT 相比训练效果明显，且无图片畸形，但部分输出图细节有小方格。
            - 部分输出效果有明显的小方格阵列，训练不足时尤其明显，即使 80w 次训练模型部分输出图也有。
          - 不建议使用 x256 以上的图片集训练，代码中未见支持、测试结果也一般。
          - 以上为使用 HQ 图片数据集进行的训练，如需对比可恢复原始数据集再做验证。
          - x256 模型中比较好的迭代次数为：[94w]/79w/74w/70w/[59w]/54w/[53w]/51w/50w

    - [**【产品 1-?】mbu-content-tansfer**](https://github.com/rmokady/mbu-content-tansfer)
      - 进展：测试较好。基于掩码的人脸特征转换，代码参考 ContentDisentanglement 改进而来。
        - 训练 x256 需显存 5G，训练 x384 需显存 9G。1天可训练约 2w 次。
        - 自训练模型 x256 可行；x384 不佳，要么缺效果要么有杂纹，难以适用。
        - x256 训练 6~8k 次的模型较好，少了没效果，多了有杂质。
      - 优点：
        - 根据参考图片进行部分特征迁移，可玩性强。输出图片自然，清晰度也较高。
        - 图片处理中采用了语义分割和掩码技术，理论上图片质量和效果更好。
      - 缺点：
        - 对训练 1w 次以上模型做验证时经常发现有杂纹，x256、x384 都有。除了次数，与参考图片内容也有关系。
      - 结论：
        - **可以使用自训练 x256 模型提供部分 FUN 所需功能。或者结合超解析提供部分 Editor 功能。**
        - 运行时所需显存：~2GB。
        - 可根据参考图片应用不同风格的胡子、眼镜等。
        - 参考图片的选择对结果影响较大，产品化时需仔细挑选。（需同性别、同肤色，部位清晰）

    - [**HomoInterpGAN**](https://github.com/yingcong/HomoInterpGAN)
      - 进展：测试尚可。与上面的 Facelet_Bank 是同一作者，最近新开发项目。必须人脸对齐：？，支持CPU推理：?。
        - 可根据参考图修改 嘴型、胡子、肤色、刘海、发色等，输出自然、细腻。
        - 已修改代码只用 HD 图片做训练。修改了 loss.py 的 classification_loss_list 函数中的一行代码。
          - 训练方法：训练时可使用x512分辨率的HD数据集，将 ./data/attributeDataset.py 中的4处 scale=(xxx, x) 替换为不同分辨率，即可训练出支持指定分辨率图片的模型。
          - 完成 x256 训练需 100w~150w 个迭代，每 10w 迭代耗时约 8 小时。
        - 嘴型和其他放在一起貌似不太好训练
          - 到 130w 迭代为止，早期发色好、后期嘴型好、刘海一般。分开训练是否更合适？
      - 优点：
        - 根据参考图片进行特征迁移，可玩性强。输入图片人脸无需严格对齐。
        - 训练所需显存较少：x256 最低只需 ~3G 显存，x384 约为 5G，x496 约为 7G。
        - 一个模型可支持多个特征，但每个训练模型只能输入固定分辨率图片。
      - 缺点：
        - 训练：预训练模型只支持处理 x128 分辨率人脸对齐图片。若要支持高解析图片，则需使用同等解析度数据集做训练。
          - 使用 x512 数据集长时间训练后效果仍不佳，可能训练不足也可能模型有限制。
            - 但从训练过程中产生的图片看，处理效果和质量都比较不错。是否用法不对？
          - 训练所需的计算量很大，x256 需训练至少几天。
        - 推理：处理后的图片虽然光滑，但细节处略模糊，在可以接受范围内。
          - *处理时消耗的显存较多*。x256 所需显存：~4GB。x384 所需动态显存会超过 10G，导致处理失败。
      - 结论：
        - 实测效果并不出众，用法及功能上与 BeautyGAN 类似。后者效果更明显。
        - 预训练模型支持的分辨率过低，不适合产品应用。功能上可以被 BeautyGAN 替代。
        - **暂不产品化。可继续研究高分辨率模型训练及应用，若效果超过 BeautyGan 则可替换。**

    - [**MGPE**](https://github.com/cientgu/Mask_Guided_Portrait_Editing)
      - 进展：基本测试尚可。必须人脸对齐：是，支持CPU推理：是。有预训练模型。代码规整，便于训练和集成。
        - 由于没有合适的生成 mask 和 label的工具，样本外验证尚未进行。
      - 优点：
        - 从介绍看效果比较优秀，各种特征迁移自然。
        - 处理性能很好，平均每张图片不到 1s。
      - 缺点：
        - 缺乏合适的 mask 生成工具，不便于样本外或商业使用。
          - 作者说用到了论文 "Face Parsing with RoI Tanh-Warping" 所涉及的人脸解析方法，相关参考代码及数据（貌似尚未完善）： <https://github.com/Eskender-B/roi-tanh> / <https://github.com/JPlin/Relabeled-HELEN-Dataset>
          - 论文中所列的 mask 工具为 JDA face detector，没找到。作则提供了一个 win 版的非商用工具。
          - FIXME: 用 CariFaceParsing/Segmentation 替代 JDA，可以直接生成彩色和黑白掩码图。但加入该软件生成的测试图片和掩码图后，测试时报cuda设备级错误。图片大小及格式都一致，应该是图片内容导致，具体原因未知。
          - 另外 CelebAMask-HQ/face_parsing/utils.py 中的代码也可生成彩色和黑白掩码图，或许可参考。
        - 项目文档相当简单，很多步骤缺乏说明。
      - 结论：
        - 效果及性能较好，但由于工具缺乏目前难以使用样本外图片验证。**暂不适合产品化，可进一步研究**。
        - 可能代码硬编码支持 x256 分辨率，更高分辨率未验证。

    - [*ContentDisentanglement*](https://github.com/oripress/ContentDisentanglement.git)
      - 进展：测试中。每个特征都需单独训练，无预训练模型。
        - 图片处理时，参考图除了修改特征外，其他特征应与原图一致，否则效果会受影响。
      - 优点：
        - 根据参考图片进行迁移，如眼镜太阳镜，从介绍看效果很好。可扩展性强。
        - 代码很规范，训练所需显存较低，x384 约需 7G。x512 约需 13G。
        - 支持多卡训练，支持连续训练。
      - 缺点：
        - 模型处理效果对目标图片的人脸位置和朝向要求高。
        - FIXME: 输出图片有点模糊，部分失真。如需 x384 照片级可用，可能必须修改模型代码进行支持。
        - 模型训练不易，需花费较长时间：
          - 一个可用特征模型大约需要迭代 4~7w 次，单卡约 1 天。迭代更多效果会变差，过拟合?。
          - 据 [第三方改进版](https://github.com/kozistr/improved-ContentDisentanglement) 所述：
            - 训练一个模型需要迭代 ~80w 次（1080Ti 单卡约需11天）
      - 结论：
        - 由于当前无预训练模型，模型训练不易，且需修改代码支持 x384 清晰度。故：
          - 第一版暂不产品化，后续版本继续投入跟进。
        - 如果 mbu-content-tansfer 效果可以，则不必采用本项目。

    - [*RelGAN-PyTorch*](https://github.com/elvisyjlin/RelGAN-PyTorch)：修改面部 40 特征
      - 进展：测试尚可。必须人脸对齐：是，支持CPU推理：是。支持多属性混合，无预训练模型。对于样本外图片，需使用腾讯的 FaceAttribute-FAN 预先做特征标注，可能更好。官方还有 keras 版本。~1pic/xs。
        - 本地训练：
          - 训练 x256 有效。显存约占用 10G。使用 CelebA-HQ + GPU 训练 2k 步用时 2h。若要达到网页效果则需要训练 4w 步（约2~3天）。随着训练次数的增加，其间进行验证可以看到生成图片的效果越来越明显。
          - 训练 x256 中第 49k/64k/68k 这几步，图片质量较好。在发色修改和女性化上效果较好，其他效果不显著。
          - 训练 x384 尚未进行。
      - 优点：
        - AttGAN-PyTorch 的进化版本，同一作者开发。
        - 支持高解析图片输出。
      - 缺点：
        - 从网页 keras 版测试结果看，还是有部分纹理不自然现象存在。
        - 属于GAN类型，比较难以训练好。
      - 结论：
        - 从网页测试图片看，性别、胡子、肤色效果较好，其他的图片效果一般，部分仍有失真。
        - 无预训练模型，自训练模型仅有发色修改和女性化较好，验证结果与网页图片一致。
        - **价值不大，先不产品化。**

    - [**ELEGANT**](https://github.com/Prinsphield/ELEGANT)
      - 进展：测试尚可。北大支持项目。必须人脸对齐：是，支持CPU推理：否。无预训练模型，代码改进自 DNA-GAN。从介绍看效果不错，发型和胡子迁移自然。代码规整，便于训练和集成。
        - 训练 4k 步即可看到明显效果，大约 1s 一步。单若要图片质量高训练次数也需要足够多（如 34000）。
        - 训练所需显存约7.4G，可同时训练多于2个属性，不明显增加显存大小（尚未验证输出模型的各属性是否都有效）
      - 优点：
        - 训练和推理速度都比较快，对显存要求不大。
        - **根据参考图进行迁移，可玩性较好**。
        - 支持多特征模型，增加特征数量需要更多训练时间，所需显存无明显增加。
      - 缺点：
        - 预处理代码内置为 x256 解析率，修改代码支持 x384 以上未完成（已恢复原貌，代码未保留）。
        - 一定要使用对齐截取后的人脸图片，才有较好效果。
        - FIXME: *部分图片有畸形，即使训练 3w 次以上偶尔也存在*。(缺陷)
      - 结论：
        - 根据参考图迁移，可玩性及自主可控性好。可能适合产品化，需进一步研究。

    - [StarGAN_v2-Tensorflow](https://github.com/taki0112/StarGAN_v2-Tensorflow)
      - 目前只有介绍，没有代码。展示的效果非常好。

    - [**deepfeatinterp**](https://github.com/paulu/deepfeatinterp)
      - 进展：测试较好，康莱尔大学研究项目。GPL，可封装为后台服务。
        - 原代码依赖于 lutorpy，只支持 py2。现已将 facemodel 从 lutorpy t7 转换为 pytorch pth，实现了对 py3 的支持，功能测试正常。
        - 正负样本数对时间几无影响，50足以，多了反倒有点模糊。
        - 图片大小、迭代次数及处理强度，对处理耗时影响较大。
      - 优点：
        - 60 多种可编辑特征，输出效果较自然，图片质量高。
        - 支持高分辨率图像，尺寸可自适应。（从部分输出图来看，其实也是将修改后图片原角度粘贴回去，只是效果较好）
        - 使用 CPU 和 GPU 性能差不多（对于400x500，分别为35s和37s），可以将 GPU 空出来做其他事务。
      - 缺点：
        - 照片级输出图片所需处理时间一般要到 20s 以上。运行时占用显存也较多。
        - 通过调整参数为 K=15,iter=50 耗时可控制在 15s 内，但输出质量大幅下降。
        - 代码太乱，需要大重构。去掉 caffe 和不相关代码，简洁清晰化。
      - 结论：
        - **可以生成较好的效果，但需要较长处理时间。性能未达标前暂不适合产品化。**。
        - 优化思路：
          - 1、选择合理图片大小和处理参数。（基本完成：400x500 or 200x250?，迭代 150 次等）
          - 2、目前为进程间通讯方式，可优化。（已完成）
          - 3、使用低分辨率（x256）模型，然后做超解析，处理时间能否减少？（已完成，比较有限）
          - 4、TODO: 对于相同基片的处理，人脸检测等操作只执行一次，结果缓存。(低优先。耗时不多)
            - alignface 和 facemodel 中都加载了 dlib 人脸识别库，可合并。
            - 可使用 DFI 中的特征识别算法替代框架所用基于 Caffe 的腾讯算法，且支持特征更多。
          - 5、TODO: 处理图片执行到 PF=model.mean_F 时，会从硬盘读取某些其他图片，效率较低。预加载到内存？
          - 6、TODO: 使用脸部组件掩码图合成，提升处理图片质量。
    - [*新版DFI*](https://github.com/rhedges14/Deep_Feature_Interpolation.git)
      测试一般。DFI 方式实现人脸特征迁移的另一个实现。TF 框架。代码清晰，说明详细。
      - 进展：基本功能验证通过。快速模式验证失败，生成中间文件尺寸较大，暂不支持高分辨率。
        1、已进行到第 6 步，可以使用 DFI 脚本正常处理单张图片；但 第 7 步的 Fast DFI 有代码报错，原因未知。
        2、当前代码支持的图片分辨率为 176x220，*经测试暂不支持其他分辨率*；
        3、生成的图片特征 h5 文件过大，9k 张图片，占用 40G（需清理!!）。
      - 结论：
        - 目前代码不支持高分辨率图，暂不适合产品化。

    - [**SDIT**](https://github.com/yaxingwang/SDIT)
      测试尚可。StarGAN 的改进版，Torch 框架。必须人脸对齐：是，支持CPU推理：?。代码比较规整，可以继续研究。
      目前只支持 x128 训练，更高尺寸会报 size 不匹配错，需较多修改。
      从下载脚本看提供了支持 x256 的预训练模型，但验证时报尺寸不匹配。
      - [训练高分率模型的技巧](https://github.com/yaxingwang/SDIT/issues/1)：尝试 256px 得到一个预训练模型 (step1), 然后增加解析率到 512px 并进行微调 (step2). 最后基于 step2 的模型训练 1024px 图片。
    - [chainer-dfi](https://github.com/dsanno/chainer-dfi)
      测试一般。只能直接根据特性选择图片集，然后训练和输出目标图。处理时间过长，不适合产品化。
    - [*STGAN*](https://github.com/csmliu/STGAN)
      测试一般。TF 框架。必须人脸对齐：是，支持CPU推理：?。由百度和哈工大开发，从介绍看比 AttGAN 更好，实测样本外不理想。代码结构与 AttGAN-PyTorch 类似，需较多修改。只有x128低解析度预训练模型。~1pic/5s。
    - [*GDWCT*](https://github.com/WonwoongCho/GDWCT)
      测试一般。必须人脸对齐：是，支持CPU推理：是。大部分没效果，普适性不佳（或测试方式不对？）。文档简单，有预训练模型，从介绍看效果不错。每个特性都需要单独训练。代码简洁，应易于集成。cpu 模式性能较低，大约 ~1pic/40s。
    - [StarGAN](https://github.com/yunjey/StarGAN)
      测试一般。官方实现 torch 版。加载缓慢，会循环执行逐渐给出更好的结果。
    - [StarGAN-Tensorflow](https://github.com/taki0112/StarGAN-Tensorflow)
      测试一般，可以直接处理样本外数据。只有 x128 低解析度预训练模型，可尝试高解析度训练。~1pic/1s。
    - [Sparsely-Grouped-GAN](https://github.com/zhangqianhui/Sparsely-Grouped-GAN)
      未测试。Python2 TF 版。无预训练模型。从介绍看貌似比 StarGAN 和 ResidualGAN 都要好一点。
    - [AttGAN-Tensorflow](https://github.com/LynnHo/AttGAN-Tensorflow)
      测试尚可。有x384高解析模型，测试效果好一些，但仍存在纹理不自然的问题，可以尝试更多训练。样本外不理想，但使用腾讯的 FaceAttribute-FAN 对图片做特征标注后，效果就好多了。代码较繁琐，不利于产品化。~1pic/6s。
    - [Residual_Image_Learning_GAN](https://github.com/zhangqianhui/Residual_Image_Learning_GAN)
      未测试，无预训练模型。TF 版。使用了残差图方法，从介绍看主要用在换性别上，效果可能好于 StarGAN。

    - [transparent_latent_gan](https://github.com/SummitKwan/transparent_latent_gan)
      未完成本地测试。潜在空间人脸编辑，GAN 2019 新进展。非特征迁移，而是人脸生成。只能运行在 GPU 上。在 kaggle 上测试 OK，效果很好，但部分场景如带眼镜有时怪异。提供x1024高分预训练模型，依赖于 nvidia 的 PGGAN 预训练模型，该模型非免费。
    - [InterFaceGAN](https://github.com/ShenYujun/InterFaceGAN)
      未测试，无预训练模型。潜在空间人脸编辑，功能与上一项目类似。未见对样本外数据进行处理。

  - **2 BeautyGAN**：美颜、美妆

    - [**【产品 2-1】BeautyGAN**](https://github.com/Honlan/BeautyGAN)
      测试尚可。基于 TF 框架，代码简洁，已集成到服务端。部分图片口红部分渲染过大，可尝试更多训练或更高分辨率能否解决问题。
      - 结论：
        - 满足产品化需求。**可以仔细挑选不同参考图片，生成不同效果，可玩性好。**
        - CPU 模式：运行时所需显存 0GB；速度 1p/5s；初次启动加载时间较长。
    - [**【产品 2-2】face-makeup.PyTorch**](https://github.com/zllrunning/face-makeup.PyTorch)
      测试尚可。有预训练模型。直接根据人脸地图修改头发或嘴唇等部位颜色，正面大脸效果不错，侧脸或小脸则不佳。
      必需用GPU，运行所需显存：~1G。图片尺寸任意正方形，x1024最佳。
      需要 torch==0.4.1.post2，numpy==1.15.0。~1pic/30s。
    - [*BeautyGAN_pytorch*](https://github.com/wtjiang98/BeautyGAN_pytorch.git)
      尚未测试。BeautyGAN torch 版官方实现。文档过于简单，缺少数据集使用说明，暂无法进行训练。
    - [**【产品 2-？】digital-makeup**](https://github.com/wen-kou/digital-makeup)
      未测试。使用的是人脸解析合并的方式。基于 cv2，代码全面、规整，有 GUI。
      从介绍看效果较自然、明显，有较高参考价值。*后续版本可考虑整合到数字美妆功能中*。
    - [*BeautyGAN-using-web-camra*](https://github.com/sakurayamaki/Generating-makeup-image-with-BeautyGAN-using-web-camra)
      测试一般，效果有限，有时不自然。基于 BeautyGAN，直接根据输入图片风格进行上妆，可应用于图片或视频。在性能及产品化集成方面有优势。
    - [beautyGAN-tf-Implement](https://github.com/baldFemale/beautyGAN-tf-Implement)
      测试无输出。文档不充分，代码修改较多，运行较慢。
    - [MakeupEmbeddingGAN-tf-Implement](https://github.com/baldFemale/MakeupEmbeddingGAN-tf-Implement)
      未测试。无预训练模型，从介绍看与BeautyGAN效果差不多。

  - **3 通用风格迁移**：画风迁移、创意、艺术
    - [***【产品 3-1】face-preserving-style-transfer***](https://github.com/zfergus/face-preserving-style-transfer)
      测试较好，6种预训练风格模型。可直接处理大图，画质较高。每个新增风格都需使用 COCO2017 数据集进行训练。
      运行所需显存：~0.8G。~1pic/3s。
    - [**【产品 3-2】arbitrary_style_transfer**](https://github.com/elleryqueenhomels/arbitrary_style_transfer)
      测试尚可。根据参考图处理，可玩性好。大图可直接应用，输出质量主要取决于风格图片。
      适合线条清晰、色调鲜明的风格，不适合暗色系及照片、油画类风格。
      新增风格直接使用参考图片，无需另外训练，图片尺寸不限、最好为高清。
      运行所需显存：~?G，~1pic/?s。CPU 模式：~1pic/8s。处理速度与风格图片大小也有关。
      **推荐使用该模式（每种风格一个进程，风格预先加载？）**
    - [**MetaStyle**](https://github.com/WellyZhang/MetaStyle)
      测试较好，输出图风格鲜明。属于元风格迁移，平衡了速度、灵活性和品质。基于 torch 实现。
      每个新增风格都需要使用 COCO & WikiArt 数据集单独训练，需大量时间和显存。
      *目前只有一个预训练风格模型发布，暂不适合产品化*。~1pic/5s。
    - [*universal-style-transfer-pytorch*](https://github.com/jfilter/universal-style-transfer-pytorch)
      测试一般。输出图线条僵硬，适合大图，小图效果不佳。运行所需显存：~3G。~1pic/5s。
    - [WCT-TF](https://github.com/eridgd/WCT-TF)
      测试一般。效果不如上面的。~1pic/10s。
    - [PytorchWCT](https://github.com/sunshineatnoon/PytorchWCT)
      未测试。为上述 universal-style-transfer-pytorch 项目的原型，效果应略低。
    - [WCT2](https://github.com/clovaai/WCT2)
      未测试。上述算法改进版。
    - [Real-Time-Arbitrary-Style-Transfer-AdaIN-TensorFlow](https://github.com/MingtaoGuo/Real-Time-Arbitrary-Style-Transfer-AdaIN-TensorFlow)
      未测试。貌似不区分训练与测试模式，可能运行缓慢、不适合产品部署。
    - [*prisma_abu*](https://github.com/bbfamily/prisma_abu)
      未测试。根据特征图片直接进行迁移，适合做创意。有详尽代码讲解。
    - [adaptive-style-transfer](https://github.com/tensorlayer/adaptive-style-transfer)
      未测试。需要 Tensorflow 2.0 以上。

  - **4 卡通风格**：风格迁移
    - [**【产品 4-1】cartoonGAN**](https://github.com/latte0/cartoonGAN)
      测试效果较好。基于原始版本完善的 torch 版本，支持测试和训练。CPU 模式运行缓慢。
      运行所需显存：~3G。性能：~1pic/3s。*不同风格模型只能分别加载，消耗显存较多*。
    - [**【产品 4-2】UGATIT**](https://github.com/taki0112/UGATIT)
      测试较好。日式大眼漫画风效果。官方实现，TF 框架，有预训练模型。支持 x256 分辨率。
      运行所需显存：~1G。性能：~1pic/4s。CPU 模式可多进程处理，也是 ~1pic/4s。
      有个 light 版的预训练模型，效果较差不建议采用。
    - [**UGATIT-pytorch**](https://github.com/znxlwm/UGATIT-pytorch)
      未测试。同上，基于 torch 实现。无预训练模型，从 tf 模型转换失败。暂不考虑产品化。
    - [CartoonGAN-Tensorflow](https://github.com/taki0112/CartoonGAN-Tensorflow)
      未测试。无预训练模型。
    - [pytorch-CartoonGAN](https://github.com/znxlwm/pytorch-CartoonGAN)
      未测试。另一个 torch 版，无预训练模型。
    - [CartoonGAN-4731](https://github.com/manestay/CartoonGAN-4731)
      未测试。卡通视频生成，基于上面的 pytorch-CartoonGAN。
    - [WarpGAN](https://github.com/seasonSH/WarpGAN)
      未测试。夸张漫画风。

  - **5 素描生成**
    - [*【产品 5-?】APDrawingGAN*](https://github.com/yiranran/APDrawingGAN.git)
      测试较好，钢笔画风。清华项目。有预训练模型，处理效率高，直接处理 x512 图片。
      代码比较混乱，难以整合。数据集加载时依赖预先准备的人脸掩码图以及文本格式的人脸分割数据。
      运行所需显存：初始化~4G，处理时~1.2G。
    - [*Face-Sketch-Wild*](https://github.com/chaofengc/Face-Sketch-Wild)
      测试尚可，铅笔画风，没有上面清晰。预训练模型无法在 pytorch>0.3 时加载，修改代码后可以运行。
      运行所需显存：~5G，~1pic/1s。CPU 模式处理缓慢，~1pic/20s。消耗过多，不建议产品化。
    - [*pGAN*](https://github.com/hujiecpp/pGAN)
      测试未完成。MDAL 的改进版，从论文介绍看效果比较好，面部特征清晰。应仅次于 APDrawingGAN。
      有预训练模型，但名称与代码不一致且无文档说明，暂无法测试。测试图片需要做数据预处理，取得人像及脸部掩模。
    - [MDAL](https://github.com/hujiecpp/MDAL)
      未测试。无预训练模型。

  - **6 换脸应用**：各种创意，如婚纱试装等，部分也支持特征迁移
    - [**PRNet**](https://github.com/YadiraF/PRNet)
      测试尚可，但运行较慢。支持3D重建、换脸、换眼睛等。修改加上了 alpha 混合。~1pic/25s。
    - [FaceSwap](https://github.com/Aravind-Suresh/FaceSwap)
      测试一般。代码简洁，主要使用了 dlib 库和 opencv，效果比较粗糙。~1pic/3s。
    - [*【产品 6-？】face_morpher*](https://github.com/WeiJiHsiao/face_morpher)
      测试一般。代码简洁，相比于上面的 FaceSwap 增加了 alpha 混合，但不支持不同大小图片的自动处理。~1pic/3s。
    - [pytorch-prnet](https://github.com/liguohao96/pytorch-prnet)
      未测试。上述 PRNET 的另外实现，支持训练。
    - [photolab_hack](https://github.com/gasparian/photolab_hack)
      未测试。貌似代码不完整，缺少 points json 文件的生成方式。

  - *8 图片对图片转换*：根据输入图和风格图生成输出图，可玩性较高
    - [**【产品 8-？】DRIT**](https://github.com/HsinYingLee/DRIT)
      测试较好，有预训练模型。支持照片与油画、冬天与夏天互换。各种风格需单独训练模型，也可用做特征迁移。
      输出风格鲜明，但支持分辨率只能到 x256，是否产品化待验证。运行所需显存：~1.8G。
    - [*MDMM*](https://github.com/HsinYingLee/MDMM)
      未测试，有预训练模型。为同一作者在 DRIT 之前开发的。变换画风、季节等，也可用做特征迁移。
    - [*instagan*](https://github.com/sangwoomo/instagan)
      未测试。可用于换装如裤子改裙子等，每种风格需单独训练。
    - [FUNIT](https://github.com/pomelyu/FUNIT)
      未测试。无预训练模型。根据少量样本照片进行风格转换，比如变更种族等。
    - [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)
      未测试，有预训练模型。变换季节、画风、日夜，照片着色，每种风格单独训练。比较基础，直接用处不大。
    - [famos](https://github.com/zalandoresearch/famos)
      未测试，无预训练模型。以引导图片作为纹理，生成内容图的马赛克图片。可用于艺术化，功能单一。
    - [automated-deep-photo-style-transfer](https://github.com/Spenhouet/automated-deep-photo-style-transfer)
      测试不佳。支持自动图像语义切分。代码清晰，但貌似不区分训练与测试模式，运行缓慢，不适合产品部署。
    - [DeepPhotoStyle_pytorch](https://github.com/ray075hl/DeepPhotoStyle_pytorch)
      测试不佳。基本逻辑同上，原代码只针对GPU，较多修改后适用于CPU。不区分训练与测试模式，运行缓慢，不适合产品部署。支持自动的图像语义切分。
    - [Neural-Tools](https://github.com/ProGamerGov/Neural-Tools)
      测试一般。只迁移颜色，应用有限。
    - [Photorealistic-Style-Transfer](https://github.com/KushajveerSingh/Photorealistic-Style-Transfer)
      测试效果不错，但不支持快速处理，只能多次迭代。不适合产品使用。
    - [Neural-Style-Transfer](https://github.com/titu1994/Neural-Style-Transfer.git)
      未测试。从介绍看可达照片级效果，但不支持快速处理，只能多次迭代。不适合产品使用。
    - [deep-photo-styletransfer-tf](https://github.com/LouieYang/deep-photo-styletransfer-tf)
      未测试。从介绍看可达照片级效果，但不支持快速处理，只能多次迭代。不适合产品使用。
    - [artistic style transfer](https://github.com/Echoha/style-transfer.git)
      未测试，无文档说明，无预训练模型。基于残差网络的图片风格迁移，支持 x512。

  - 9 工具-人脸属性提取：主要用于人脸特征迁移等功能的前置处理上
    - [**FaceAttribute-FAN**](https://github.com/luanfujun/deep-painterly-harmonization)
      测试较好。腾讯优图出品，提供预训练模型。使用 caffe 实现，在 docker 上使用比较合适。
    - [mxnet-face](https://github.com/tornadomeet/mxnet-face)
      MacOS 上测试失败，可能 mxnet 版本问题等导致，代码较老。
    - [Facial_Attributes_MTL_Basiline](https://github.com/espectre/Facial_Attributes_MTL_Basiline)
      未测试，未提供预训练模型。基于 pytorch 实现，代码简洁易于集成。
    - [FaceAttributePrediction](https://github.com/DetionDX/FaceAttributePrediction)
      未测试，未提供预训练模型。基于 pytorch 实现。
    - [*face-attribute-prediction*](https://github.com/d-li14/face-attribute-prediction)
      未测试，未提供预训练模型。基于 pytorch 实现。

  - 10 工具-人脸分割（Face Parsing/Segmentation/Semantic）
    - [*CariFaceParsing*](https://github.com/ZJULearning/CariFaceParsing)
      从介绍看效果不错，但训练貌似稍复杂。有预训练模型，测试良好。优先研究采用。
    - [*face-parsing*](https://github.com/FlYWMe/face-parsing)
      中文项目，从介绍看效果不错，可满足需求。优先研究采用。
      有训练模型。也可以下载 helen 数据集自行训练。
    - [face-parsing.PyTorch](https://github.com/zllrunning/face-parsing.PyTorch)
      优点：能够区分头发和五官，直接生成分割图和掩码图
      缺点：如果人脸较小或者不正，则结果不理想，错误会较多
    - [CelebAMask-HQ](https://github.com/switchablenorms/CelebAMask-HQ.git)
      效果较好，但数据集限制非商用。

  - 11 工具-抠图
    - [**Deep-Image-Matting-v2**](https://github.com/foamliu/Deep-Image-Matting-v2.git)
      未测试，有预训练模型。DIM v1 算法的官方改进版，基于 pytorch 实现。重点研究。
    - [*pytorch-deep-image-mattin*](https://github.com/huochaitiantang/pytorch-deep-image-matting)
      未测试完，稍繁琐。DIM v1 的第三方 pytorch 实现。提供了预训练模型，仅支持 torch-0.3.1。
    - [Deep-Image-Matting](https://github.com/foamliu/Deep-Image-Matting)
      未测试。DFI v1 版，基于 Google 算法的 AI 自动抠图算法，基于 TensorFlow 。

  - 12 工具-面部装饰
    - [**【产品】supersaiyan**](https://github.com/pengfexue2/supersaiyan)
      未测试。添加超级赛亚人发型和电弧特效。基于人脸地图进行处理，代码简单，适合用于发型、纹身、眼镜、貌似等。
    - [*faceai*](https://github.com/vipstone/faceai)（）
      未测试。各种面部应用，如基于 dlib 的头饰面饰等。中文项目。

  - 13 工具-超解析
    - [**【产品】ESRGAN**](https://github.com/xinntao/ESRGAN)
      测试较好。有预训练模型，处理一张图片约0.3秒。
    - [*CARN_pytorch*](https://github.com/nmhkahn/CARN-pytorch)
      未测试。超解析，快速、轻量级。

  - 14 工具-人脸生成
    - [**chainer-stylegan**](https://github.com/pfnet-research/chainer-stylegan)
      测试较好。生成 x1024 高质量人脸图片。为避免版权纠纷，本项目中所用的公开人脸数据，原则上都是采用这里生成的。
    - [face_gan](https://github.com/seasonyc/face_gan)
      未测试完。各种人脸生成 GAN 的大集合。当前代码只支持固定大小图片，不支持自动缩放。
    - [GeoGAN](https://github.com/wdyin/GeoGAN.git)
      测试一般。复旦项目，非特征迁移，而是人脸生成?。必须人脸对齐：是，支持CPU推理：是。无预训练模型。支持 x1024 高清图，从介绍看效果很好。每个新增特征（如山羊胡子）都需要使用 CelebA-HQ 高清数据集单独训练。
      - 进展：部分图片效果不错，但存在大量变形的情况，x1024 的尚未验证。x256 可训练，x384 和 x512 均显存不足。
      - 优点：暂无。
      - 缺点：代码比较杂乱。
      - 结论：目前不适合产品化。

  - 15 其他工具
    - [glow](https://github.com/openai/glow)
      未测试。OpenAI 开发的基于流的 GAN，可以生成笑脸之类，貌似效果很好。可以研究。
    - [AttentionGAN](https://github.com/Ha0Tang/AttentionGAN)
      未测试。更改表情。

    - [*BeautyPredict*](https://github.com/ustcqidi/BeautyPredict)
      未测试。颜值评估。
    - [deep-painterly-harmonization](https://github.com/luanfujun/deep-painterly-harmonization)
      未测试。和谐添加。
    - [inpainting_gmcnn](https://github.com/shepnerd/inpainting_gmcnn)
      未测试。照片修复，去除不想要的部分等。
    - [DeOldify](https://github.com/jantic/DeOldify)
      未测试。照片着色。
    - [albumentations](https://github.com/albu/albumentations)
      快速图片处理工具集。

- 二、产品功能 - **美颜**：【主要】瘦脸、瘦身、磨皮、微雕、祛斑、肤色、黑眼圈、美牙

  - AI 方式：（关键词：face dlib opencv makeup）
    - AttGAN-PyTorch / STGAN
      如上所述。构造特定样本集进行训练。
    - BeautyGAN
      如上所述。构造特定样本集进行训练。
    - [Face-Thin-Auto](https://github.com/cytheria43/Face-Thin-Auto)
      基于 dlib 的瘦脸。用处不大。

  - JS 方式：
    - [腾讯AI](https://ai.qq.com/doc/ptuimgfilter.shtml)
      建议使用腾讯AI开放平台API。
    - [hash2face](https://github.com/LinXueyuanStdio/hash2face)
      使用 webdnn 和 gan 生成图像。非美颜，供参考。

- 三、产品功能 - **美妆**：基于 dlib/opencv 的特效合成，部分也可采用上述 AI 模型实现
  - 试妆：美瞳、修眉……
  - 特效：
    - 上述 faceai 中的头像合成和数字化妆。

- 四、产品功能 - 滤镜：经典常用滤镜，最好能本地执行（初始版本暂不实现）
  - [GPUImage.js](https://github.com/aza/GPUImage.js)
    仿 GPUImage，功能较简单。

- 五、产品功能 - **创意**：【重点】主要采用上述 AI 方式实现
  - 胡子、发型、眼镜、种族：

## 7. 运维部署

- 开发环境部署：
  - OS：Debian 9
  - 模型训练及部署测试设备为 DL580-G7，需补充 2 块 1080Ti 显卡，以及 500GB SSD。（后需扩容需要加IO板）。
- 生产环境部署：
  - OS：Debian 9 或 Ubuntu server 16.04
  - 需根据 GPU 数量确定 gunicorn 的 worker 进程数，修改到 server/backend_py/misc/sv_gunicorn.conf 文件中。分配给 docker 的内存大小也要相应调整 >= 4G * worker 进程数。
  - 云主机：
    - 初期可使用腾讯或亚马逊 p2.xlarge GPU 型主机（配备 12G 显存的 Tesla K80 显卡，4核 CPU，60G 内存，以及 500M 网速），最低每月 3000 人民币；如果选用 spot 无状态模式，则最低可到每小时 2 人民币，大约每月 1500 元。
    - 华为和阿里云最高支持16G显存。[腾讯云](https://cloud.tencent.com/document/product/560/8025)可支持到256GB，推荐。
      - 计算型 GN2：（仅限国内）
        实例规格 GPU(Tesla M40) GPU 显存 vCPU 内存 包年包月* 按量计费*
        GN2.7XLARGE48*  1颗 24GB 28核 48GB  2781元/月 7.91元/小时
        GN2.14XLARGE112 2颗 48GB 56核 112GB 5856元/月 16.78元/小时
      - 计算型 GN7：（仅限国内）
        实例规格 GPU(NVIDIA T4) GPU显存 vCPU 内存 包年包月* 按量计费*
        GN7.2XLARGE32 1颗 Tesla T4 16GB 8 32 2500元/月 8.68元/小时
      - 计算型 GN10X：（仅限国内）
        实例规格 GPU(Tesla V100-NVLINK-32G) GPU 显存 vCPU 内存 包年包月* 按量计费*
        GN10X.LARGE20 1/2颗 16GB 4核 20GB 2595元/月 9.02元/小时
        GN10X.2XLARGE40 1颗 32GB 8核 40GB 5190元/月 18.02元/小时
    - 也可以考虑采用竞价实例，大多数情况是同规格按量计费模式的 10% - 20%。
      - 适用于大数据计算、采用负载均衡的在线服务和网站服务等场景
      - 实例可能会因为资源库存减少、其他用户出价竞争而发生系统主动回收实例的情况。
      - 腾讯云 *GPU计算型GN8*：（香港可用，P40 貌似都是 24G）
        机型 规格          GPU   vCPU   内存G   显存G  内网带宽  网络收发包  Linux计费
        GN8.LARGE56      1xP40    6     56     24  1.5Gbps  45万PPS    ￥3.1元/小时
      - AWS EC2 [GPU 竞价实例](https://aws.amazon.com/cn/ec2/instance-types/)：
        实例              GPU   vCPU   内存G   显存G  存储G  网络性能Gb    Linux计费
        g4dn.xlarge      1xT4     4     16     16    125    最高 25   $0.1578 每小时
        *g4dn.2xlarge*   1xT4     8     32     16    225    最高 25   $0.2256 每小时
        g4dn.4xlarge     1xT4    16     64     16    225    最高 25   $0.3612 每小时
        g4dn.8xlarge     1xT4    32    128     16  1x900    最高 50   $0.6528 每小时
        *g4dn.12xlarge*  4xT4    48    192     64  1x900    最高 50   $1.1736 每小时
        g4dn.metal       8xT4    96    384    128  2x900    最高 100  $1.3056 每小时
        p2.xlarge        1xK80    4     61     12    EBS    高        $0.302 每小时
        p2.8xlarge       8xK80   32    488     96    EBS    最高 10   $2.16  每小时
        p3.2xlarge       1xV100   8     61     16    EBS    最高 10   $0.998 每小时
        p3.8xlarge       4xV100  32    244     64    EBS    最高 10   $3.672 每小时
        p3.16xlarge      8xV100  64    488    128    EBS    最高 25   $7.344 每小时
    - 小结：
      - 竞价实例更划算。设计上要负载均衡化。
      - 腾讯云国外产品较少，适合国内用户或微信小程序。
      - AWS 适合国外用户或独立 App。g4 系列适合推理，扩展性好；p3 适合训练；p2 比较鸡肋。
      - TODO: 建议选择 AWS g4dn.2xlarge 竞价实例。每月花费约 ￥1500。可多台负载均衡（费用每月+￥200）。
- 共同：
  - 模型训练和生产环境需支持显卡，所以需要安装 nvidia-docker2，并且修改 /etc/docker/daemon.json 设置 "default-runtime": "nvidia"
  - 需安装 zsh，否则 docker-compose 中的容器名称对于下划线的处理可能不一致。

- 添加新人脸特征模型，操作步骤：
  1. 进入 07-DeepFeatInterp 目录，修改 demo2_facelet.py 添加新特征过滤条件；
  2. 修改并执行该目录下的 zzz_gen.sh 最后一行指令生成 3k 个左右的特征矢量文件；
  3. 回到 01-Facelet_Bank 目录，修改并执行 zzz_train.sh 脚本生成最终的 .pth 模型文件；
  4. 修改并执行该目录下的 zzz_run.sh，使用本地训练模型进行效果验证。

- 进入目录自动激活虚拟环境，步骤：
  A. 安装（只需做一次）：
    1, git clone https://github.com/inishchith/autoenv ~/.autoenv
    2, echo 'source ~/.autoenv/activate.sh' >> ~/.bashrc or ~/.zshrc
    3, echo 'AUTOENV_ENABLE_LEAVE=true' >> ~/.bashrc or ~/.zshrc
    4, 新开终端或者 source ~/.bashrc or ~/.zshrc
  B. 使用虚拟环境：
    1, 在项目目录下准备好 .env、.env.leave 两个文件，若没有按照格式创建
    2, 准备好指定名称的虚拟环境，如果没有则创建：
       conda env create -f environment.yml 或者：conda create -n ENV_NAME python=3.6
    3, cd 进入项目目录，自动激活指定虚拟环境
    4, 在该虚拟环境中进行安装软件包等 python 相关操作……，退出该目录时会自动取消激活
  C. 保存虚拟环境：
    1, conda env export --no-builds > environment.yml
    2, pip freeze > requirements.txt [可选]

- conda 虚拟环境更名方法：
  conda create --name new_name --clone old_namef
  conda remove --name old_name --all

[Python]: https://www.python.org/
[Flask]: http://flask.pocoo.org/
[Gunicorn]: https://gunicorn.org/
[WSGI]: https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface
[NGINX]: https://www.nginx.com/
[Docker]: https://www.docker.com/
[microservices]: https://en.wikipedia.org/wiki/Microservices
[REST]: https://en.wikipedia.org/wiki/Representational_state_transfer
[Docker-Compose]: https://github.com/docker/compose
[Conda]: https://conda.io/docs/index.html
[Anaconda]: https://www.anaconda.com/
[Jupyter Notebook]: http://jupyter.org/
[Deep Learning]: https://en.wikipedia.org/wiki/Deep_learning
[Keras]: https://keras.io/
[Tensorflow]: https://www.tensorflow.org/
[Matplotlib]: https://matplotlib.org/
[NumPy]: http://www.numpy.org/
[scikit-image]: https://scikit-image.org/
[curl]: https://curl.haxx.se/
[pytest]: https://docs.pytest.org/en/latest/
[Makefile]: https://en.wikipedia.org/wiki/Makefile
