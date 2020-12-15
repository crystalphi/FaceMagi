<template>
  <view class="ts-segmented-control" :class="styleType" :style="wrapStyle">
    <view v-for="(item, index) in values" class="ts-segmented-control-item" :class="styleType" :key="index" :style="index === currentTab ? activeStyle : itemStyle"
      @click="onClick(index)">
      {{item}}
    </view>
  </view>
</template>

<script>
  export default {
    name: 'ts-segmented-control',
    model: {
      prop: 'current',
      event: 'clickItem'
    },
    data() {
      return {
        currentTab: 0,
      }
    },
    watch: {
      currentTab(val) {
        this.onClick(val);
      },
      current(val) {
        this.updateValue(val);
      }
    },
    onLoad: function(e) {
      this.updateValue(this.current);
    },
    props: {
      current: {
        type: Number,
        default: 0
      },
      values: {
        type: Array,
        default () {
          return [];
        }
      },
      activeColor: {
        type: String,
        default: '#d81e06'
      },
      borderColor: {
        type: String,
        default: '#d81e06'
      },
      styleType: {
        //支持：button,text
        type: String,
        default: 'text'
      }
    },
    computed: {
      wrapStyle() {
        let styleString = '';
        switch (this.styleType) {
          case 'text':
            styleString = `border:0;`;
            break;
          default:
            styleString = `border-color: ${this.borderColor}`;
            break;
        }
        return styleString;
      },
      itemStyle() {
        let styleString = '';
        switch (this.styleType) {
          case 'text':
            styleString = `color:#000;border-left:0; border-bottom: #F0F0F0 solid 1px;`;
            break;
          default:
            styleString = `color:${this.activeColor};border-color:${this.borderColor};`;
            break;
        }
        return styleString;
      },
      activeStyle() {
        let styleString = '';
        switch (this.styleType) {
          case 'text':
            styleString = `color:${this.activeColor};border-left:0;border-bottom-style:solid;`;
            break;
          default:
            styleString = `color:#fff;border-color:${this.borderColor};background-color:${this.activeColor}`;
            break;
        }
        return styleString;
      }
    },
    methods: {
      onClick(index) {
        if (this.currentTab !== index) {
          this.currentTab = index;
          setTimeout(() => {
            this.$emit('clickItem', index);
          }, 10)
        }
      },
      updateValue(val) {
        this.currentTab = val;
      },
    },
  }
</script>

<style scoped lang="scss">
  .ts-segmented-control {
    justify-content: center;
    /* width: 100%; */
    display: flex;
    flex-direction: row;
    flex: 1;

    // font-size: 40upx;
		font-size:$uni-font-size-base;
    border-radius: 12upx;
    box-sizing: border-box;
    margin: 0 auto;
    overflow: hidden;
		font-weight: normal;
  }

  .ts-segmented-control.button {
    border: 1upx solid #CCCCCC;
  }

  .ts-segmented-control.text {
    border: 0;
    border-radius: 0upx;
  }

  .ts-segmented-control-item {
    flex: 1;
    text-align: center;
    line-height: 80upx;
    box-sizing: border-box;

    align-items: center;
    justify-content: center;
  }

  .ts-segmented-control-item.button {
    border-left: 1upx solid;
  }

  .ts-segmented-control-item.text {
    border-left: 0;
  }

  .ts-segmented-control-item:first-child {
    border-left-width: 0;
  }
</style>
