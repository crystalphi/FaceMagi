<template>
  <view class="ts-column ts-flex-item ts-padding" style="background-color: #f0f0f0;">
    <view class="ts-card ts-column" v-for="(address,index) in addressList" :key="index">
      <view class="ts-card-header">{{address.title}}
       <!-- <ts-badge :text="address.type" type="error"></ts-badge> -->
      </view>
      <view class="ts-card-content">
        <!-- <ts-list>
          <ts-list-item :title="address.name" :note="address.mobile"></ts-list-item>
        </ts-list> -->

        <view class="ts-list">
          <view class="ts-list-cell" hover-class="ts-list-cell-hover">
            <view class="ts-list-cell-navigate  ts-navigate-badge"> 姓名 <ts-badge :text="address.name" :inverted='false'
                type="error"></ts-badge>
            </view>
          </view>
          <view class="ts-list-cell" hover-class="ts-list-cell-hover">
            <view class="ts-list-cell-navigate  ts-navigate-badge"> 手机号码 <ts-badge :text="address.mobile" :inverted='false'
                type="error"></ts-badge>
            </view>
          </view>
        </view>
      </view>
      <view class="ts-card-footer">{{address.address}}</view>
    </view>
  </view>
</template>
<script>
  import api from '@/common/api'
  import {
    mapState,
    mapMutations,
    mapActions
  } from 'vuex'
  export default {
    data() {
      return {
        hasUserInfo: true,
        userInfo: {
          avatar: '../../static/photo.png',
          nickName: '用户名',
        },
        addressList: []
      };
    },
    computed: { ...mapState(['hasLogin'])
    },
    async onLoad() {
      if (this.hasLogin) {
        //必须先登录才能获取用户的信息
        this.userInfo = await this.getUserInfo();
        console.log(this.userInfo)
        //         api.user.getMemberInfo(this.userInfo.id).then((res) => {
        //           if (res.errno === 0) {
        //            
        //             console.log(this.memberInfo);
        //           }
        //         });
        this.addressList = [{
          title: '学校',
          name: 'Jack Chen',
          mobile: '18928779564',
          address: '广州市番禺区南城路698号',
        }, {
          title: '我的家',
          name: 'Jack Chen',
          mobile: '18928779564',
          address: '广州市番禺区南城路698号'
        }];
      }
    },
    methods: {
      // ...mapMutations(['logout']),
      // ...mapActions(['getUserInfo', 'logout']),
      ...mapActions({
        getUserInfo: 'user/getUserInfo',
      }),
    }
  }
</script>
<style>
</style>
