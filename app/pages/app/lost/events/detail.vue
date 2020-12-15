<template>
	<view class="ts-column">
		<view class="banner">
			<image class="banner-img" :mode="imageMode" :src="cover"></image>


			<view class="banner-title">{{pageData.title}}</view>

		</view>

		<view class="ts-section">
			<view class="ts-section-title">
				<view class="ts-row">
					<view class="ts-flex-item" style="align-items: flex-end;">
						<text class="ts-h2 ts-text-bold">{{pageData.linkman}}</text>
						<text class="ts-h6 ts-padding-left">{{pageData.mobile}}</text>
					</view>
					<view style="justify-content: center; align-items: center;">
						<ts-badge :text="pageData.type" type="error"></ts-badge>
					</view>
				</view>
			</view>
			<view class="ts-section-body">
				<view class="ts-row ts-h2 ts-text-bold ts-ellipsis">
					{{pageData.title}}
				</view>

				<view class="ts-row" style="flex-wrap: wrap;">
					{{pageData.description}}
				</view>
				<ts-line></ts-line>
				<view class="ts-row">
					<view>地址：</view>
					<view>{{pageData.address}}</view>
				</view>
				<view class="ts-row">
					<view>时间：</view>
					<view>{{pageData.create_time}}</view>
				</view>


				<view class="ts-column ts-padding-top ts-center" v-for="(img,idx) in pageData.images" :key="idx" @tap="previewImage(pageData.images)">
					<image :src="img" style="width: 100%;" :mode="imageMode"></image>
				</view>


			</view>
		</view>

	</view>
</template>

<script>
	import * as api from "@/common/api/lost"

	function _handleShareChannels(provider) {
		let channels = [];
		for (let i = 0, len = provider.length; i < len; i++) {
			switch (provider[i]) {
				case 'weixin':
					channels.push({
						text: '分享到微信好友',
						id: 'weixin',
						sort: 0
					});
					channels.push({
						text: '分享到微信朋友圈',
						id: 'weixin',
						sort: 1
					});
					break;
				default:
					break;
			}
		}
		channels.sort(function(x, y) {
			return x.sort - y.sort;
		});
		return channels;
	}

	export default {
		data() {
			return {
				title: 'list-triplex-row',
				id: 0, //项目ID
				isLoading: false,

				providerList: [],
				pageData: {
					title: '详情',
				},

				imageMode: 'widthFix',
			}
		},
		computed: {
			cover() {
				if (this.pageData.images && this.pageData.images.length > 0) {
					return this.pageData.images[0];
				} else {
					return 'http://via.placeholder.com/750x250'
				}
			}
		},
		onLoad(e) {
			this.id = parseInt(e.id)
			this.getDetail();
			setTimeout(() => {
				uni.setNavigationBarTitle({
					title: this.pageData.title
				});
			}, 500)
		},
		onShareAppMessage() {
			return {
				title: this.banner.title,
				path: DETAIL_PAGE_PATH + '?detailDate=' + JSON.stringify(this.banner)
			}
		},
		onNavigationBarButtonTap(event) {
			const buttonIndex = event.index;
			if (buttonIndex === 0) {
				// 分享 H5 的页面
				const shareProviders = [];
				uni.getProvider({
					service: 'share',
					success: (result) => {
						// 目前仅考虑分享到微信
						if (result.provider && result.provider.length && ~result.provider.indexOf('weixin')) {
							const channels = _handleShareChannels(result.provider);
							uni.showActionSheet({
								itemList: channels.map(channel => {
									return channel.text;
								}),
								success: (result) => {
									const tapIndex = result.tapIndex;
									uni.share({
										provider: 'weixin',
										type: 0,
										title: this.banner.title,
										scene: tapIndex === 0 ? 'WXSceneSession' : 'WXSenceTimeline',
										href: 'https://uniapp.dcloud.io/h5' + DETAIL_PAGE_PATH + '?detailDate=' + JSON.stringify(this.banner),
										imageUrl: 'https://img-cdn-qiniu.dcloud.net.cn/uniapp/app/share-logo@3.png'
									});
								}
							});
						} else {
							uni.showToast({
								title: '未检测到可用的微信分享服务'
							});
						}
					},
					fail: (error) => {
						uni.showToast({
							title: '获取分享服务失败'
						});
					}
				});
			}
		},
		methods: {
			 previewImage(imageList) {
				//预览图片
				uni.previewImage({
					urls: imageList
				});
			},
			
			getDetail() {
				//阻止重复加载网络请求
				if (this.isLoading) {
					// uni.stopPullDownRefresh();
					return;
				}
				this.isLoading = true;

				api.event.getInfo(this.id, {}).then(res => {
					if (res.errno === 0) {
						this.pageData = res.data;
						this.isLoading = false;
					} else {
						console.log(res.errmsg);
					}
				});

			}
		}
	}
</script>

<style>
	.banner {
		/* height: 360upx; */
		/* overflow: hidden; */
		position: relative;
		background-color: #ccc;
		display: flex;
		flex: 1;
		flex-direction: row;
	}

	.banner-img {
		/* width: 100%; */
		display: flex;
		flex: 1;
	}

	.banner-title-wraper {
		background-color: #ccc;
		height: 100upx;
		flex: 1;
		display: flex;
		flex-direction: row;
		padding: 20upx;
	}

	.banner-title {
		max-height: 84upx;
		overflow: hidden;
		position: absolute;
		/* left: 30upx; */
		bottom: 30upx;
		width: 100%;
		font-size: 32upx;
		font-weight: 400;
		line-height: 42upx;
		color: white;
		z-index: 11;
		font-weight: bold;

		background-color: rgba(0, 0, 0, 0.6);
		padding: 20upx;
	}

	.article-meta {
		padding: 20upx 40upx;
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		color: gray;
	}

	.article-text {
		font-size: 26upx;
		line-height: 50upx;
		margin: 0 20upx;
	}

	.article-author,
	.article-time {
		font-size: 30upx;
	}

	.article-content {
		padding: 0 30upx;
		overflow: hidden;
		font-size: 30upx;
		margin-bottom: 30upx;
	}
</style>
