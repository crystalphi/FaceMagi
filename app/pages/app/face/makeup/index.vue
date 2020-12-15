<template>
	<view>
		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="backText">返回</block>
			<block slot="content">图标</block>
		</cu-custom>
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
						name: "Fashion Makeup",
						url: "fashion-makeup",
						title: "Hundreds of latest trends effects",
						desc: "[FACIAL STICKERS] Using facial recognition, create customized hairstyles, beards and eye wear stickers for men with just one touch. Exclusive women\'s hairstyles and eye wear stickers that let you freely try on new styles"
					},
					{
						name: "Realtime Filters",
						url: "realtime-filters",
						title: "Define your style with 100+ filters",
						desc: "Various Filter: Whether you want to create a fashionable, sweet, lazy, or everyday style, our filters can always help you! Real-time Skin and Facial Reshaping: Beautify your selfie when taking pictures, no need to edit afterwards!"
					},
					{
						name: "Skin Tone",
						url: "skin-tone",
						title: "Make your skin tone and texture even out",
						desc: "Easily adjust your skin tone, whether you want bronze, dark or fair skin, Facetify can do it for you."
					},
					{
						name: "Auto Skin Retouch",
						url: "auto-skin-retouch",
						title: "Custom your own beauty effects",
						desc: "Smooth Skin: Creates smooth skin while keeping the area outside the skin unaffected, no longer have to worry about exaggerated smoothing!\nFix the redness: Cool down skin redness and give you healthy and natural skin.\nRosy skin – Rejuvenate pale skin and make it rosy and energetic.\nBright eyes - Brighten your eyes with a vibrant glow. \nGet rid of dark circles – Remove the annoying dark circles. \nTeeth whitening – Whiten your teeth and make your smile confident."
					},
					{
						name: "Manly Stickers",
						url: "manly-stickers",
						title: "Change hair styles, beards and glasses in 1 min",
						desc: ""
					},
				],
				//ColorList: this.ColorList
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
	/*
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
	*/
	
	.card-cell {
		margin: 40upx 0;
		height: 150upx;
	}
</style>
