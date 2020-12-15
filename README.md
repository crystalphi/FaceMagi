# FaceMagi 移动应用项目代码

FaceMagi 为一款基于 AI 技术的人脸编辑手机应用，类似于 FaceApp。

本项目为 iOS 商店 2020-2021 在售手机应用 FaceMagi 的前后端源码。

除了商业运营所需的一些文件如 AI 模型等之外，核心代码基本上都是完整的。
除此之外，商业运营所需的代码、资源、文件等可以有偿转让，具体见下述。

## [APP 链接](https://apps.apple.com/cn/app/facemagi/id1502256892)

  `https://apps.apple.com/cn/app/facemagi/id1502256892`

## APP 功能

1. 五种卡通风格转换
2. 三类数十种图片艺术风格转换
3. 多种头发颜色修改
4. 多种人脸妆容风格修改
5. 处理结果保存本地，调用社交应用进行在线分享
6. 已集成苹果应用内支付，支持自动续费订阅

## 技术架构

1. 采用C/S前后端系统应用架构
2. 前端技术实现
    - 主要编程语言：js
    - 使用 Uni-App 框架，包括自开发的滑动式多级图标菜单组件
    - 支持 IOS、安卓、微信小程序、支付宝小程序等多种平台（目- 前只调试和生成了 IOS 安装包）
    - 支持多国语言，自动切换
    - 支持应用内在线支付
3. 后端技术实现：
    - 主要编程语言：Python
    - 使用 nginx + Flask + docker 构建高可用后端服务
    - 使用异步处理架构，支持多请求并发
    - 支持 pytorch + tensorflow 等主流 AI 框架
    - 支持 AI 功能项的模块化扩展
    - 针对 demo 图片等的缓存及处理优化
    - 部署简便

## 转让范围

1. 苹果商店应用项目：FaceMagi
2. 网站域名：facemagi.com
3. 当前上架版本二进制文件：v1.0.8
4. 完整源代码：前端APP代码，后端服务代码，以及后端 AI 功能模块研究代码、资源等
5. 已租赁在线服务器：amazon 硅谷机房 GPU 服务器（21年中到期，可自行续租）

## 转让方式

- 源码出售：包括前端和后端完整源码，运行效果与在线版本一致。
- 源码买断：包括前端和后端完整源码，后端所有 AI 模块产品及研究代码，以及图标、测试素材等相关资源文件。买断后该代码归买家所有，卖家不再以任何方式出售相关代码。买断前已售的源码归原买家所有，不再追回。
- 整体转让：包括上述所有代码及资源文件的买断，Facemagi 苹果商店项目转让、facemagi.com 网站域名转让，以及 amazon 云服务器剩余时间使用权。

联系方式：vedasky（微信号，请注明 facemagi转让）

如果觉得项目对您有用，不妨打赏一下作者~
![avatar](images/wxds.jpg)
