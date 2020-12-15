<template>
	<view class="main-view">
		<view>
			<view class="padding-top-xl cu-bar bg-white">
				<view class="action">
					<!--
						<text class="cuIcon-home" @click="onClickBack()" />
					-->
				</view>
				<view class="text-xl text-bold">
					{{ app_name }}
				</view>
				<view class="action">
					<!--
					<text class="cuIcon-share" @click="onClickShare()" />
					<text>&nbsp;&nbsp;&nbsp;</text>
					<text class="cuIcon-down" @click="onClickSaveImage()" />
					-->
				</view>
			</view>
		</view>

		<view class="zzz-media-editor">
			<zzzMediaEditor ref="zme" :editorImage="editorImage">
			</zzzMediaEditor>
		</view>

	</view>
</template>

<script>
	import uniNavBar from '@/components/uni-nav-bar/uni-nav-bar.vue'
	//import uniIcon from '@/components/uni-icon/uni-icon.vue'
	import zzzMediaEditor from '@/components/zzz-components/zzz-media-editor.vue'
	import apiFacemagi from '@/common/api/facemagi.js'
	
	export default {
		components: {
			uniNavBar,
			//uniIcon,
			zzzMediaEditor,
		},
		data() {
			return {
				//待处理图片默认地址
				editorImage: "/static/images/facemagi/720x900.png",
				imageKey: null
			}
		},
		onLoad(options) {
			console.log('options of editor: ' + JSON.stringify(options));
			this.imageKey = decodeURIComponent(options.imageKey);
			//console.log('imageKey:', this.imageKey);
			
			//从本地缓存读取要编辑的图片
			let that = this;
			uni.getStorage({
				key: that.imageKey,
				success(e) {
					//console.log('--> e.data:', e.data);
					that.editorImage = e.data;
					console.log("loaded image from local storage.");
				}
			});
		},
		created: function() {
		},
		computed: {
			i18n() {
				return this.$t('index');
			}
		},
		methods: {
			//调用 i18n 翻译，用于 script 中
			translate(e) {
				return this.$t('index')[e];
			},
			
			onClickBackHome() {
				this.$refs.zme.onClickBackHome();
			},
			
			onClickShare() {
				//console.log('share image ...');
				this.$refs.zme.shareImage();
			},
			
			onClickSaveImage() {
				//console.log('save image into album ...');
				this.$refs.zme.saveImageToAlbum();
			}
		}
	}
</script>

<style>
	.page {
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.main-view {
		/*background: #f3f5f6;*/
	}
	
	.zzz-media-editor {
		position: fixed;
		width: 100%;
		bottom: 0rpx;
	}
</style>
