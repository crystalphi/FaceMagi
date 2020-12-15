<template>
  <view class="ts-list-cell" :class="[disabled === true || disabled === 'true' ? 'ts-list-cell--disabled' : '']"
    :hover-class="disabled === true || disabled === 'true' || showSwitch === true || showSwitch === 'true' ? '' : 'ts-list-cell--hover'"
    @click="onClick">
    <view class="ts-list-cell__container">
      <view class="ts-list-cell__icon" v-if="thumb">
        <image class="ts-list-cell__icon-img" :src="thumb"></image>
      </view>
      <view class="ts-list-cell__icon" v-else-if="showExtraIcon === true || showExtraIcon === 'true'">
        <ts-icon :color="extraIcon.color" :size="extraIcon.size" :type="extraIcon.type"></ts-icon>
      </view>
      <view class="ts-list-cell__content">
        <view class="ts-list-cell__content-title">{{title}}</view>
        <view class="ts-list-cell__content-note" v-if="note">{{note}}</view>
      </view>
      <view class="ts-list-cell__extra" v-if="showBadge === true || showBadge === 'true' || showArrow === true || showArrow === 'true'||showSwitch === true || showSwitch === 'true'">
        <ts-badge v-if="showBadge === true || showBadge === 'true'" :type="badgeType" :text="badgeText"></ts-badge>
        <switch v-if="showSwitch === true || showSwitch === 'true'" :disabled='disabled' :checked="switchChecked"
          @change="onSwitchChange" />
        <ts-icon v-if="showArrow === true || showArrow === 'true'" color="#bbb" size="20" type="arrowright"></ts-icon>
      </view>
    </view>
  </view>
</template>

<script>
  import tsIcon from '../ts-icon/ts-icon.vue'
  import tsBadge from '../ts-badge/ts-badge.vue'
  export default {
    name: 'ts-list-item',
    components: {
      tsIcon,
      tsBadge
    },
    data() {
      return {

      };
    },
    props: {
      title: String, //列表标题
      note: String, //列表描述
      disabled: { //是否禁用
        type: [Boolean, String],
        default: false
      },
      showArrow: { //是否显示箭头
        type: [Boolean, String],
        default: true
      },
      showBadge: { //是否显示数字角标
        type: [Boolean, String],
        default: false
      },
      showSwitch: { //是否显示Switch
        type: [Boolean, String],
        default: false
      },
      switchChecked: { //Switch是否被选中
        type: [Boolean, String],
        default: false
      },
      badgeText: String, //badge内容
      badgeType: { //badge类型
        type: String,
        default: 'success'
      },
      thumb: String, //缩略图
      showExtraIcon: { //是否显示扩展图标
        type: [Boolean, String],
        default: false
      },
      extraIcon: {
        type: Object,
        default () {
          return {
            type: "contact",
            color: "#000000",
            size: "20"
          };
        }
      }
    },
    methods: {
      onClick() {
        this.$emit('click')
      },
      onSwitchChange(e) {
        this.$emit('switchChange', e.detail)
      }
    }
  }
</script>

<style lang="scss">
  @mixin list-hover {
    background-color: $uni-bg-color-hover;
  }

  @mixin list-disabled {
    opacity: 0.3;
  }

  $list-cell-pd:$uni-spacing-col-lg $uni-spacing-row-lg;

  .ts-list-cell {
    font-size: $uni-font-size-lg;
    position: relative;
    display: flex;
    flex-direction: row;
    // width: 100%;
    flex: 1;
    justify-content: space-between;
    align-items: center;

    &--disabled {
      @include list-disabled;
    }

    &--hover {
      @include list-hover;
    }

    &__container {
      padding: $list-cell-pd;
      width: 100%;
      box-sizing: border-box;
      flex: 1;
      position: relative;
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      align-items: center;

      &:after {
        position: absolute;
        z-index: 3;
        right: 0;
        bottom: 0;
        left: 30upx;
        height: 1px;
        content: '';
        -webkit-transform: scaleY(.5);
        transform: scaleY(.5);
        background-color: $uni-border-color;
      }
    }

    &__content {
      flex: 1;
      overflow: hidden;
      display: flex;
      flex-direction: column;

      &-title {
        font-size: $uni-font-size-lg;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: inherit;
        line-height: 1.5;
        overflow: hidden;
      }

      &-note {
        color: $uni-text-color-grey;
        font-size: $uni-font-size-base;
        white-space: normal;
        display: -webkit-box;
        -webkit-box-orient: vertical;
        -webkit-line-clamp: 2;
        overflow: hidden;
      }
    }

    &__extra {
      width: 25%;
      display: flex;
      flex-direction: row;
      justify-content: flex-end;
      align-items: center;
    }

    &__icon {
      margin-right: 18upx;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;

      &-img {
        height: $uni-img-size-base;
        width: $uni-img-size-base;
      }
    }
  }

  .ts-list>.ts-list-cell:last-child .ts-list-cell-container:after {
    height: 0px;
  }
</style>
