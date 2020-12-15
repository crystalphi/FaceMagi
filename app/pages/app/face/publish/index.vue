<template>

	<view class="ts-column ts-padding">
		<view class="ts-row">

			<view class="ts-row ts-padding ts-flex-item">
				<ts-button class="ts-flex-item" :borderRadius="30" type="error" :inverted="type!='丢失'" @click="switchType">丢失</ts-button>
			</view>
			<view class="ts-row ts-padding ts-flex-item">
				<ts-button class="ts-flex-item" :borderRadius="30" type="primary" :inverted="type==='丢失'" @click="switchType">捡到</ts-button>
			</view>
		</view>

		<view class="ts-row" style="align-items: center;">
			<view class="ts-row">
				我的名字
			</view>
			<input type="text" v-model="linkman" placeholder="请填写您的姓名" />
		</view>

		<view class="ts-row" style="align-items: center;">

			<view class="ts-row">
				手机号码
			</view>
			<input type="text" v-model="mobile" placeholder="请填写您的手机号码" />
		</view>
		<view class="ts-row" style="align-items: center;">
			<view class="ts-row">
				{{typeMessage}}物品
			</view>
			<input type="text" v-model="title" :placeholder="'请填写'+typeMessage+'物品的名称'" />
		</view>
		<view class="ts-row" style="align-items: center;">
			<view class="ts-row">
				{{typeMessage}}地点
			</view>
			<input type="text" v-model="address" :placeholder="'请填写'+typeMessage+'物品的地点'" />
		</view>

		<view class="ts-column">
			<view class="ts-row">
				{{typeMessage}}物品简单描述
			</view>
			<view class="ts-row" style="flex:1;">
				<textarea v-model="description" style="height: 200upx; border: #3C3E49 solid 1upx; width: 100%; padding: 10upx;"
				 :placeholder="'请填写'+typeMessage+'物品的地点'"> </textarea>
			</view>
		</view>

		<view class="ts-column">
			<view class="ts-row ts-flex-item ts-h6">
				上传{{typeMessage}}物品的图片，方便找回，最多上传9张图片。
			</view>
			<view class="ts-row ts-flex-item">
				<ts-image-uploader :count="9" @change="onChange"></ts-image-uploader>
			</view>
		</view>
		<view class="ts-column">
			<view class="ts-row ts-flex-item">
				<ts-button class="ts-row ts-flex-item" @tap="doPublish">发布</ts-button>
			</view>

		</view>
	</view>
</template>

<script>
	import tsImageUploader from "@/components/teaset/components/ts-image-uploader/ts-image-uploader.vue"
	import {
		image
	} from '@/common/api';
	import {
		event
	} from '@/common/api/lost';
	import {
		mapState,
		mapMutations,
		mapActions
	} from 'vuex'
	
	export default {
		components: {
			tsImageUploader
		},
		data() {
			return {
				type: "丢失",
				title: "校园卡",
				address: '罗马广场',
				linkman: '张三',
				mobile: '18928779500',
				description: '校园卡，编号XXXXXXXX',
				// title: "",
				// address: '',
				// linkman: '',
				// mobile: '',
				// description: '',
				files: [],
			}
		},
		async onLoad(e) {
			if (await this.checkLogin()) {

			}
		},
		methods: {
			//checkLogin
			...mapActions({
				getUserInfo: 'user/getUserInfo',
				checkLogin: 'checkLogin',
			}),
			
			switchType() {
				this.type = this.type == "丢失" ? "捡到" : "丢失";
			},
			onChange(files) {
				console.log(files)
				this.files = files;
			},

			async doPublish() {

				uni.showModal({
					title: '提示',
					content: `您确认要发布该条消息吗？`,
					success: async (res) => {
						if (res.confirm) {
							//上传图片
							let tmp_ids = new Set();
							for (let f of this.files) {
								let formdata = {};
								const res = await image.upload(f, formdata);
								if (res.errno === 0) {
									tmp_ids.add(res.data.id);
								}
							}
							const image_ids = Array.from(tmp_ids).join(',')
							// console.log(image_ids);

							let data = {
								image_ids: image_ids,
								title: this.title,
								address: this.address,
								linkman: this.linkman,
								mobile: this.mobile,
								description: this.description,
								type: this.type,
								user_id: this.user_id
							}

							const res = await event.create(data);
							console.log(res);

							if (res.errno === 0) { //添加成功								
								uni.navigateBack({
									delta: 1
								});
							} else {
								uni.showToast({
									title: res.errmsg,
									duration: 2000
								});
								// console.log(res);
							}

						} else if (res.cancel) {
							// console.log('用户点击取消');
						}
					}
				});
			},

		},
		computed: {
			typeMessage() {
				return (this.type == "丢失" ? "丢失" : "捡到");
			}

		}
	}
</script>

<style>
	view {
		line-height: 3em;
	}

	input {
		border-bottom: #C0C0C0 solid 1px;
		display: flex;
		flex: 1;
		margin-left: 30upx;
	}
</style>
