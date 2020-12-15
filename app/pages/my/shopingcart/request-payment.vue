<template>
  <view class="page-section">
    <text class="ts-h3">支付金额</text>
    <view class="price">
      <text class="rmbLogo">￥</text><text class="ts-h1 ts-text-red">{{displayAmount}}</text></view>
    <view class="btn-area">
      <!-- #ifdef MP-WEIXIN -->
      <button type="primary" disabled="true">微信支付</button>
      <!-- #endif -->
      <!-- #ifdef APP-PLUS -->
      <button v-for="(item,index) in providerList" :key="index" type="primary" @tap="requestPayment(item,index)"
        :loading="item.loading">{{item.name}}支付</button>
      <!-- #endif -->
    </view>
  </view>
</template>
<script>
  export default {
    data() {
      return {
        providerList: [],
        amount: 1, //支付金额，单位分
      }
    },
    computed: {
      displayAmount() {
        return this.amount / 100; //支付金额单位转换位元显示
      }
    },
    onLoad: function({
      amount
    }) {
      // console.log(JSON.stringify(options))
      this.amount = amount;
      // #ifdef MP-WEIXIN
      uni.showModal({
        content: "小程序支付正在申请中...",
        showCancel: false
      })
      return;
      uni.requestPayment({
        timeStamp: '',
        nonceStr: '',
        package: '',
        signType: 'MD5',
        paySign: '',
        success: function(res) {
          console.log('success:' + JSON.stringify(res));
        },
        fail: function(err) {
          console.log('fail:' + JSON.stringify(err));
        }
      });
      // #endif
      // #ifdef APP-PLUS
      uni.getProvider({
        service: "payment",
        success: (e) => {
          console.log("payment success", e);
          this.providerList = e.provider.map((value) => {
            switch (value) {
              case 'alipay':
                return {
                  name: '支付宝',
                  id: value,
                  loading: false
                }
              case 'wxpay':
                return {
                  name: '微信',
                  id: value,
                  loading: false
                }
            }
          })
        },
        fail: (e) => {
          console.log("获取登录通道失败", e);
        }
      });
      // #endif
    },
    methods: {
      async requestPayment(e, index) {
        this.providerList[index].loading = true;
        let orderInfo = await this.getOrderInfo(e.id);
        console.log("得到订单信息", orderInfo);
        if (orderInfo.statusCode !== 200) {
          console.log("获得订单信息失败", orderInfo);
          uni.showModal({
            content: "获得订单信息失败",
            showCancel: false
          })
          return;
        }
        uni.requestPayment({
          provider: e.id,
          orderInfo: orderInfo.data,
          success: (e) => {
            console.log("success", e);
            uni.showToast({
              title: "感谢您的赞助!"
            })
            //通知支付成功，删除购物车数据
            this.$store.dispatch('buy')
          },
          fail: (e) => {
            console.log("fail", e);
            uni.showModal({
              content: "支付失败,原因为: " + e.errMsg,
              showCancel: false
            })
          },
          complete: () => {
            this.providerList[index].loading = false;
          }
        })
      },
      getOrderInfo(e) {
        let appid = uni.os.plus ? plus.runtime.appid : "";
        let url = 'https://demo.dcloud.net.cn/payment/?payid=' + e + '&appid=' + appid + '&total=0.01';
        return new Promise((res) => {
          uni.request({
            url: url,
            success: (result) => {
              res(result);
            },
            fail: (e) => {
              res(e);
            }
          })
        })
      }
    },
    components: {}
  }
</script>
<style>
  .page-section {
    display: flex;
    flex: 1;
    flex-direction: column;
    margin-top: 100upx;
    justify-content: flex-start;
    align-items: center;
  }

  .price {
    margin-top: 30upx;
    margin-bottom: 25upx;
    position: relative;
    line-height: 1;
  }

  .rmbLogo {
    position: absolute;
    font-size: 40upx;
    top: 8upx;
    left: -40upx;
  }

  .btn-area {
    margin-top: 50upx;
    margin-bottom: 50upx;
    display: flex;
    flex: 1;
    flex-direction: column;
  }

  button {
    margin-top: 10upx;
    margin-bottom: 10upx;
    width: 710upx;
  }
</style>
