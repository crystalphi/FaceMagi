<template>

	<view>
		
		<view class="ts-column ts-flex-item">
			<view class="ts-section">
				<view class="ts-section-title">美颜麻吉 - 功能列表</view>
				<view class="ts-section-body">
					<view class="ts-row">
						<navigator url="/pages/app/face/functions/image" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>图片美颜</text>
							</view>
						</navigator>
						<navigator url="/pages/app/face/functions/filter" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>美颜滤镜</text>
							</view>
						</navigator>
						<navigator url="/pages/app/face/functions/magic" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>时光幻影</text>
							</view>
						</navigator>
					</view>
					<view class="ts-row"></view>
					<view class="ts-row"></view>
				</view>
			</view>
		</view>
		<ts-gap></ts-gap>
		
		<view class="uni-padding-wrap uni-common-pb">
			<view class="uni-hello-text uni-common-pb">
				以下是uni-app扩展组件示例，更多组件见插件市场：<u-link :href="'https://ext.dcloud.net.cn/'" :text="'https://ext.dcloud.net.cn'" :inWhiteList="true"></u-link>
			</view>
			<view class="uni-card" v-for="(list,index) in lists" :key="index">
				<view class="uni-list">
					<view class="uni-list-cell uni-collapse card-cell">
						<view class="uni-list-cell-navigate uni-navigate-right" hover-class="uni-list-cell-hover" @click="goDetailPage(list.url)">
							{{list.name}}
						</view>
					</view>
				</view>
			</view>
		</view>

	</view>

</template>

<script>
	import uLink from "@/components/uLink.vue"
	
	export default {
		components: {
			uLink
		},
		data() {
			return {
				lists: [{
						name: "Convert Gender",
						url: "convert-gender",
						title: "Unlimit your imagination",
						desc: "Are you curious to know what you would look like as another gender?"
					},
					{
						name: "Time Machine",
						url: "time-machine",
						title: "See you in the future",
						desc: "[Aging] Journey thru time to see what you will look like in 30 years time"
					},
					{
						name: "Dreamy Scene",
						url: "dream-scene",
						title: "One tap to transform scenes",
						desc: "[Face swap] To a wedding scene; be a mermaid princess; be like the Mona Lisa, or other such famous art subjects; there are a variety of character scenes for you to choose from"
					},
					{
						name: "Premium Frames",
						url: "premium-frames",
						title: "Use the frames to get creative",
						desc: "Choose from a variety of frames and backgrounds and improve your photos!"
					},
				]
			}
		},
		onPullDownRefresh() {
			
		},
		onLoad(options) {
			// #ifdef APP-PLUS
			plus.nativeUI.showWaiting('加载中……');
			// #endif
		},
		onReady() {
			// #ifdef APP-PLUS
			plus.nativeUI.closeWaiting();
			// #endif
		},
		onShareAppMessage() {
			return {
				title: '欢迎体验uni-app',
				path: '/pages/tabBar/extUI/extUI'
			}
		},
		onReachBottom() {

		},
		onNavigationBarButtonTap(e) {
			uni.navigateTo({
				url: '/pages/about/about'
			});
		},
		methods: {
			goDetailPage(path) {
				uni.navigateTo({
					url: '/pages/extUI/' + path + '/' + path
				});
			}
		}
	};
</script>

<style>
	page {
		height: auto;
		min-height: 100%;
		background-color: #f1f1f1;
	}
	
	view {
		display: flex;
		flex-direction: column;
		font-size: 28upx;
		line-height: inherit
	}
	
	.card-cell {
		margin: 40upx 0;
		height: 150upx;
	}
</style>
