<template>
  <view class="content">
    <view class="top">

    </view>
    <view class="ts-column ts-center" style="margin-top: -150upx;">
      <view class="ts-row">
        <image class="logo" src="../../static/images/logo.png" mode=""></image>
      </view>
      <view class="ts-row">
        产教融合
      </view>
    </view>


    <view class="ts-flex ts-column ts-center">
      <!-- #ifdef APP-PLUS -->
      <view @tap="openLink()" @longtap="save">
        <qrcode :val="qrcodeLink" :size="qrsize" ref="qrcode"></qrcode>
      </view>
      <!-- #endif -->

      <!-- #ifndef APP-PLUS -->
      <view @tap="openLink()">
        <qrcode :val="qrcodeLink" :size="qrsize" ref="qrcode"></qrcode>
      </view>
      <!-- #endif -->

      <view><text>{{qrcodeLink}}</text></view>
      <view><text>邀请码：UVWROO</text></view>
    </view>

    <view class="ts-row ts-padding ts-flex-item">
      <!-- #ifdef APP-PLUS -->
      <ts-button class="ts-row ts-flex-item" @click="save" type="primary">保存二维码</ts-button>
      <!-- #endif -->
      <!-- #ifndef H5 -->
      <ts-button class="ts-row ts-flex-item" @click="sharurl" type="error">复制推广链接</ts-button>
      <!-- #endif -->
    </view>

    <view class="ts-row ts-flex-item  ts-center">
      <ts-share-buttons :providerList="providerList" :shareOptions="shareOptions"></ts-share-buttons>
    </view>


    <!-- #ifdef MP -->
    <view class="ts-row ts-flex-item">
      <button type="primary" size="default" open-type="share">分享</button>
    </view>
    <!-- #endif -->

    <view class="ts-column" style="padding-left: 100upx; line-height: 1.8em;">
      <text>1、好友识别二维码通过手机号进行注册</text>
      <text>2、也可分享此页面到微信或QQ邀请好友注册</text>
      <text>3、注册完成后您即可得到相应的积分</text>
    </view>

  </view>
</template>

<script>
  import Qrcode from '@/components/qrcode/qrcode.vue'
  import TsShareButtons from '@/components/teaset/components/ts-share/ts-share-buttons.vue'
  import {
    mapState,
    mapMutations,
    mapActions
  } from 'vuex'

  export default {
    components: {
      Qrcode,
      TsShareButtons
    },
    data() {
      return {
        inviterCode: 'UVWROO',

        qrcodeLink: 'http://www.zengqs.com/share?id=3228969',
        qrsize: uni.upx2px(300),

        // #ifdef APP-PLUS
        providerList: this.$providerList,

        shareOptions: {
          shareType: 0,
          shareImage: 'https://img-cdn-qiniu.dcloud.net.cn/uniapp/app/share-logo@3.png',
          shareTitle: '欢迎体验优职道',
          shareText: '专注在校学生的实习、就业，破解企业招工难题，提供精准就业、精准招聘服务！',
          shareLink: 'http://www.zengqs.com', //生成的二维码的链接，点解分享链接到改页面
          miniProgram: {
            id: 'wx86ab541f20e43dc4',
            path: '/pages/tabbar/home/index',
            webUrl: 'http://www.zengqs.com',
            type: 0
          },
        },
        // #endif

      }
    },
    computed: {
      ...mapState(['hasLogin']),
    },

    onLoad() {

      //必须延时，否则报错
      setTimeout(() => {
        this.$refs.qrcode.creatQrcode();
        // console.log(this.$refs.qrcode.img);

      }, 100)
    },

    methods: {
      // ...mapMutations(['logout']),
      // ...mapActions(['getUserInfo', 'logout']),
      ...mapActions({
        getUserInfo: 'user/getUserInfo',
        // logout: 'logout'
      }),
      //复制分享链接
      sharurl() {
        //#ifndef H5
        uni.setClipboardData({
          data: this.shareLink,
          success: function() {
            console.log('success');
            uni.showModal({
              title: '复制成功',
              content: '内容已复制到粘贴板，可前往其他应用粘贴查看。',
              showCancel: false,
              success: function(res) {
                if (res.confirm) {
                  //console.log('用户点击确定');
                } else if (res.cancel) {
                  //console.log('用户点击取消');
                }
              }
            });
          }
        });
        //#endif
      },
      //保存图片到相册  
      //#ifdef APP-PLUS
      save() {

        uni.showActionSheet({
          itemList: ['保存图片到相册'],
          success: () => {
            plus.gallery.save('https://img.cdn.aliyun.dcloud.net.cn/guide/uniapp/app_download.png', function() {
              uni.showToast({
                title: '保存成功',
                icon: 'none'
              });
            }, function() {
              uni.showToast({
                title: '保存失败，请重试！',
                icon: 'none'
              });
            });
          }
        });

      },
      //#endif

      openLink() {
        //#ifdef APP-PLUS
        plus.runtime.openWeb(this.shareOptions.shareLink)
        //#endif   

        // #ifdef H5
        window.location.href = this.shareOptions.shareLink;
        // #endif
      },

      chooseImage() {
        uni.chooseImage({
          count: 1,
          sourceType: ['album', 'camera'],
          sizeType: ['compressed', 'original'],
          success: (res) => {
            this.shareImage = res.tempFilePaths[0];
          }
        })
      },

    }
  }
</script>

<style>
  page {
    min-height: 100%;
  }

  view {
    line-height: 1.8em;
  }

  /*  view {
    border: #000000 solid 1px;
    padding: 10px;
  } */

  .content {
    display: flex;
    flex-direction: column;
    flex: 1;
  }


  .top {
    width: 100%;
    height: 300upx;
    background: url(http://pds.jyt123.com/wxtest/banner.png) no-repeat;
    background-size: 100%;
    background-position: center center;
  }

  .logo {
    width: 200upx;
    height: 200upx;
  }

  .qrcode {
    width: 300upx;
    height: 300upx;
  }

  .icon {
    width: 80upx;
    height: 80upx;
  }
</style>
