<template>
	<view class="ts-row ts-flex-item">
		<!-- #ifdef APP-PLUS -->
		<view class="ts-row ts-padding ts-center" v-if="providerList.length > 0">
			<block v-for="(value,index) in providerList" :key="index">
				<view class="ts-row">
					<view class="ts-padding">
						<image v-if="value" :style="{width:iconSize_,height: iconSize_}" :src="'/static/app-plus/providers/'+value.id+'.png'"
						 @tap="share(value)" />
						</image>
					</view>
				</view>
			</block>
		</view>
		<!-- #endif -->
	</view>
</template>
<script>
	export default {
		name: 'ts-share-buttons',
		props: {
			iconSize: {
				type: Number,
				default: 80 //upx
			},
			//系统支持的服务供应商
			providerList: {
				type: Array,
				default () {
					return []
				}
			},
			//配置项
			shareOptions: {
				type: Object,
				default () {
					return {
						shareType: 0,
						shareImage: 'https://img-cdn-qiniu.dcloud.net.cn/uniapp/app/share-logo@3.png',
						shareTitle: '欢迎体验优职道',
						shareText: '专注在校学生的实习、就业，破解企业招工难题，提供精准就业、精准招聘服务！',
						shareLink: 'http://www.zengqs.com', //生成的二维码的链接，点解分享链接到改页面
						miniProgram: {
							id: 'wx86ab541f20e43dc4',
							path: '/pages/tabbar/home/index',
							webUrl: 'http://www.zengqs.com',
							type: 0
						}
					}
				}
			}
		},
		data() {
			return {}
		},
		computed: {
			iconSize_() {
				return uni.upx2px(this.iconSize) + 'px';
			}
		},
		methods: {
			// #ifdef APP-PLUS
			async share(e) {
				console.log('分享通道:' + e.id + '； 分享类型:' + this.shareType);
				if (!this.shareOptions.shareText && (this.shareOptions.shareType === 1 || this.shareOptions.shareType === 0)) {
					uni.showModal({
						content: '分享内容不能为空',
						showCancel: false
					})
					return;
				}

				if (!this.shareOptions.shareImage && (this.shareOptions.shareType === 2 || this.shareOptions.shareType === 0)) {
					uni.showModal({
						content: '分享图片不能为空',
						showCancel: false
					})
					return;
				}

				if (e.id === 'qq') {
					this.shareOptions.shareType = 1; //QQ不支持图文分享
				}

				let shareOptions = {
					provider: e.id,
					scene: e.type && e.type === 'WXSenceTimeline' ? 'WXSenceTimeline' : 'WXSceneSession',
					//WXSceneSession”分享到聊天界面，“WXSenceTimeline”分享到朋友圈，“WXSceneFavorite”分享到微信收藏     
					type: this.shareOptions.shareType,
					success: (e) => {
						console.log('success', e);
						uni.showModal({
							content: '分享成功',
							showCancel: false
						})
					},
					fail: (e) => {
						console.log('fail', e)
						//             uni.showModal({
						//               content: e.errMsg,
						//               showCancel: false
						//             })
					},
					complete: function() {
						console.log('分享操作结束!')
					}
				}

				switch (this.shareOptions.shareType) {
					case 0: //图文
						shareOptions.summary = this.shareOptions.shareText;
						shareOptions.imageUrl = this.shareOptions.shareImage;
						shareOptions.title = this.shareOptions.shareTitle;
						shareOptions.href = this.shareOptions.shareLink;
						break;
					case 1: //纯文字
						shareOptions.summary = this.shareOptions.shareText;
						break;
					case 2: //纯图片
						shareOptions.imageUrl = this.shareOptions.shareImage;
						break;
					case 5: //小程序
						shareOptions.imageUrl = this.shareOptions.shareImage;
						shareOptions.title = this.shareOptions.shareTitle;
						shareOptions.miniProgram = {
							id: 'wx86ab541f20e43dc4',
							path: '/pages/tabbar/home/index',
							webUrl: this.shareOptions.shareLink,
							type: 0
						};
						break;
					default:
						break;
				}

				if (shareOptions.type === 0 && plus.os.name === 'iOS') { //如果是图文分享，且是ios平台，则压缩图片 
					shareOptions.imageUrl = this.compress();
				}
				if (shareOptions.type === 1 && shareOptions.provider === 'qq') { //如果是分享文字到qq，则必须加上href和title
					shareOptions.href = this.shareOptions.shareLink;
					shareOptions.title = this.shareOptions.shareTitle;
				}

				uni.share(shareOptions);
			},

			compress() { //压缩图片 图文分享要求分享图片大小不能超过20Kb
				console.log('开始压缩');
				let img = this.shareOptions.shareImage;
				return new Promise((res) => {
					var localPath = plus.io.convertAbsoluteFileSystem(img.replace('file://', ''));
					console.log('after' + localPath);
					// 压缩size
					plus.io.resolveLocalFileSystemURL(localPath, (entry) => {
						entry.file((file) => { // 可通过entry对象操作图片 
							console.log('getFile:' + JSON.stringify(file));
							if (file.size > 20480) { // 压缩后size 大于20Kb
								plus.zip.compressImage({
									src: img,
									dst: img.replace('.jpg', '2222.jpg').replace('.JPG', '2222.JPG'),
									width: '10%',
									height: '10%',
									quality: 1,
									overwrite: true
								}, (event) => {
									console.log('success zip****' + event.size);
									let newImg = img.replace('.jpg', '2222.jpg').replace('.JPG', '2222.JPG');
									res(newImg);
								}, function(error) {
									//                   uni.showModal({
									//                     content: '分享图片太大,需要请重新选择图片!',
									//                     showCancel: false
									//                   })
								});
							}
						});
					}, (e) => {
						console.log('Resolve file URL failed: ' + e.message);
						//             uni.showModal({
						//               content: '分享图片太大,需要请重新选择图片!',
						//               showCancel: false
						//             })
					});
				})
			},
			// #endif
		},
	}
</script>
<style lang="scss" scoped>

</style>
