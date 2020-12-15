<template>
	<view>

		<cu-custom bgColor="bg-gradual-blue" :isBack="true">
			<block slot="backText">{{ i18n.back }}</block>
			<block slot="content">{{ i18n.skin_tone }}</block>
		</cu-custom>

		<view class="zzz-tab-swiper bg-white set-bottom">
			<zzzTabSwiper :galleryheight="100" bkstart="#eef2ee" bkend="#eef2ee" :imgviewwidth="72" :imgviewheight="72"
			 :showbadge="true" badegwidth="25" badegheight="25" :showdec="true" :tabSwiperData="tabSwiperData" :mainImageDefault="mainImageDefault"
			 @clickimg="onclickimg">
			</zzzTabSwiper>
		</view>

	</view>
</template>


<script>
	import zzzTabSwiper from '@/components/zzz-components/zzz-tab-swiper.vue'

	export default {
		components: {
			zzzTabSwiper,
		},
		data() {
			return {
				//待处理图片默认地址
				mainImageDefault: "/static/images/facemagi/350x750.png",
				//指定分组滑动选择组件初始化数据
				tabSwiperData: [{
					name: 'Older Women',
					id: 'tab_older_women',
					mainImageDefault: '',
					images: [{
							url: "/static/images/facemagi/filters/blank-128x128.png",
							id: "tab_ow_00",
							is_pro: false
						},
						{
							url: "/static/images/facemagi/filters/child-01-128x128.jpg",
							id: "tab_ow_01",
							is_pro: false
						},
						{
							url: "/static/images/facemagi/filters/128x128.png",
							id: "tab_ow_02",
							is_pro: true
						},
						{
							url: "/static/images/facemagi/filters/128x128.png",
							id: "tab_ow_03",
							is_pro: true
						}
					]
				}, {
					name: 'Older Man',
					id: 'tab_older_man',
					images: [{
							url: "/static/images/facemagi/filters/blank-128x128.png",
							id: "tab_om_00",
							is_pro: false
						},
						{
							url: "/static/images/facemagi/filters/128x128.png",
							id: "tab_om_01",
							is_pro: true
						},
						{
							url: "http://p0.meituan.net/movie/fc4dd6cd0c6f7db566a128cc05c475355664427.jpg@170w_235h_1e_1c",
							id: "tab_om_02",
							is_pro: true
						}
					]
				}, {
					name: 'Younger Girl',
					id: 'tab_younger_girl',
					images: [{
							url: "/static/images/facemagi/filters/blank-128x128.png",
							id: "tab_yg_00",
							is_pro: false
						},
					]
				}, {
					name: 'Younger Boy',
					id: 'tab_younger_boy',
					images: [{
							url: "/static/images/facemagi/filters/blank-128x128.png",
							id: "tab_yb_00",
							is_pro: false
						},
					]
				}, {
					name: 'Child',
					id: 'tab_child',
					images: [{
							url: "/static/images/facemagi/filters/blank-128x128.png",
							id: "tab_chl_00",
							is_pro: false
						},
						{
							url: "/static/images/facemagi/filters/child-01-128x128.jpg",
							id: "tab_chl_01",
							is_pro: true
						},
						{
							url: "/static/images/facemagi/filters/128x128.png",
							id: "tab_chl_02",
							is_pro: true
						}
					]
				}],
			}
		},
		computed: {
			i18n() {
				return this.$t('index');
			},
		},
		methods: {
			onclickimg(imgviewobj, mainImage) {
				if (imgviewobj.id != undefined)
					console.log('--> onclickimg(): 选择了滤镜 ' + imgviewobj.id + ', 图片地址:' + mainImage);
			}
		}
	}
</script>

<style>
	page {
		/*background-color: #aaaaaa;*/
	}

	view {
		/*font-size: 28upx;*/
		line-height: inherit
	}

	zzz-tab-swiper {
		/*
		position: absolute;
		top: 0px;
		bottom: 0px;
		left: 0px;
		width: 100%;
		height: 100%; */
	}

	.set-bottom {
		position: fixed;
		bottom: 0;
		width: 100%;
		margin: 0;
		padding: 0;
	}
</style>
