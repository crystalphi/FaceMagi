<template>
	<view>
		<view class="bg-img bg-mask flex align-center" style="background-image: url('https://ossweb-img.qq.com/images/lol/web201310/skin/big10006.jpg');height: 350upx;">
			<view class="padding-xl text-white">
				<view class="padding-xs text-xxl text-bold">
					FaceMagi
				</view>
				<view class="padding-xs text-lg">
					Designed for perfect selfies
				</view>
			</view>
		</view>
		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				<text class="cuIcon-title text-blue"></text>{{ i18n.face_makeup }}
			</view>
		</view>
		<view class="nav-list">
			<navigator hover-class="none" :url="'/pages/app/face/makeup/' + item.url" class="nav-li" navigateTo :class="'bg-'+item.color"
			 :style="[{animation: 'show ' + ((index+1)*0.2+1) + 's 1'}]" v-for="(item,index) in FaceMakeupList" :key="index">
				<view class="nav-title"></view>
				<view class="nav-name">{{item.title}}</view>
				<text :class="'cuIcon-' + item.icon"></text>
			</navigator>
		</view>
		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				<text class="cuIcon-title text-blue"></text>{{ i18n.face_creative }}
			</view>
		</view>
		<view class="grid col-2 padding-sm">
			<view class="padding-sm" v-for="(item,index) in FaceCreativeList" :key="index">
				<navigator hover-class="none" :url="'/pages/app/face/creative/' + item.url" class="padding-sm" navigateTo>
				
					<view :class="'padding radius text-center shadow-blur bg-gradual-'+item.color">
						<text class="cuIcon-cu-image" :class="'cuIcon-' + item.icon"></text>
						<view class="margin-top-sm text-bold">{{item.name}}</view>
					</view>
				</navigator>
			</view>
			<view class="padding-sm">
				<view class="bg-gradual-pink padding radius text-center shadow-blur" style="background-image: url('https://ossweb-img.qq.com/images/lol/web201310/skin/big10007.jpg');height: 207upx;">
					<view class="text-lg">霞彩</view>
					<view class="margin-top-sm text-Abc">#ec008c - #6739b6</view>
				</view>
			</view>
		</view>
		<view class="cu-bar bg-white margin-top">
			<view class="action">
				<text class="cuIcon-title text-blue"></text>透明背景(文字层)
			</view>
		</view>
		<view class="grid col-2">
			<view class="bg-img padding-bottom-xl" style="background-image: url('https://ossweb-img.qq.com/images/lol/web201310/skin/big10007.jpg');height: 207upx;">
				<view class="bg-shadeTop padding padding-bottom-xl">
					上面开始
				</view>
			</view>
			<view class="bg-img padding-top-xl flex align-end" style="background-image: url('https://ossweb-img.qq.com/images/lol/web201310/skin/big10001.jpg');height: 207upx;">
				<view class="bg-shadeBottom padding padding-top-xl flex-sub">
					下面开始
				</view>
			</view>
		</view>

		<view class="ts-column ts-flex-item">
			<!--<ts-banner image="http://via.placeholder.com/750x375" :height="375"></ts-banner>-->
			<view class="ts-section">
				<view class="ts-section-title">Makeup</view>
				<view class="ts-section-body">
					<view class="ts-row">
						<navigator url="/pages/app/face/makeup/index" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>index</text>
							</view>
						</navigator>
						<navigator url="/pages/app/face/makeup/fashion-makeup" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>Fashion Makeup</text>
							</view>
						</navigator>
					</view>
					<view class="ts-row">
						<navigator url="/pages/app/face/makeup/manly-stickers" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>Manly Stickers</text>
							</view>
						</navigator>
						<navigator url="/pages/app/face/makeup/realtime-filters" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>Realtime Filters</text>
							</view>
						</navigator>
					</view>
				</view>
			</view>
			<ts-gap></ts-gap>
			<view class="ts-section">
				<view class="ts-section-title">Creative</view>
				<view class="ts-section-body">
					<view class="ts-row">
						<navigator url="/pages/app/face/creative/index" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>aaa</text>
							</view>
						</navigator>
						<navigator url="/pages/app/face/creative/index" hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-column ts-flex-item  ts-center">
								<image class="app-icon" src="http://via.placeholder.com/48x48"></image>
								<text>bbb</text>
							</view>
						</navigator>
						<view class="ts-flex-item"></view>
						<view class="ts-flex-item"></view>
					</view>
				</view>
			</view>
			<ts-gap></ts-gap>
		</view>
	</view>
</template>

<script>
	export default {
		components: {

		},
		data() {
			return {
				FaceMakeupList: this.FaceMakeupList,
				FaceCreativeList: this.FaceCreativeList
			}
		},
		onPullDownRefresh() {
			setTimeout(() => {
				uni.stopPullDownRefresh()
			}, 1000)
		},
		onLoad(options) {
		},
		onReachBottom() {
		},
		computed: {
			i18n() {
				return this.$t('index');
			},
		},
		methods: {
		}
	};
</script>

<style lang="scss">

</style>
