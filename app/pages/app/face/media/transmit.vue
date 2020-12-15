<template>
	<view>
		<view class="">
			<view class="padding-top-xl cu-bar bg-white">
				<view class="action">
				</view>
				<view class="text-xl text-bold">
					{{ app_name }}
				</view>
				<view class="action">
				</view>
			</view>
		</view>
		
		<view class="cropper-wrapper">
			<image :style="{width:cropperOpt.width+'px', height:cropperOpt.height+'px', filter:cropperOpt.filter, transform:cropperOpt.transform}" mode="aspectFill" :src="imageRead" @error="imageError"></image>
		</view>
		
		<view class="cropper-buttons" :style="{visibility:cropperButtonsVisibility}">
			<view class="half padding flex flex-direction">
				<button class="cu-btn lg" @tap="goBack">{{ i18n.back }}</button>
			</view>
			<view class="half padding flex flex-direction">
				<button class="cu-btn lg" @tap="processMediaRemote">{{ i18n.Continue }}</button>
			</view>
		</view>

	</view>
</template>

<script>
	import apiFacemagi from '@/common/api/facemagi'; //与服务端的图片交互
	//import avatar from "@/components/yq-avatar/yq-avatar.vue";
	//import weCropper from '@/common/weCropper.js';
	//import { handleMediaFile } from '@/common/image-process-tools.min.js';
	import imageTool from '@/common/image_tool.js';
	import compressImage from '@/common/image_util.js';
	
	const device = uni.getSystemInfoSync();
	//console.log('--> device:', device);
	
	export default {
		components: {
			//avatar
		},
		data() {
			return {
				gLoginInfo: this.gLoginInfo,
				cropperOpt: {
					width: device.windowWidth,
					height: device.windowHeight - 100,
					//height: device.windowWidth * 5/4,
					filter: "",
					transform: ""
				},
				cropperButtonsVisibility: 'visible', // visible, hidden
				imageStyle: "transform: scale(1.0);",
				imageRead: "../../../../static/photo.jpg",
				imageUpload: null,
				demoIdx: null
			}
		},
		onLoad(options) {
			//console.log('--> options:', options);
			this.imageRead = decodeURIComponent(options.image);
			console.log('recieved image: ' + this.imageRead);
			if ('demo_idx' in options) {
				this.demoIdx = options.demo_idx;
				console.log('recieved demo_idx:', options.demo_idx);
			}
			
			let that = this;
			uni.getImageInfo({
				src: this.imageRead,
				success: async function (image) {
					console.log('getImageInfo() width:' + image.width + ', height:' + image.height + ', orientation:' + image.orientation + ', path:' + image.path);
					
					//方式 2：自动旋转压缩后上传
					let tempPath = null;
					//在运行期，可使用 uni.getSystemInfoSync().platform 判断客户端环境是 Android、iOS 还是小程序开发工具（在百度、微信或支付宝小程序开发工具中返回值均为 devtools）。
					switch(uni.getSystemInfoSync().platform){
						case 'android':
						case 'ios':
							console.log('运行iOS上，使用基于 app plus 的方法');
							tempPath = await compressImage(image.path, device.platform);
							that.imageUpload = tempPath;
							that.processMediaRemote(); //真机上已经有过选择确认了，直接下一步
							break;
						default: //'other'
							console.log('运行在开发者工具上，使用基于 H5 的方法'); //如各种小程序
							imageTool.imageCompress({
								url: that.imageRead,
								success: function(e) {
									//console.log('--> e:', e) //e 为图片 base64
									//"data:image/png;base64,XFOY5SGLYS3KLHB923bkHG..."
									that.imageUpload = e;
									//base64 转图片，替换屏幕图片
									//that.imageRead = imageTool.base64ToBlob(e, "image/png");
									//that.imageRead = imageTool.dataURLtoFile(e);
									//使用 base64 图片上传
									that.imageRead = e;
									//console.log('--> that.imageRead:', that.imageRead);
								}
							});
							break;
					}
					
					//方式 3：直接使用原始图片文件上传
					//that.imageUpload = that.imageRead;
				}
			});
		},
		computed: {
			i18n() {
				return this.$t('index');
			},
		},
		methods: {
			//调用 i18n 翻译，用于 script 中
			translate(e) {
				return this.$t('index')[e];
			},
			
			goBack() {
				uni.navigateBack({
					delta: 1
				});
			},
			
			imageError: function(e) {
				console.error('image error: ' + e.detail.errMsg);
			},
			
			taskProcessSuccess(res_data, i18n_msg) {
				//存储返回的图片信息到本地，并进入编辑页面
				let imageKey = "image_norm";
				uni.setStorage({
					key: imageKey,
					data: res_data['image'],
					success: function(e) {
						apiFacemagi.setStorageValue("image_save_editor", res_data['image']);
						apiFacemagi.setStorageValue("image_save_art", res_data['image']);
						uni.setStorage({
							key: 'm_id',
							data: res_data['m_id'],
							success: function(e) {
								uni.setStorage({
									key: 'attr_dict',
									data: JSON.parse(res_data['msg']),
									success: function(e) {
										uni.hideLoading();
										uni.navigateTo({
											url: '/pages/app/face/media/editor?imageKey=' + imageKey
										});
									}
								});
							}
						});
					}
				});
			},
			taskProcessFail() {
				this.cropperButtonsVisibility = 'visible';
			},
			
			//上传图片到后端做归一化处理
			async processMediaRemote() {
				this.cropperButtonsVisibility = 'hidden';
				
				//动态设置图片模糊
				this.cropperOpt.filter = "blur(30px)";
				this.cropperOpt.transform = "scale(1.2)";
				
				let tk = "harekrishna10800"; //访问令牌（原则上应在登录后由后端动态生成）
				let m_id = null; //新提交图片，取值为空
				let m_path = this.imageUpload; //新提交图片，指定文件路径
				let user_id = apiFacemagi.getUserIdLocal();
				let func_group = null; //上传后进行的处理分类，新提交图片为空
				let func_class = null; //上传后进行的处理类型，新提交图片为空
				let func_name = null; //上传后进行的处理名称，新提交图片为空
				let func_params = null; //上传后进行的处理参数，新提交图片为空
				let i18n_msg = { //多语言支持
					'api_processing': this.translate('api_processing'),
					'api_failed':  this.translate('api_failed'),
					'api_process_timeout': this.translate('api_process_timeout'),
					'api_add_task_err': this.translate('api_add_task_err'),
					'api_query_task_err': this.translate('api_query_task_err'),
					'api_msg_cannot_process': this.translate('api_msg_cannot_process')
				}
				apiFacemagi.taskProcess(tk, m_id, m_path, user_id,
						func_group, func_class, func_name, func_params, 
						i18n_msg, this.demoIdx)
				.then((res_data, i18n_msg) => {
					this.taskProcessSuccess(res_data, i18n_msg);
				})
				.catch((e) => {
					console.log(JSON.stringify(e));
					uni.showModal({
						title: '',
						content: this.translate('msg_check_network_try_again'),
						showCancel: false,
						confirmText: 'Confirm',
						success: () => {}
					});
					this.taskProcessFail();
				});
			}
		}
	}
</script>

<style>
	page {
		/*background-color: #3a3a3a;*/
	}

	.cropper {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
	}
	
	.cropper-wrapper {
		position: relative;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		width: 100%;
		/*background-color: #7F7F7F;*/
		overflow: hidden;
	}
	
	.cropper-buttons {
		background-color: #C4C4C4;
		color: #010101;
		width: 100vw;
		height: 140rpx;
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		position: fixed;
		bottom: 0;
		left: 0;
		line-height: 120rpx;
	}
	
	.cropper-buttons .half {
		/*background-color: #3F3F3F;*/
		width: 50%;
		text-align: center;
	}
</style>
