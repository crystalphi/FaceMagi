<template>
  <view class="ts-column ts-flex-item">
    <view class="ts-list">
      <view class="ts-list-cell" hover-class="ts-list-cell-hover">
        <view class="ts-list-cell-navigate ts-navigate-badge">用户ID
          <ts-badge :text="userInfo.id" type="default" inverted></ts-badge>
        </view>
      </view>
      <view class="ts-list-cell" hover-class="ts-list-cell-hover">
        <view class="ts-list-cell-navigate ts-navigate-badge">账号类型
          <ts-badge :text="userInfo.user_type" type="primary"></ts-badge>
        </view>
      </view>
      <view class="ts-list-cell" hover-class="ts-list-cell-hover">
        <view class="ts-list-cell-navigate ts-navigate-badge">邀请码
          <ts-badge :text="memberInfo && memberInfo.invitation_code" type="danger" inverted></ts-badge>
        </view>
      </view>
      <view class="ts-list-cell" hover-class="ts-list-cell-hover">
        <view class="ts-list-cell-navigate ts-navigate-badge">账号
          <ts-badge :text="userInfo.username" type="default" inverted></ts-badge>
        </view>
      </view>
      <view class="ts-list-cell" hover-class="ts-list-cell-hover">
        <view class="ts-list-cell-navigate ts-navigate-badge">手机号码
          <ts-badge :text="userInfo.mobile" type="default" inverted></ts-badge>
        </view>
      </view>
      <view class="ts-list-cell" hover-class="ts-list-cell-hover">
        <view class="ts-list-cell-navigate ts-navigate-badge">邮箱
          <ts-badge :text="userInfo.email" type="default" inverted></ts-badge>
        </view>
      </view>
    </view>
  </view>
</template>
<script>
  import api from "@/common/api";
  import {
    mapState,
    mapMutations,
    mapActions
  } from "vuex";
  export default {
    data() {
      return {
        hasUserInfo: true,
        userInfo: {
          id: "",
          username: "",
          email: "",
          mobile: "",
          user_type: ""
        },
        memberInfo: {
          invitation_code: ""
        }
      };
    },
    computed: {
      ...mapState(["hasLogin"])
    },
    methods: {
      // ...mapMutations(['logout']),
      // ...mapActions(['getUserInfo', 'logout']),
      ...mapActions({
        getUserInfo: "user/getUserInfo"
      })
    },
    async onLoad() {
      if (this.hasLogin) {
        //必须先登录才能获取用户的信息
        this.userInfo = await this.getUserInfo();
        // console.log(this.userInfo)
        // this.$logger.info(this.$logger.dump(this.userInfo))
        api.user.getMemberInfo(this.userInfo.id).then(res => {
          if (res.errno === 0) {
            this.memberInfo = res.data;
            // console.log(this.memberInfo);
          }
        });
      }
    }
  };
</script>
<style>
</style>
