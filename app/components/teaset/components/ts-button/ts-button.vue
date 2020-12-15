<template>
  <view :style="styleStr + 'height:' +heightPx + 'px; padding:' + paddingPx + 'px; border-radius:' + borderRadiusPx +'px;' "
    :disabled="disabled" @click="onClick" :hover-class="disabled?'none':'navigator-hover'" :class="['ts-btn', 'ts-btn-'+type, inverted === true ? 'ts-btn-inverted' : '', disabled ? 'ts-btn-disabled':'']">
    <!--  ts-btn-primary ts-btn-inverted ts-btn-enabled -->
    <slot></slot>
  </view>
</template>

<script>
  export default {
    name: 'ts-button',
    props: {
      styleStr: {
        type: String,
        default: ''
      },
      height: {
        type: Number,
        default: 80,
      },
      padding: {
        type: Number,
        default: 10,
      },
      type: {
        type: String,
        default: 'primary'
      },
      borderRadius: {
        type: Number,
        default: 0,
      },
      disabled: {
        type: Boolean,
        default: false
      },
      inverted: {
        type: Boolean,
        default: false
      },
    },
    computed: {
      heightPx() {
        return uni.upx2px(this.height);
      },
      paddingPx() {
        let padding = uni.getSystemInfoSync().windowWidth / 750 * this.padding;
        return padding
        // return uni.upx2px(this.padding);
      },
      borderRadiusPx() {
        let borderRadius = uni.getSystemInfoSync().windowWidth / 750 * this.borderRadius;
        return borderRadius
        // return uni.upx2px(this.borderRadius);
      }
    },
    methods: {
      onClick() {

        if (!this.disabled) {
          this.$emit('click')
          // console.log('onClick')
        }
      }
    }
  }
</script>

<style>
  .ts-btn {
    font-family: 'Helvetica Neue', Helvetica, sans-serif;
    box-sizing: border-box;
    font-size: 28upx;
    padding: 20upx 30upx;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
  }

  .ts-btn-primary {
    border: 1upx solid #007aff;
    color: #fff;
    background-color: #007aff
  }

  .ts-btn-success {
    border: 1upx solid #4cd964;
    color: #fff;
    background-color: #4cd964;
  }

  .ts-btn-warning {
    border: 1upx solid #f0ad4e;
    color: #fff;
    background-color: #f0ad4e
  }

  .ts-btn-error {
    border: 1upx solid #dd524d;
    color: #fff;
    background-color: #dd524d
  }

  .ts-btn-primary.ts-btn-inverted {
    border: 1upx solid #007aff;
    color: #007aff;
    background-color: #fff
  }

  .ts-btn-success.ts-btn-inverted {
    border: 1upx solid #4cd964;
    color: #4cd964;
    background-color: #fff
  }

  .ts-btn-warning.ts-btn-inverted {
    border: 1upx solid #f0ad4e;
    color: #f0ad4e;
    background-color: #fff
  }

  .ts-btn-error.ts-btn-inverted {
    border: 1upx solid #dd524d;
    color: #dd524d;
    background-color: #fff
  }

  .ts-btn-disabled {
    opacity: .6
  }
</style>
