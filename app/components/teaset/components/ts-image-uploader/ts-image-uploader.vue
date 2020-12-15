<template>
	<view class="ts-uploader-wraper">
		<view class="ts-uploader">
			<view class="ts-uploader-head">
				<view class="ts-uploader-title">
					<slot>
						<text class="ts-h5">点击预览图片</text>
					</slot>
				</view>
				<view class="ts-uploader-info ts-h5">{{imageList.length}}/{{count}}</view>
			</view>
			<view class="ts-uploader-body">
				<view class="ts-uploader__files">
					<block v-for="(image,index) in imageList" :key="index">
						<view class="ts-uploader__file">
							<image class="ts-uploader__img" :src="image.path" @tap="previewImage" @longpress="removeImage(image.path)"></image>
						</view>
					</block>
					<view class="ts-uploader__input-box">
						<view class="ts-uploader__input" @tap="chooseImg"></view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		pathToBase64,
		base64ToPath,
		md5
	} from "../../common/helper/index.js";

	var self;
	export default {
		props: {
			count: {
				type: Number,
				default: 9
			}
		},
		data() {
			return {
				imageList: []
			};
		},
		methods: {
			async chooseImg() {
				//选择图片
				uni.chooseImage({
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album', 'camera'], //从相册选择
					count: this.count - this.imageList.length, //H5 平台，手机浏览器不能限制数量
					success: async (res) => {

						for (let img of res.tempFilePaths) {
							let checksum = md5(await pathToBase64(img)); //通过计算图形的校验值赖判断是否是同名图片
							// console.log(checksum)
							let index = this.imageList.findIndex(item => item.md5 === checksum);
							if (index === -1) {
								this.imageList.push({
									path: img,
									md5: checksum
								});
							}
						}

						// console.log(this.imageList)
						//触发所选择文件更改事件，参数为文件列表
						let data = [];
						for (let image of this.imageList) {
							data.push(image.path)
						}
						this.$emit('change', data);
					}
				});
			},
			removeImage(img) {

				uni.showModal({
					title: '提示',
					content: '确认删除选中的图片？',
					success: (res) => {
						if (res.confirm) {
							const index = this.imageList.findIndex(item => item === img);
							this.imageList.splice(index, 1);
						} else if (res.cancel) {
							//
						}
					}
				});
			},
			previewImage() {
				//预览图片
										let data = [];
				for (let image of this.imageList) {
					data.push(image.path)
				}
				
				uni.previewImage({
					urls: data
				});
			}
		}
	};
</script>

<style scoped>
	.ts-uploader-wraper {
		display: flex;
		flex-direction: column;
		flex: 1;
		padding: 22upx 20upx;
	}

	.ts-uploader {
		display: flex;
		flex: 1;
		flex-direction: column;
	}

	.ts-uploader-head {
		display: flex;
		flex-direction: row;
		justify-content: space-between;
	}

	.ts-uploader-info {
		color: #b2b2b2;
	}

	.ts-uploader-body {
		margin-top: 16upx;
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.ts-uploader__files {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
	}

	.ts-uploader__file {
		display: flex;
		flex-direction: row;
		margin-right: 18upx;
		margin-bottom: 18upx;
	}

	.ts-uploader__img {
		display: flex;
		flex-direction: row;
		width: 158upx;
		height: 158upx;
	}

	.ts-uploader__input-box {
		float: left;
		position: relative;
		margin-right: 18upx;
		margin-bottom: 18upx;
		width: 154upx;
		height: 154upx;
		border: 2upx solid #d9d9d9;
	}

	.ts-uploader__input-box:before,
	.ts-uploader__input-box:after {
		content: ' ';
		position: absolute;
		top: 50%;
		left: 50%;
		-webkit-transform: translate(-50%, -50%);
		transform: translate(-50%, -50%);
		background-color: #d9d9d9;
	}

	.ts-uploader__input-box:before {
		width: 4upx;
		height: 79upx;
	}

	.ts-uploader__input-box:after {
		width: 79upx;
		height: 4upx;
	}

	.ts-uploader__input-box:active {
		border-color: #999999;
	}

	.ts-uploader__input-box:active:before,
	.ts-uploader__input-box:active:after {
		background-color: #999999;
	}

	.ts-uploader__input {
		position: absolute;
		z-index: 1;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		opacity: 0;
	}
</style>
