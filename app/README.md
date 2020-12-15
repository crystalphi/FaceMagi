项目说明
=======

## 功能特性

本应用功能主要参考“FaceApp”、“Facetify”和“美颜相机”这三款应用，以“FaceApp”为主，二八原则取其中最受欢迎的功能点。界面及操作风格主要对标 FaceApp。

除此之外，还参考了[PhotoLab](https://photolab.me)。详细对比表可参考后端程序代码的说明。

功能特性：笑容、印象、年龄、胡子、发色、发型、眼镜、打扮、滤镜、调焦、背景、刺青、边框、对齐、裁剪。这些功能动态加载、顺序排开，每个功能都可点进去引用或取消，其中的高级功能收费。

其中美颜采用 JS 方式：
  - [腾讯AI开放平台API](https://ai.qq.com/doc/ptuimgfilter.shtml)（推荐使用）
  - [GPUImage](https://github.com/aza/GPUImage.js)（功能较简单）

## 前端设计说明

- 客户端主要使用ColorUI及teaset组件库，目前测试支持安卓、IOS、微信小程序、手机浏览器、支付宝小程序、百度小程序
- 项目采用模块化设计，新增功能模块放在/pages/app/目录下，可以参考示例模块进行组织
- /pages/auth为登录注册页面目录
- /pages/home为首页
- /pages/my为用户中心
- /store/为Vuex实现的状态管理
- /common/api/为远程请求的API接口
- /common/request通过对Flyio封装实现远程访问

## 后端设计说明

- AI 相关后端服务使用 python 实现，flask 封装
- 其他后端服务如用户登录等有状态API，使用 thinkjs 等实现
- nginx 作为统一接口做负载转发

## 开发注意事项

- 系统使用Flyio实现远程API的请求，并通过拦截器自行注入登录安全访问机制，
  对于没有授权的API请求会自动拦截，对401错误会重定向到登录页面。
- 不要直接使用uni.request请求服务器的接口，项目对远程API的请求集中放在/common/api目录下，
  项目中只通过这个目录下的服务实现远程访问
- 为维护代码的一致性，PC端的远程访问也使用Flyio实现，没有采用axios，因为axios不支持uniapp在支付宝小程序中不能用。

## API访问需要修改common/request.js文件中的服务器地址

```
const config = {
	baseUrl: 'http://127.0.0.1:8360/api',
	uploadUrl: 'http://127.0.0.1:8360/api/image'
}
```

## 参考项目

- [高级图片处理库](https://github.com/image-js/image-js)
- [hash2face](https://github.com/LinXueyuanStdio/hash2face)（使用 webdnn 和 gan 生成图像）
