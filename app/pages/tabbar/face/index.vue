<template>
	<view>
		<view class="">
			<view class="padding-top-xl cu-bar bg-white">
				<view class="action">
					<text class="cuIcon-settings text-xl text-bold shadow" @click="showSettings" data-target="DialogModal1"></text>
				</view>
				<view class="text-xl text-bold">
					{{ app_name }}
				</view>
				<view class="action">
					<button class="cu-btn round sm bg-orange" @click="showModal" data-target="DialogModal2">PRO</button>
				</view>
			</view>
		</view>
		
		<view class="cu-modal" :class="modalName=='DialogModal1'?'show':''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">{{ i18n.settings }}</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-red"></text>
					</view>
				</view>
				<view class="padding">
					<view class="cu-list menu text-left">
						<view class="cu-item">
							<text class="">{{ i18n.version }} - {{ sysInfoVersion }} ({{ sysInfoVersionCode }})</text>
						</view>
						<view class="cu-item">
							<view class="content">
								<text class="cuIcon-favor" />
								<text class="text-xl text-bold" @tap="commentApp()">{{ i18n.comment_app }}</text>
							</view>
						</view>
						<view class="cu-item">
							<view class="content">
								<text class="cuIcon-forward" />
								<text class="text-xl text-bold" @tap="shareApp()">{{ i18n.share_app }}</text>
							</view>
						</view>
						<view class="cu-item">
							<view class="content">
								<text class="cuIcon-moneybag" />
								<text class="text-xl text-bold" @tap="getPaid()">{{ i18n.restore_paid }}</text>
							</view>
						</view>
						<view class="cu-item">
						</view>
						<view class="cu-item padding-top">
							<view class="content text-center">
								<text class="text-blue text-df" style="text-decoration: underline;" @tap="openUrl('https://www.facemagi.com/privacy/privacy-en.html')">{{ i18n.privacy }}</text>
								<text class="text-white">---</text>
								<text class="text-blue text-df" style="text-decoration: underline;" @tap="openUrl('https://www.facemagi.com/terms.html')">{{ i18n.terms }}</text>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="cu-modal" :class="modalName=='DialogModal2'?'show':''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">{{ i18n.subscription_title }}</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-red"></text>
					</view>
				</view>
				<view class="padding">
					<view class="cu-list">
						<view class="cu-item">
							<view class="content text-left">
								<text class="text-xl text-bold">{{ i18n.subscription_banner1 }}</text><br />
								<text class="text">{{ i18n.subscription_banner2 }}</text>
							</view>
						</view>
						<view class="cu-item">
							<view class="padding-top-xl">
								<view class="padding-sm round bg-gradual-pink" style="hight: 20rpx;" @click="execLoginAndIAP">
									<view class="content"><text class="text-xl text-bold">{{ i18n.subscription_button_text1 }}</text></view>
									<view class="content"><text class="text-sm">{{ i18n.subscription_button_text2 }}</text></view>
								</view>
							</view>
						</view>
						<view class="cu-item">
							<view class="content padding text-shadow">
								<text class="text-sm text-bold text-gray" style="text-decoration: underline;" @tap="getPaid()">{{ i18n.restore_paid }}</text>
							</view>
						</view>
						<view class="cu-item">
							<view class="content">
								<text class="text-sm text-grey padding-xs" style="line-height: 0.5">
								{{ i18n.subscription_description }}
								</text>
							</view>
						</view>
						<view class="cu-item padding-top">
							<view class="content">
								<text class="text-blue text-df" style="text-decoration: underline;" @tap="openUrl('https://www.facemagi.com/privacy/privacy-en.html')">{{ i18n.privacy }}</text>
								<text class="text-white">---</text>
								<text class="text-blue text-df" style="text-decoration: underline;" @tap="openUrl('https://www.facemagi.com/terms.html')">{{ i18n.terms }}</text>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
		
		<view class="cu-modal drawer-modal justify-end" :class="modalName=='DrawerModalR'?'show':''" @tap="hideModal()">
			<view class="cu-dialog basis-lg" @tap.stop="" :style="[{top:CustomBar+'px',height:'calc(100vh - ' + CustomBar + 'px)'}]">
				
			</view>
		</view>
		
		<view class="bg-gradual-pink padding radius shadow-blur">
			<view class="padding-md text-white">
				<view class="padding-xs text-lg">
					{{ i18n.app_advert }}
				</view>
			</view>
		</view>

		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				{{ i18n.face_demo }}
			</view>
		</view>
		<view class="bg-white padding">
			<view class="grid col-4 grid-square">
				<view class="bg-img" v-for="(item,index) in demo_faces" :key="index" @tap="goTransmit(item, index, 'face_demo')"
				 :style="[{ backgroundImage:'url(' + demo_faces[index] + ')' }]"></view>
			</view>
		</view>

		<view class="cu-bar bg-white solid-bottom margin-top">
			<view class="action">
				{{ i18n.face_photo }}
			</view>
		</view>
		<view class="bg-white padding">
			<view class="grid col-4 grid-square">
				<view class="bg-img" v-for="(item,index) in data2" :key="index" @tap="goTransmit(item, index, 'face_photo')" :style="[{ backgroundImage:'url(' + data2[index] + ')' }]"></view>
			</view>
		</view>
		
		<view class="cu-bar margin-top">
			<!-- 广告联盟-应用内展示的广告组件 (TODO: adpid需使用增强广告位替换)-->
			<view class="ad-view">
				<ad adpid="1111111111" @load="" @close="" @error="" @downloadchange=""></ad>
			</view>
		</view>
		
	</view>
