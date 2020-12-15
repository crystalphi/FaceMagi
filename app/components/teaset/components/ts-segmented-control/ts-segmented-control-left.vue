<template>
	<view class="ts-flex ts-row">
		<view class="ts-segmented-left">
			<scroll-view scroll-y :style="'height:'+heightPx +'px; width:' + tabWidthPx  +'px;'">
				<view v-for="(item, index) in values" class="nav-left-item" :class="index==current?'active':''" :key="index" @click="onClick(index)"
				 :style="'height:'+tabHeightPx +'px; width:' + tabWidthPx  +'px;'">
					{{item}}
				</view>
			</scroll-view>
		</view>

		<scroll-view class="ts-segmented-content" scroll-y @scrolltolower="onReachBottom" :style="'height:'+heightPx+'px'">
			<slot></slot>
		</scroll-view>
	</view>

</template>

<script>
	var self;
	export default {
		data() {
			return {
				// 				tabScrollTop: [],
				// 				scrollTop: 0,
				currentTab: 0,
				scale: 1,

				// tabs: [],
			}
		},
		model: {
			prop: 'current',
			event: 'clickItem'
		},
		props: {
			tabWidth: { //导航按钮的宽度，单位为px
				type: Number,
				default () {
					//return uni.getSystemInfoSync().windowWidth / 4;
					return 200;
				}
			},
			tabHeight: { //导航按钮的高度，单位为px
				type: Number,
				default: 100,
			},
			height: { //整个控件显示区域的高度，单位为px
				type: Number,
				default () {
					//换算为UPX单位
					const {
						windowHeight,
						windowWidth
					} = uni.getSystemInfoSync();
					return windowHeight / windowWidth * 750;
				}
			},
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
		},
		watch: {
			currentTab(val) {
				this.onClick(val);
			},
			current(val) {
				this.updateValue(val);
			},

			// 			values(val) {
			// 				this.tabs = val;
			// 			}
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
				if (this.currentTab !== index) {
					// console.log('onClick(index)')
					this.currentTab = index;
					// 					const _self = this;
					// 					setTimeout(function() {
					// 						_self.$emit('clickItem', index);
					// 					}, 10)

					//或者写成以下语法
					setTimeout(() => {
						this.$emit('clickItem', index);
					}, 10)
				}
			},
			updateValue(val) {
				this.currentTab = val;
			},

			onReachBottom(e) {
				this.$emit('onReachBottom')
			},
		},
		onLoad: function() {
			// this.height = uni.getSystemInfoSync().windowHeight;
			this.updateValue(this.current);

			this.scale = uni.getSystemInfoSync().windowWidth / 750;
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
