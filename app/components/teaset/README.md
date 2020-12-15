# Teaset

## 项目介绍

- uni-app 是一个使用 Vue.js 开发跨平台应用的前端框架。
- 开发者通过编写 Vue.js 代码，uni-app 将其编译到iOS、Android、微信小程序等多个平台，保证其正确运行并达到优秀体验。
- uni-app 继承自 Vue.js，提供了完整的 Vue.js 开发体验。
- uni-app 组件规范和扩展api与微信小程序基本相同。
- 有一定 Vue.js 和微信小程序开发经验的开发者可快速上手 uni-app ，开发出兼容多端的应用。



**Teaset**是一个uniapp开源组件库，旨在推动uniapp的普及，收集整理社区常用的资源加工而成，欢迎收藏，fork,现在用于我们课题组的一个研发项目。

仓库地址：[https://gitee.com/zengqs/teaset](https://gitee.com/zengqs/teaset)

项目案例使用的数据源是本人打理的贝店的数据，各位亲多多支持下。贝店是一个类似于京东、天猫的购物平台，免费注册，首单送10元体验券。任何人都可申请成为店主，开店购物更实惠，每单返现。

我的贝店：[贺兰小铺](https://m.beidian.com/shop/shopkeeper.html?shop_id=682731)，店铺邀请码：**690638**。

开店指南：[http://beidian.zengqs.com](http://beidian.zengqs.com)


## 项目联系信息

1. 项目讨论QQ群:631951344
3. QQ:1024343803

## 主要贡献者

想加入团队，贡献自己的代码请联系项目负责人：qingsongzeng@163.com。

- [青伢子](mailto:qingsongzeng@163.com)，现供职于[广州番禺职业技术学院信息工程学院](http://www.gzpyp.edu.cn)


## 安装教程

1. 将components目录及子目录下的所有文件复制到你新建的项目中。

## 使用说明

1. 参考pages/example/teaset/文件，每一个组件有对应的案例的基础用法和高级案例。

* 仓库地址：https://gitee.com/zengqs/teaset
* 个人网站（网页服务暂时关闭，只提供API支持）：http://www.zengqs.com
* DEMO APP 下载地址：http://m3w.cn/teaset

## 教学资源

- [uni-app 官方文档](https://uniapp.dcloud.io)
- 课堂录像：[https://pan.baidu.com/s/1Ni5JxEt9pfY1tY7gu90J7A](https://pan.baidu.com/s/1Ni5JxEt9pfY1tY7gu90J7A), 密码：qf0i
- UNI-APP讲义：已在QQ群631951344发布PDF版本

## 测试环境

### 真机环境

** 系统 **
- 安卓系统：4,5,6,7,8
- 苹果IOS：11

** 机型 **
- 华为：Mate8，麦芒
- 小米：小米2，Max
- Apple：苹果4

### 模拟器

- iTool安卓模拟器
- 夜神模拟器
- 天天模拟器
- 微信小程序模拟器

### 云测平台
> 不定期提交云测平台做兼容性检测。我们免费提供测试服务（软件测试专业学生实践需要），提供专业测试报告，移动端支持云测平台的各种测试。

## 版本日志
### 2018年10月19日
- 增加失物招领应用模版（3个页面，使用Mockjs生成模拟数据，演示npm安装第三方包）
- 修复部分组件的错误
- 完整的教学案例代码：https://gitee.com/zengqs/uni-app-course 和视频录像可以参考百度云盘录像中的04-lost-found项目 [https://pan.baidu.com/s/1Ni5JxEt9pfY1tY7gu90J7A](https://pan.baidu.com/s/1Ni5JxEt9pfY1tY7gu90J7A), 密码：qf0i

### 2018年10月13日
- 修复部分组件的错误

### 2018年10月10日
- 修复tsSearchBar的错误
- 增加模版页面，演示Teaset组件的用法，增加echart组件的复杂用法案例
- 其它Bug

### 2018年10月9日
- 修复tsSegmentedControl的错误，增加v-model指令支持双向绑定当前激活的Tab

### 2018年10月8日
- 修复tsImageUploader文件增量选择的错误
- 增加tsScrollMessage滚动消息，支持横向与纵向显示，支持设置图标

### 2018年10月6日
- 增加tsImageUploader用于支持多文件选择上传

### 2018年10月5日
- 增加tsCityPicker组件，用于选择城市
- tsLeftCategory组件增加onReachBottom事件，用于上拉加载更多页面

### 2018年10月4日
- 增加ts-feedback-star组件，用于支持评级场景

### 2018年10月3日
- 修改长度单位为UPX，所有涉及到长度度量的单位统一使用UPX，之前的版本的代码需要做出相应调整，主要涉及到tsIcon、tsLeftCategory、tsBanner组件
- 修复tsIcon，增加默认尺寸，当没有指定type时不显示图标占位符
- 修复tsBadge显示高度问题

### 2018年10月2日
- 增加tsBadge组件


### 2018年10月1日
> 发布第一个版本