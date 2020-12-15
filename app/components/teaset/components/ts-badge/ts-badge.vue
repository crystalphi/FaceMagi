<template>
  <text class="uni-badge" v-if="text" :class="setClass" @click="onClick()">{{text}}</text>
</template>

<script>
  export default {
    name: 'ts-badge',
    props: {
      type: {
        type: String,
        default: 'default'
      },
      inverted: {
        type: Boolean,
        default: false
      },
      text: {
        type: [String,Number,Boolean],
        default: ''
      },
      size: { //small.normal
        type: String,
        default: 'normal'
      }
    },
    computed: {
      setClass() {
        let classList = ['uni-badge-' + this.type, 'uni-badge--' + this.size];
        if (this.inverted === true) {
          classList.push('uni-badge-inverted')
        }
        return classList.join(" ")
      }
    },
    methods: {
      onClick() {
        this.$emit('click')
      }
    }
  }
</script>

<style lang="scss" scoped>
  @charset "UTF-8";

  $tag-pd:0upx 32upx;
  $tag-small-pd:0upx 16upx;

  .uni-badge {
    // 		font-family: 'Helvetica Neue', Helvetica, sans-serif;
    // 		box-sizing: border-box;
    // 		font-size: 24upx;
    // 		/* line-height: 1; */
    // 		display: inline-block;
    // 		padding: $tag-small-pd;
    // 		color: #333;
    // 		/* border-radius: 100px; */
    //     border-radius: 10upx;
    // 		background-color: #f1f1f1

    box-sizing: border-box;
    padding: $tag-small-pd;
    height: 60upx;
    line-height: calc(60upx - 2upx);
    font-size: $uni-font-size-base;
    display: inline-block;
    color: $uni-text-color;
    border-radius: $uni-border-radius-base;
    background-color: $uni-bg-color-grey;
    border: 1upx solid $uni-bg-color-grey;


font-weight: normal;

    border-radius: 30upx;
  }

  .uni-badge.uni-badge-inverted {
    padding: 0 5upx 0 0;
    color: #999;
    background-color: transparent
  }

  .uni-badge-primary {
    color: #fff;
    background-color: #007aff
  }

  .uni-badge-primary.uni-badge-inverted {
    color: #007aff;
    background-color: transparent
  }

  .uni-badge-success {
    color: #fff;
    background-color: #4cd964
  }

  .uni-badge-success.uni-badge-inverted {
    color: #4cd964;
    background-color: transparent
  }

  .uni-badge-warning {
    color: #fff;
    background-color: #f0ad4e
  }

  .uni-badge-warning.uni-badge-inverted {
    color: #f0ad4e;
    background-color: transparent
  }

  .uni-badge-error {
    color: #fff;
    background-color: #dd524d
  }

  .uni-badge-error.uni-badge-inverted {
    color: #dd524d;
    background-color: transparent
  }

  .uni-badge--small {
    // 		transform: scale(.8);
    // 		transform-origin: center center

    height: 40upx;
    padding: $tag-small-pd;
    line-height: calc(40upx - 2upx);
    font-size: $uni-font-size-sm;
    border-radius: 20upx;
  }
</style>
