<template>
  <view class="ts-row" v-if="closable">
    <view v-if="text" :class="computedClass" @click="onClick()">
      <view class="ts-row ts-padding-right" >
      	   {{text}}
      </view>   
      <view :hover-class="disabled?'none':'navigator-hover'" @click="onClose()">
      	 x
      </view>    
    </view>
  </view>
  <view v-else>
    <view v-if="text" :class="computedClass" @click="onClick()">{{text}}</view>
  </view>
</template>

<script>
  export default {
    name: 'ts-tag',
    props: {
      closable: {
        type: Boolean,
        default: false
      },
      type: { //标签类型default、primary、success、warning、error
        type: String,
        default: 'default'
      },
      size: { //标签大小 normal, small
        type: String,
        default: 'small'
      },
      text: [String, Number, Boolean], //标签内容
      disabled: { //是否为禁用状态
        type: [String, Boolean],
        defalut: false
      },
      inverted: { //是否为空心
        type: [String, Boolean],
        defalut: false
      },
      circle: { //是否为圆角
        type: [String, Boolean],
        defalut: false
      },
      dashed: { //是否为虚线框
        type: [String, Boolean],
        defalut: false
      },
      mark: { //是否为标记样式
        type: [String, Boolean],
        defalut: false
      }
    },
    computed: {
      computedClass() {
        let classArr = ['ts-tag'];

        if (this.disabled === true || this.disabled === 'true') {
          classArr.push('ts-tag--disabled');
        }
        if (this.inverted === true || this.inverted === 'true') {
          classArr.push('ts-tag--inverted');
        }
        if (this.circle === true || this.circle === 'true') {
          classArr.push('ts-tag--circle');
        }
        if (this.mark === true || this.mark === 'true') {
          classArr.push('ts-tag--mark');
        }

        if (this.dashed === true || this.dashed === 'true') {
          classArr.push('ts-tag--dashed');
        }

        classArr.push('ts-tag--' + this.size);
        classArr.push('ts-tag--' + this.type);
        // console.log(classArr);
        return classArr;
      }
    },
    methods: {
      onClick() {
        if (this.disabled === true || this.disabled === 'true') {
          return;
        }
        this.$emit('click')
      },
      onClose() {
        if (this.disabled === true || this.disabled === 'true') {
          return;
        }
        this.$emit('close')
        console.log('close')
      }
    }
  }
</script>

<style lang="scss" scoped>
	$tag-pd:0upx 10upx;
	$tag-small-pd:0upx 5upx;

  @mixin tag-disabled {
    opacity: 0.5;
  }

  .ts-tag {
    box-sizing: border-box;
    
		padding: $tag-pd;
    margin: 5upx;
		
    // height: 60upx;
    // line-height: calc(60upx - 2upx);
    font-size: $uni-font-size-base;
    display: flex;
    flex-direction: row;
    color: $uni-text-color;
    border-radius: $uni-border-radius-base;
    background-color: $uni-bg-color-grey;
    border: 1upx solid $uni-bg-color-grey;

    justify-content: center;
    align-items: center;
		font-weight: normal;

    &--circle {
      border-radius: 30upx;
    }

    &--mark {
      border-radius: 0 30upx 30upx 0
    }

    &--dashed {
      border: 1upx dashed;
    }

    &--disabled {
      @include tag-disabled;
    }

    &--small {
      // height: 40upx;
      padding: $tag-small-pd;
      // line-height: calc(40upx - 2upx);
      font-size: $uni-font-size-sm;
    }

    &--default {}

    &--primary {
      color: $uni-text-color-inverse;
      background-color: $uni-color-primary;
      border: 1upx solid $uni-color-primary;

      &.ts-tag--inverted {
        color: $uni-color-primary;
        background-color: $uni-bg-color;
        border: 1upx solid $uni-color-primary;
      }

    }

    &--success {
      color: $uni-text-color-inverse;
      background-color: $uni-color-success;
      border: 1upx solid $uni-color-success;

      &.ts-tag--inverted {
        color: $uni-color-success;
        background-color: $uni-bg-color;
        border: 1px solid $uni-color-success;
      }

      &.ts-tag--dashed {
        border: 1upx dashed;
      }
    }

    &--warning {
      color: $uni-text-color-inverse;
      background-color: $uni-color-warning;
      border: 1upx solid $uni-color-warning;

      &.ts-tag--inverted {
        color: $uni-color-warning;
        background-color: $uni-bg-color;
        border: 1upx solid $uni-color-warning;
      }

      &.ts-tag--dashed {
        border: 1upx dashed;
      }
    }

    &--error {
      color: $uni-text-color-inverse;
      background-color: $uni-color-error;
      border: 1upx solid $uni-color-error;

      &.ts-tag--inverted {
        color: $uni-color-error;
        background-color: $uni-bg-color;
        border: 1upx solid $uni-color-error;
      }

      &.ts-tag--dashed {
        border: 1upx dashed;
      }
    }


    &--inverted {
      color: $uni-text-color;
      background-color: $uni-bg-color;
      border: 1upx solid $uni-bg-color-grey;
    }
  }
</style>