</template>

<script>
	import Vue from 'vue';
	import apiFacemagi from '@/common/api/facemagi';
	import config from '@/common/api/config';
	import uniGrid from '@/components/uni-grid/uni-grid.vue';
	import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue';
	//import uniIcon from '@/components/uni-icon/uni-icon.vue';
	import permission from '@/js_sdk/wa-permission/permission.js';
	import payment from '@/common/payment.js';
	import plusShare from '@/js_sdk/plusShare.js';
	
	export default {
		components: {
			uniNavBar,
			//uniIcon,
			uniGrid
		},
		data() {
			return {
				FaceMakeupList: this.FaceMakeupList,
				FaceCreativeList: this.FaceCreativeList,
				data2: [
					'/static/images/ui/face-album-7.png',
					'/static/images/ui/face-camera-7.png'
				],
				demo_faces: [],
				CustomBar: this.CustomBar,
				modalName: null,
				sysInfoVersion: '',
				sysInfoVersionCode: ''
			}
		},
		onPullDownRefresh() {
			setTimeout(() => {
				uni.stopPullDownRefresh()
			}, 1000)
		},
		onLoad(options) {
			/* //存储调试代码：
			try {
				//同步获取本地存储相关信息
				//const res = uni.getStorageInfoSync();
				//console.log("keys", res.keys);
				//console.log("currentSize:", res.currentSize);
				//console.log("limitSize", res.limitSize);
				
				//清除本地存储数据
				//uni.clearStorageSync();
				
				//修改、新增本地存储键值
				//uni.setStorageSync('keyname', {'ver':'unset'});
			} catch (e) {
				// error
			}
			*/
			//uni.clearStorageSync();
			
			//设置默认的后端服务器地址
			Vue.prototype.$BASE_URL = 'http://54.193.181.205:8087';
			Vue.prototype.$API_URL = 'http://54.193.181.205:8087' + '/api/v1';
			//this.getDemoFaces();
			
			//根据 App Store Review Guidelines 3.1.2 要求：如果您提供自动续订订阅，则必须为客户提供持续的价值，订阅期必须持续至少七天，并且能够在用户的所有设备上访问。
			//https://developer.apple.com/cn/app-store/review/guidelines/
			let ios_user_info = apiFacemagi.getStorageValue('ios_user_info');
			if (ios_user_info) {
				console.log('--> ios_user_info: ' + JSON.stringify(ios_user_info));
				Vue.prototype.apple_user_id = ios_user_info.user_id;
			}
			
			//获取基本配置并执行后端登录（后端部分接口需要登录才可以调用）
			apiFacemagi.getBaseCfg()
			.then((baseCfg) => {
				//console.log('获取远程配置成功：' + JSON.stringify(baseCfg));
				this.getDemoFaces();
				apiFacemagi.execUserLogin()
				.then(() => {
					if (Vue.prototype.app_start_notice_viewed == false) {
						uni.showModal({
							title: this.translate('notice'),
							content: this.translate('app_start_notice'),
							showCancel: false,
							confirmText: this.translate('confirm'),
							success: () => {
								Vue.prototype.app_start_notice_viewed = true;
							}
						});
					}
				});
			})
			.catch(() => {
				this.getDemoFaces();
				uni.showModal({
					title: this.translate('msg_get_confg_fail'),
					content: this.translate('msg_check_network'),
					showCancel: false,
					confirmText: this.translate('confirm'),
					success: () => {
						apiFacemagi.exitApp();
					}
				});
			});
		},
		onReachBottom() {},
		computed: {
			i18n() {
				return this.$t('index');
			},
		},
		created() {},
		methods: {
			//调用 i18n 翻译，用于 script 中
			translate(e) {
				return this.$t('index')[e];
			},
			
			hideModal(e) {
				this.modalName = null;
				uni.hideLoading();
			},
			showModal(e) {
				this.modalName = e.currentTarget.dataset.target;
			},
			showSettings(e) {
				/*
				let res = uni.getSystemInfoSync();
				console.log('  version:' + res.version); //1.9.9.74105
				console.log('  platform:' + res.platform); //ios
				console.log('  system:' + res.system); //13.4
				this.sysInfoVersion = res.version;
				*/
				// #ifdef APP-PLUS
				plus.runtime.getProperty(plus.runtime.appid, (wgtinfo) => {
					console.log(JSON.stringify(wgtinfo));
					//console.log(wgtinfo.version); //应用版本号
					this.sysInfoVersion = wgtinfo.version;
					this.sysInfoVersionCode = wgtinfo.versionCode;
				});
				// #endif
				this.showModal(e);
			},
			
			//从服务端获取系统支持的演示人脸数据
			getDemoFaces() {
				let res = apiFacemagi.getDemoList()
				.then((res) => {
					//console.log('--> getDemoList res:' + JSON.stringify(res));
					const data = res.data;
					//console.log('--> data:' + data);
					if (data) {
						let _this = this;
						
						function download_demo_faces(data) {
							let _demo_faces = {};
							let _retried = 0;
							
							function set_demo_faces() {
								_this.demo_faces = [];
								for(let j = 0; j < data.demo_list.length; j++){
									_this.demo_faces.push(_demo_faces[j]);
								}
							}
							
							for (let i = 0, length = data.demo_list.length; i < length; i++) {
								//this.demo_faces.push(Vue.prototype.$BASE_URL + data.demo_list[i]);
								//检查临时下载路径是否有保存，如有则检查是否有已下载文件
								//若有则直接使用，否则执行下载并保存临时下载路径
								if (Vue.prototype.demoFacesSaveDir != null) {
									_demo_faces[i] = Vue.prototype.demoFacesSaveDir + '/' + Vue.prototype.demoFacesFileNames[i];
									console.log('--> 使用已下载缓存：' + _demo_faces[i]);
									set_demo_faces();
								} else {
									uni.downloadFile({
										url: Vue.prototype.$BASE_URL + data.demo_list[i],
										success: (res) => {
											if (res.statusCode === 200) {
												//console.log('下载成功 ' + i + ': ' + res.tempFilePath);
												let str = res.tempFilePath;
												let obj = str.lastIndexOf("/");
												Vue.prototype.demoFacesSaveDir = str.substr(0, obj);
												Vue.prototype.demoFacesFileNames[i] = str.substr(obj + 1);
												
												// #ifdef H5
												_demo_faces[i] = res.tempFilePath;
												set_demo_faces();
												// #endif
												// #ifndef H5
												uni.saveFile({
													tempFilePath: res.tempFilePath,
													success: function (res) {
														_demo_faces[i] = res.savedFilePath;
														set_demo_faces();
													}
												});
												// #endif
											} else {
												console.log('下载失败 ' + res.statusCode);
												//_retried += 1;
												//if (_retried <= 1) {
												//	setTimeout(() => {
												//		download_demo_faces(data);
												//	}, 2000);
												//}
											}
										},
										fail: (res) => {
											console.log('下载失败 ' + '无法访问服务器');
											//_retried += 1;
											//if (_retried <= 1) {
											//	setTimeout(() => {
											//		download_demo_faces(data);
											//	}, 2000);
											//}
										}
									});
								}
								
							}
						}
						
						download_demo_faces(data);
					}
				}).catch((e) => {
					console.log('getDemoList faile: ' + JSON.stringify(e));
					uni.showToast({
						title: this.translate('msg_check_network'),
						duration: 2000,
						icon: 'none'
					});
					
					setTimeout(() => {
						this.getDemoFaces();
					}, 5000);
				});
			},

			//转到下一个处理页面
			goTransmit(item, index, category) {
				console.log('--> goTransmit() item:' + item + ' index:' + index + ' category:' + category);
				let url_prefix = '/pages/app/face/media/transmit?';
				if ('face_demo' === category) {
					url_prefix += 'demo_idx=' + index + '&';
					/* //重新根据图片 url 下载
					uni.showLoading();
					uni.downloadFile({
						url: item,
						success: (res) => {
							uni.hideLoading();
							if (res.statusCode === 200) {
								uni.navigateTo({
									url: url_prefix + 'image=' + encodeURIComponent(res.tempFilePath)
								});
							}
						},
						fail: (res) => {
							uni.hideLoading();
							uni.showModal({
								title: this.translate('network_error'),
								content: this.translate('please_try_later'),
								showCancel: false,
								confirmText: 'Confirm',
								cancelText: 'Cancel',
								success: function (res) {}
							});
						}
					});
					*/
					//直接使用本地已缓存图片路径
					uni.navigateTo({
						url: url_prefix + 'image=' + encodeURIComponent(this.demo_faces[index])
					});
				} else if ('face_photo' === category) {
					if (0 === index) {
						uni.chooseImage({
							count: 1,
							sizeType: ['original', 'compressed'], //'original', 'compressed'] 或其中之一
							sourceType: ['album'],
							success: function(res) {
								//console.log('photo path:', JSON.stringify(res.tempFilePaths[0]))
								uni.navigateTo({
									url: url_prefix + 'image=' + encodeURIComponent(res.tempFilePaths[0])
								});
							}
						});
					} else if (1 === index) {
						// #ifdef APP-PLUS
						let c = plus.camera.getCamera();
						console.log('使用 plus 拍照。支持分辨率：' + c.supportedImageResolutions);
						c.captureImage(function(e) {
							plus.io.resolveLocalFileSystemURL(e, function(entry) {
								let s = entry.toLocalURL();
								console.log('应用拍照文件：' + JSON.stringify(s))
								uni.navigateTo({
									url: url_prefix + 'image=' + encodeURIComponent(s)
								});
							}, function(e) {
								console.log("读取拍照文件错误：" + e.message);
							});
						}, function(e) {
							console.log("拍照错误：" + e.message);
						}, {
							//filename: "_doc/camera.png",
							resolution: "high", //640*480,1280*720,960*540,high,medium,low（在 ip8p 上使用 high 前摄获取的照片分辨率为 2576x1932，压缩后约 250KB）
							filter: "image"
						})
						// #endif
						// #ifndef APP-PLUS
						uni.chooseImage({
							count: 1,
							sizeType: ['original', 'compressed'], //['original', 'compressed']
							sourceType: ['camera'],
							success: function(res) {
								//console.log('photo path:', JSON.stringify(res.tempFilePaths[0]))
								/* uni.getImageInfo({
									src: res.tempFilePaths[0],
									success: function(image) {
										console.log("图片路径:" + image.path);
									}
								}) */
								uni.navigateTo({
									url: url_prefix + 'image=' + encodeURIComponent(res.tempFilePaths[0])
								});
							}
						});
						// #endif
					}
				}
			},

			//打开外部超链接
			openUrl(url) {
				// #ifdef APP-PLUS
				plus.runtime.openURL(url, function(res) {
					console.log('openUrl(): 外部调用 ' + res);
				});
				// #endif
				// #ifndef APP-PLUS
				console.log('openUrl(): 平台不支持该外部调用');
				// #endif
			},
			
			//在应用商店评价
			commentApp(marketPackageName) {
				// #ifdef APP-PLUS
				let appUrl = null;
				if (plus.os.name == "Android") {
					appUrl = "market://details?id=io.dcloud.HelloH5"; //由于hello uni-app没有上Android应用商店，所以此处打开了另一个示例应用
				}
				else {
					//appUrl = "itms-apps://itunes.apple.com/cn/app/hello-uni-app/id1417078253?mt=8";
					appUrl = "itms-apps://itunes.apple.com/us/app/facemagi/id1502256892"; //TODO: 改为本应用地址
				}
				if (typeof(marketPackageName) == "undefined") {
					plus.runtime.openURL(appUrl, function(res) {
						console.log(res);
					});
				} else { //强制指定某个Android应用市场的包名，通过这个包名启动指定app
					if (plus.os.name == "Android") {
						plus.runtime.openURL(appUrl, function(res) {
							plus.nativeUI.alert("本机没有安装应用宝");
						}, marketPackageName);
					} else {
						plus.nativeUI.alert("仅Android手机才支持应用宝");
					}
				}
				// #endif
				// #ifndef APP-PLUS
				console.log('openUrl(): 平台不支持应用市场评论操作');
				// #endif
			},
			
			//分享应用
			shareApp() {
				// #ifdef APP-PLUS
				let message = {
					type: 'image/png',
					content: 'FaceMagi - ' + this.translate('app_advert'),
					title: 'FaceMagi', //应用名字
					href: this.translate('app_store_href'), //分享出去后点击跳转，如 https://apps.apple.com/cn/app/hello-uni-app/id1417078253?mt=8
					thumbs: ["http://www.facemagi.com/icons/120x120.png"] //分享缩略图
				}
				//调起分享
				plusShare.plusShare(message, function(res) {
					//分享回调函数
					if(res) {
						//plus.nativeUI.toast("sharing success");
						uni.showToast({
							title: this.translate('sharing_success'),
							mask: false,
							duration: 1500
						});
					} else {
						//plus.nativeUI.toast("sharing fail");
						uni.showToast({
							title: this.translate('sharing fail'),
							mask: false,
							duration: 1500
						});
					}
				})
				// #endif
				// #ifndef APP-PLUS
				console.log('openUrl(): 平台不支持分享操作');
				// #endif
			},
			
			//远程获取和更新已购项
			getPaid() {
				apiFacemagi.checkApplLogin()
				.then((res) => {
					apiFacemagi.updatePaidCache()
					.then((res) => {
						console.log('远程获取已购项成功！' + JSON.stringify(res));
					})
					.catch((e) => {
						console.log('远程获取已购项失败！' + JSON.stringify(e));
					});
				})
				.catch((e) => {
				});
			},
			
			execLoginAndIAP() {
				apiFacemagi.checkApplLogin()
				.then((res) => {
					//检查权限缓存
					if (apiFacemagi.checkPaidCache()) {
						//用户已有权限，无需执行内购
						uni.showModal({
							confirmText: this.translate('confirm'),
							content: this.translate('msg_paid_valid'),
							showCancel: false
						});
					} else {
						//没有权限，执行内购
						apiFacemagi.execAppleIAP()
						.then((res) => {
							uni.showModal({
								confirmText: this.translate('confirm'),
								content: this.translate('msg_purchase_success'),
								showCancel: false
							});
						})
						.catch((e) => {
							uni.showModal({
								confirmText: this.translate('confirm'),
								content: this.translate('msg_purchase_failed'),
								showCancel: false
							});
						});
					}
				})
				.catch((e) => {
				});
			}
		},
	}
</script>

<style lang="scss">
	.example {
		padding: 0 5upx 5upx
	}
</style>
