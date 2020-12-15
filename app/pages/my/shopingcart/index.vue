<template>
  <view class="ts-flex ts-flex-item ts-column">
    <block v-if="count>0">
      <view class="ts-flex ts-flex-item ts-column">
        <view class="ts-list">
          <block v-for="(item,index) in cartList" :key="index">
            <view class="ts-list-cell">
              <checkbox-group @change="checkboxChange" :data-index="index">
                <view class="ts-media-list">
                  <view class="ts-media-list-checkbox">
                    <checkbox :checked="item.checked" />
                  </view>
                  <image class="ts-media-list-logo" :src="item.value.img"></image>
                  <view class="ts-media-list-body">
                    <view class="ts-media-list-text-top ts-ellipsis-2">{{item.value.title}}</view>
                    <view class="ts-media-list-text-bottom">
                      <view class="ts-flex ts-row ts-flex-item">
                        <text class="ts-h4 ts-text-red">￥{{item.value.price/100}}</text>
                        <text class="ts-h4 ts-text-discount ts-margin-left">￥{{item.value.origin_price/100}}</text>
                      </view>
                      <view class="ts-flex ts-row">
                        <!-- <number-box v-model="item.count" @increase="handleCount(index,1)" @reduce="handleCount(index,-1)"></number-box> -->
                        <view class="ts-numbox">
                          <view class="ts-numbox-minus" @click="handleCount(index,-1)">-</view>
                          <input class="ts-numbox-value ts-numbox-disabled" type="number" v-model="item.count" disabled>
                          <view class="ts-numbox-plus" @click="handleCount(index,1)">+</view>
                        </view>
                      </view>
                    </view>
                  </view>
                </view>
              </checkbox-group>
            </view>
          </block>
        </view>
        <view style="height: 100upx;">
          <!-- 保证底部操作栏目能够显示 -->
        </view>
      </view>
      <view class="cart-action-row">
        <view style="display: flex; flex:1; flex-direction: row; justify-content: space-between;">
          <view style="display: flex; align-items: center; padding-left: 20upx;">
            <checkbox-group @change="checkboxChangeAll">
              <checkbox :checked="checkAll" value="true" />
              <label class="ts-h6">全选</label>
            </checkbox-group>
          </view>
          <view style="display: flex; justify-content: flex-end; align-items: center;">
            <view style="display: flex; flex-direction: column; align-items: flex-end; justify-content:center;">
              <text style="color: #FF0000; font-size: 28upx; ">总计:￥{{costAll/100}}</text>
              <text style="color: #CCCCCC; font-size: 28upx;">共计:{{countAll}}件</text>
            </view>
            <!-- <button type="primary" style="margin-left: 20upx; border-radius:0upx;" @click="buy" :disabled="countAll==0">结算</button> -->
            <view class="ts-row" style="width: 200upx; height: 100upx; margin-left: 20upx;">
              <ts-button @tap="buy" :disabled="countAll==0" type="primary" :height="100">
                <text>去付款</text>
              </ts-button>
            </view>
          </view>
        </view>
      </view>
    </block>
    <block v-else>
      <view class="ts-flex ts-flex-item ts-column ts-center">
        <text>购物车啥都没有！</text>
      </view>
    </block>
  </view>
</template>
<script>
  import {
    mapState,
    mapMutations,
    mapActions
  } from 'vuex'
  // import tsButton from '@/components/teaset/components/ts-button.vue';
  import helper from '@/common/helper/index.js'
  export default {
    data() {
      return {
        checkAll: true
      }
    },
    methods: {
      handleCount: function (index, count) {
        if (count < 0 && this.cartList[index].count === 1) {
          uni.showModal({
            title: '提示',
            content: '确认要从购物车中删除该项目吗？',
            success: (res) => {
              if (res.confirm) {
                // console.log('用户点击确定');
                this.$store.commit('cart/deleteCart', this.cartList[index].product_id);
                return;
              } else if (res.cancel) {
                this.$store.commit('cart/editCartItemStatus', {
                  product_id: this.cartList[index].product_id,
                  checked: false
                });
                return;
              }
            }
          });
        } else {
          if (!this.cartList[index].checked) {
            this.$store.commit('cart/editCartItemStatus', {
              product_id: this.cartList[index].product_id,
              checked: true
            });
          }
          this.$store.commit('cart/editCartCount', {
            product_id: this.cartList[index].product_id,
            count: count,
          });
        }
      },
      checkboxChange: function (e) {
        // console.log(JSON.stringify(e.target))
        const index = e.target.dataset.index;
        this.$store.commit('cart/editCartItemStatus', {
          product_id: this.cartList[index].product_id
        });
      },
      checkboxChangeAll: function (e) {
        // console.log(JSON.stringify(e.target.value[0]))
        if (e.target.value[0]) {
          this.$store.commit('cart/editAllCartItemStatus', true);
          console.log('checked')
        } else {
          this.$store.commit('cart/editAllCartItemStatus', false);
          console.log('unchecked')
        }
      },
      buy() {
        uni.navigateTo({
          url: `request-payment?amount=${this.costAll}`
        })
      }
    },
    computed: {
      count() {
        return this.cartList.length;
      },
      cartList() {
        return this.$store.state.cart.cartList;
      },
      countAll() {
        let count = 0;
        if (!helper.isEmpty(this.cartList)) {
          this.cartList.forEach(item => {
            if (item.checked) {
              count += item.count;
            }
          });
        }
        return count;
      },
      costAll() {
        let cost = 0;
        if (!helper.isEmpty(this.cartList)) {
          this.cartList.forEach(item => {
            if (item.checked) {
              cost += item.count * item.value.price;
            }
          });
        }
        return cost;
      }
    },
    components: {
      // numberBox,
      // tsButton
    }
  }
</script>
<style>
  
  page {
    min-height: 100%;
  }
/*  page view {
    font-size: 32upx;
    display: flex;
    flex-direction: row;
  } */

  .cart-action-row {
    z-index: 1000;
    display: flex;
    flex: 1;
    flex-direction: row;
    position: fixed;
    justify-content: space-between;
    bottom: 0upx;
    left: 0upx;
    width: 100%;
    height: 100upx;
    background-color: #FFFFFF;
    border-top: #C8C7CC solid 1upx;
  }

  .ts-media-list-checkbox {
    display: flex;
    align-items: center;
  }

  .ts-media-list-logo {
    height: 150upx;
    width: 150upx;
    margin-right: 20upx;
  }

  .ts-media-list-body {
    height: 150upx;
  }

  .ts-media-list-text-top {
    font-size: 32upx;
    display: flex;
    flex: 1;
  }

  .ts-media-list-text-bottom {
    font-size: 32upx;
    align-items: center;
    justify-content: center;
  }

  .ts-numbox {
    display: flex;
    flex-direction: row;
    height: 50upx;
  }

  .ts-numbox-minus,
  .ts-numbox-plus {
    padding: 0upx;
    margin: 0upx;
    background-color: #f9f9f9;
    width: 50upx;
    line-height: 50upx;
    justify-content: center;
    /* color: #555555; */
    font-size: 50upx;
    border: 0upx;
  }

  .ts-numbox-value {
    border: 0upx;
    width: 100upx;
    font-size: 32upx;
    text-align: center;
  }

  .ts-numbox-disabled {
    /* color: #c0c0c0; */
    color: #000000;
  }
</style>
