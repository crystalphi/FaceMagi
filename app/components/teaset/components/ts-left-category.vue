<template>
	<view class="ts-flex ts-row">
		<view class="ts-segmented-left">
			<scroll-view scroll-y :style="'height:'+heightPx +'px; width:' + tabWidthPx  +'px;'">
				<view v-for="(item, index) in tabItems" class="nav-left-item" :class="index==current?'active':''" :key="index"
				 @click="onClick(index)" :style="'height:'+tabHeightPx +'px; width:' + tabWidthPx  +'px;'">
					{{item}}
				</view>
			</scroll-view>
		</view>

		<!-- <view class="ts-segmented-content">
			<slot></slot>
      </view> -->
		<scroll-view class="ts-segmented-content" scroll-y @scroll="handleScroll" @scrolltolower="onReachBottom" :scroll-top="scrollTop" :style="'height:'+heightPx+'px'">
			<slot></slot>
		</scroll-view>
	</view>

</template>

<script>
	var self;
	export default {
		data() {
			return {
				tabScrollTop: [],
				scrollTop: 0,
				current: 0,
				scale: 1,
			}
		},
		props: {
			tabWidth: { //导航按钮的宽度，单位为px
				type: Number,
				async default () {
					return uni.getSystemInfoSync().windowWidth / 4;
				}
			},
			tabHeight: { //导航按钮的高度，单位为px
				type: Number,
				default: 100,
			},
			height: { //整个控件显示区域的高度，单位为px
				type: Number,
				async default () {
					//换算为UPX单位
					const {
						windowHeight,
						windowWidth
					} = uni.getSystemInfoSync();
					return windowHeight / windowWidth * 750;
				}
			},
			currentTab: {
				type: Number,
				default: 0
			},
			tabItems: {
				type: Array,
				default () {
					return [];
				}
			},
		},
		computed: {
			tabWidthPx() {
				return this.scale * this.tabWidth;
			},
			tabHeightPx() {
				return this.scale * this.tabHeight;
			},
			heightPx() {
				return this.scale * this.height;
			}
		},
		methods: {
			onClick(index) {
				if (this.current !== index) {
					self.current = index;
					this.$emit('clickItem', index);

					//需要延时操作，等待Tab切换完成才能正确恢复位置
					setTimeout(function() {
						//恢复上一次的滚动位置
						self.scrollTop = self.tabScrollTop[self.current];
					}, 200)
				};
			},
      onReachBottom(e){
        this.$emit('onReachBottom')
      },
			handleScroll(e) {
				//"detail":{"scrollLeft":0,"scrollTop":346,"scrollHeight":2347,"scrollWidth":290,"deltaX":0,"deltaY":-1}
				//记录当前的滚动位置
				this.tabScrollTop[this.current] = e.target.scrollTop;
			}
		},
		mounted: async function() {
			self = this;
			// this.height = uni.getSystemInfoSync().windowHeight;
			this.current = this.currentTab;
			this.scale = await uni.getSystemInfoSync().windowWidth / 750;
			for (let index = 0; index < this.tabItems.length; index++) {
				this.tabScrollTop[index] = 0;
			}
		}
	}
</script>

<style>
	/*  page view{
    border: #000000 solid 1px;
  } */

	.ts-segmented-left {
		display: flex;
		flex-direction: column;
		/* 		align-content: flex-start;
		justify-content: flex-start; */
		border-right: solid 1upx #E0E0E0;
		border-top: solid 1upx #E0E0E0;
		min-height: 100%;
	}

	.ts-segmented-content {
		display: flex;
		flex: 1;
		flex-direction: column;
		min-height: 100%;
		/* 		align-content: flex-start;
		justify-content: flex-start; */
	}

	.nav-left-item {
		height: 100upx;
		/* border-right: solid 1upx #E0E0E0; */
		border-bottom: solid 1upx #E0E0E0;
		font-size: 30upx;
		display: flex;
		align-items: center;
		justify-content: center;
		display: flex;
	}

	.active {
		color: #d81e06;
		font-weight: bold;
		border-bottom: #d81e06 solid 5upx;
	}
</style>
