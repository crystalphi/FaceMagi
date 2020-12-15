<template>
	<view>

		<!-- 点击底部功能菜单项后弹出的组件 -->
		<xpopup :hidden.sync='xpopupHidden' position='bottom' :noBotton='false' :noCancel='xpopupNoCancel' :noConfirm='xpopupNoConfirm' :cancelText="translate('Return')" :confirmText="translate('apply')" @cancel="popupCancel" @confirm="popupApply">
			<scroll-view scroll-x class="bg nav" scroll-with-animation :scroll-left="tabPopupScrollLeft">
				<view class="cu-item editor-item-container" :class="index==tabPopupCur?'text-orange cur':''" v-for="(item,index) in tabPopupData.func_list" :key="index" @tap="tabSelectPopup" :data-id="index">
					<!-- background-image 只支持网络图片和 base64 图片，可考虑更新后按 base64 保存到本地数据库，加载时从数据库读取 -->
					<view class='cu-avatar xl radius editor-item-big' :style="[{backgroundImage:'url('+tabPopupImages[index]+')'}]" @tap="tapPopupItem(index,item)">
						<view class="cu-tag badge" v-if="item.vip>0">PRO</view>
					</view>
					<view class="editor-item-label">{{item.name}}</view>
				</view>
			</scroll-view>
		</xpopup>
		
		<view class="float-btns-view float-btn-view-pst01">
			<button align="left" style="float:left" class="cu-btn round bg-white float-btn-left">
				<text class="cuIcon-home" @click="onClickBackHome()" />
			</button>
		</view>
		<view class="float-btns-view float-btn-view-pst02" :class="[{hide: hideImageBtns}]">
			<button align="left" style="float:left" class="cu-btn round bg-grey shadow float-btn-left">
				<text class="cuIcon-share" @click="onClickShare()" />
			</button>
			<button align="right" class="cu-btn round bg-grey shadow float-btn-right">
				<text class="cuIcon-down" @click="onClickSaveImage()" />
			</button>
		</view>
		
		<view class="cu-modal" :class="hideAppleLogin==false?'show':''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">{{ i18n.apple_login_request }}</view>
					<view class="action" @tap="hideAppleLoginModal">
						<text class="cuIcon-close text-red"></text>
					</view>
				</view>
				<view class="padding-xl">
					<view>{{ i18n.apple_login_notify }}</view>
					<view class="padding">
						<image class="signin-button" :src="signInButtonUrl" @tap="signInAndRun">
					</view>
				</view>
			</view>
		</view>

		<!-- 底部功能菜单 分为三个页面：
		Art：照片艺术化，如风格、卡通等。
			初始输入为上面最后应用图片；输出各种画风图片、可应用做后续处理。
		Editor：人脸部位编辑。
			初始输入为标准原图；输出仍为清晰照片、可应用做后续处理。
		Fun：从上述两项中选择的特色功能，直接生成，前后端不缓存。
			输入标准原图，输出各种画风图片、不可应用做后续处理。
		-->
		<view :key="1" v-if="1==tabMainCur">
			<view class="main-image">
				<image :src="mainImageArt" mode="widthFix" @tap="previewImage(mainImageArt)" />
			</view>
			<view class="editor-tab">
				<scroll-view scroll-x class="bg nav" scroll-with-animation :scroll-left="tabArtScrollLeft">
					<view class="cu-item editor-item-container" :class="index==tabArtCur?'text-orange cur':''" v-for="(item,index) in tabArtFunctions" :key="index" @tap="tabArtSelected" :data-id="index">
						<view class="cu-avatar bg-img xl radius editor-item" @tap="tapTabItem(index,item)" :style="[{ backgroundImage:'url('+tabArtImages[index]+')' }]">
							<view class="cu-tag badge bg-blue" v-if="item.vip>0">PRO</view>
						</view>
						<view class="editor-item-label">{{item.name}}</view>
					</view>
				</scroll-view>
			</view>
		</view>
		<view :key="0" v-if="0==tabMainCur">
			<view class="main-image">
				<image :src="mainImageEditor" mode="widthFix" @tap="previewImage(mainImageEditor)" />
			</view>
			<view class="editor-tab">
				<scroll-view scroll-x class="bg nav" scroll-with-animation :scroll-left="tabEditorScrollLeft">
					<!-- :style="[{ backgroundImage:'url('+$BASE_URL+item.icon+')'
					-->
					<view class="cu-item editor-item-container" :class="index==tabEditorCur?'text-orange cur':''" v-for="(item,index) in tabEditorFunctions" :key="index" @tap="tabEditorSelected" :data-id="index">
						<view class="cu-avatar bg-img xl radius editor-item" @tap="tapTabItem(index,item)" :style="[{ backgroundImage:'url('+tabEditorImages[index]+')' }]">
							<view class="cu-tag badge bg-blue" v-if="item.vip>0">PRO</view>
						</view>
						<view class="editor-item-label">{{item.name}}</view>
					</view>
				</scroll-view>
			</view>
		</view>
		<view :key="2" v-if="2==tabMainCur">
			<view class="text-center image-fun">
				<image :src="mainImageFun" mode="widthFix" @tap="previewImage(mainImageFun)" />
			</view>
			<view class="editor-tab">
				<scroll-view scroll-x class="bg nav" scroll-with-animation :scroll-left="tabFunScrollLeft">
					<view class="cu-item editor-item-container" :class="index==tabFunCur?'text-orange cur':''" v-for="(item,index) in tabFunFunctions" :key="index" @tap="tabFunSelected" :data-id="index">
						<view class="cu-avatar bg-img xl radius editor-item" @tap="tapFunItem(index,item)" :style="[{ backgroundImage:'url('+tabFunImages[index]+')' }]">
						</view>
						<view class="editor-item-label">{{item.name}}</view>
					</view>
				</scroll-view>
			</view>
		</view>
		<scroll-view scroll-x class="bg nav text-bold big-tab" :scroll-left="tabMainScrollLeft">
			<view class="flex text-center">
				<view :key="1" class="cu-item flex-sub tab-color-red" :class="1==tabMainCur?'tab-item text-orange cur tab-color-default':''" @tap="tabMainSelected" :data-id="1">
					{{ i18n.art }}
				</view>
				<view :key="0" class="cu-item flex-sub tab-color-green" :class="0==tabMainCur?'tab-item text-orange cur tab-color-default':''" @tap="tabMainSelected" :data-id="0">
					{{ i18n.editor }}
				</view>
				<view :key="2" class="cu-item flex-sub tab-color-blue" :class="2==tabMainCur?'tab-item text-orange cur tab-color-default':''" @tap="tabMainSelected" :data-id="2">
					{{ i18n.fun }}
				</view>
			</view>
		</scroll-view>

	</view>
</template>

<script>
	import Vue from 'vue';
	import apiFacemagi from '@/common/api/facemagi.js'
	import xpopup from '@/components/zzz-components/x-popup.vue'
	// app 权限判断及引导：https://ext.dcloud.net.cn/plugin?id=594
	import permission from '@/js_sdk/wa-permission/permission.js'
	import plusShare from '@/js_sdk/plusShare.js'
	//import payment from '@/common/payment.js'
	
	//TODO: 付费用户任务优先！
	
	export default {
		components: {
			xpopup
		},
		name: 'zzzMediaEditor',
		//本组件公开属性
		props: {
			editorImage: [String], //待处理图片地址
			//someData: {type: Array}, //分组数据（暂不用）
		},
		data() {
			return {
				//Tab 组件所用数据
				tabMainCur: 1, //底部大签页
				tabMainScrollLeft: 0, //底部大签页
				tabEditorCur: 0, //大标签页 EDITOR 中的小标签页
				tabEditorScrollLeft: 0, //大标签页 EDITOR 中的小标签页
				tabArtCur: 0, //大标签页 ART 中的小标签页
				tabArtScrollLeft: 0, //大标签页 ART 中的小标签页
				tabFunCur: 0, //大标签页 FUN 中的小标签页
				tabFunScrollLeft: 0, //大标签页 FUN 中的小标签页
				tabPopupCur: 0, //底部弹窗中的标签页
				tabPopupScrollLeft: 0, //底部弹窗中的标签页
				tabItemIndex: 0, //大标签页中当前开启底部弹窗的标签序号
				tabPopupItemIndex: 0, //底部弹窗的当前选中标签序号
				//xpopup 组件所用数据
				xpopupHidden: true, //是否显示底部抽屉
				xpopupNoCancel: false, //不显示底部抽屉上的返回按钮
				xpopupNoConfirm: true, //不显示底部抽屉上的确定按钮
				//其他数据
				mainImageEditor: null, //Editor 标签主图片
				mainImageArt: null, //Art 标签主图片
				mainImageFun: null, //Fun 标签主图片
				hideImageBtns: true, //是否在图片处理时隐藏相关按钮
				hideAppleLogin: true, //是否隐藏苹果登录按钮对话框
				gLoginInfo: this.gLoginInfo,
				tabEditorFunctions: [], //Editor 标签项数据，从后端获取的功能清单数据
				tabArtFunctions: [], //Art 标签项数据，从后端获取的功能清单数据
				tabFunFunctions: [], //Fun 标签项数据，从后端获取的功能清单数据
				tabEditorImages: [], //Editor 标签项数据，从后端获取的功能清单图片地址
				tabArtImages: [], //Art 标签项数据，从后端获取的功能清单图片地址
				tabFunImages: [], //Fun 标签项数据，从后端获取的功能清单图片地址
				savedFilePath: null,
				tabPopupData: [], //弹窗标签项菜单数据
				tabPopupImages: [], //弹窗标签项菜单图片地址
				tabEditorFuncImages: [], //Editor 标签项功能子项菜单图片地址，二维数组
				tabArtFuncImages: [], //Art 标签项功能子项菜单图片地址，二维数组
				storeKeyAlbumFlagEditor: "album_not_save_editor", // Editor标签页主图是否保存
				storeKeyAlbumFlagArt: "album_not_save_art", // Art标签页主图是否保存
				storeKeyImageCur: null, //当前标签页存储键值
				storeKeyAlbumFlagCur: null, //当前标签页图片保存标记
				funcData: null, //后端任务处理函数参数
				funcGroup: null, //后端任务处理函数分组
				screenPixelRatio: 1.0,
				attr_dict: null,
				m_id: null,
				paidCacheUpdated: false,
				signInButtonUrl: "https://appleid.cdn-apple.com/appleid/button?color=black&border=false&height=45&width=210&locale=" + Vue.prototype.language
			};
		},
		created: function() {
			//console.log('--> this.editorImage:', this.editorImage)
		},
		mounted: function() {
			//console.log('--> mounted#');
			let _this = this;
			uni.getSystemInfo({
				success: function (res) {
					console.log('--> pixelRatio: ' + res.pixelRatio);
					console.log('--> windowWidth: ' + res.windowWidth);
					_this.screenPixelRatio = res.pixelRatio * res.windowWidth / 750; //ip6s: 750 = 2 * 375
				}
			});
			
			//远程获取已购项更新
			//this.loopUpdatePaidCache();
			
			//从后端获取功能清单完整信息，动态生成底部功能菜单界面
			//备注：由于小程序端对本地缓存有大小限制，现不做缓存，统一都从后端读取
			this.mainImageEditor = this.editorImage;
			this.mainImageArt = this.editorImage;
			this.mainImageFun = this.editorImage;
			
			apiFacemagi.setStorageValue(this.storeKeyAlbumFlagEditor, false);
			apiFacemagi.setStorageValue(this.storeKeyAlbumFlagArt, false);
			this.tabMainSetCur(); //当前大标签初始信息设置
			
			let that = this;
			uni.getStorage({
				key: 'attr_dict',
				success(e) {
					//console.log('--> e.data:', e.data);
					that.attr_dict = e.data;
					console.log("load attr_dict from local storage: " + e.data);
					let sex = 'female';
					if (that.attr_dict != null && that.attr_dict['Male']) {
						sex = 'male';
					}
					that.getFunctions('', sex).then(function(value) {
						//console.log('got functions info from backend:', value);
						that.tabEditorFunctions = value.functions_editor; //赋值后界面会自动更新
						that.tabArtFunctions = value.functions_art; //同上
						that.tabFunFunctions = value.functions_fun; //同上
						//但是有个缺陷：ios上图片不会自动更新，分析后发现
						//字典数据中的图片不更新，但列表中的图片可以。所以补充下面代码：
						that.tabEditorImages = [];
						that.tabArtImages = [];
						that.tabEditorFuncImages = [];
						that.tabArtFuncImages = [];
						for (let i in value.functions_editor) { //Editor 及其弹出标签图片数据
							that.tabEditorImages.push(that.$BASE_URL + value.functions_editor[i].icon);
							let x = [];
							//console.log('-->', value.functions_editor[i]);
							for (let j in value.functions_editor[i].func_list) {
								x.push(that.$BASE_URL + value.functions_editor[i].func_list[j].icon);
							}
							that.tabEditorFuncImages.push(x);
						}
						for (let i in value.functions_art) { //Art 及其弹出标签图片数据
							that.tabArtImages.push(that.$BASE_URL + value.functions_art[i].icon);
							let x = [];
							//console.log('-->', value.functions_art[i]);
							for (let j in value.functions_art[i].func_list) {
								x.push(that.$BASE_URL + value.functions_art[i].func_list[j].icon);
							}
							that.tabArtFuncImages.push(x);
						}
						that.tabFunImages = [];
						for (let i in value.functions_fun) { //Fun（无弹出标签）图片数据
							//console.log('--> functions_fun i:', value.functions_fun[i])
							that.tabFunImages.push(that.$BASE_URL + value.functions_fun[i].icon);
						}
					}).catch((e) => {
						console.log('call getFunctions got error:', JSON.stringify(e));
					});
					uni.getStorage({
						key: 'm_id',
						success(e) {
							//console.log('--> e.data:', e.data);
							that.m_id = e.data;
							console.log("load m_id from local storage:" + e.data);
						}
					});
				}
			});
		},
		onLoad(options) { //貌似没有调用到
			//console.log('--> onLoad# zzz-media-editor # options:', options);
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
			
			//图片预览
			previewImage(_image) {
				apiFacemagi.saveBase64ImageFile(_image, false)
				.then(function(res) {
					//console.log('saved image to temp file:', res.filePath);
					// #ifdef APP-PLUS
					plus.nativeUI.previewImage([res.filePath],{
						current:0,
						loop:false
					});
					// #endif
				})
				.catch(function(e) {
					console.log('saveBase64ImageFile rejected:', JSON.stringify(e));
				});
			},
			
			//设置当前大标签页相关信息
			tabMainSetCur() {
				if (this.tabMainCur == 0) {
					this.storeKeyImageCur = "image_save_editor";
					this.storeKeyAlbumFlagCur = this.storeKeyAlbumFlagEditor;
				} else if (this.tabMainCur == 1) {
					this.storeKeyImageCur = "image_save_art";
					this.storeKeyAlbumFlagCur = this.storeKeyAlbumFlagArt;
				} else if (this.tabMainCur == 2) {
					this.storeKeyImageCur = "image_save_fun";
				}
			},
			
			//选取底部大标签页
			tabMainSelected(e) {
				//console.log('--> tabMainSelected e:', e);
				this.tabMainCur = e.currentTarget.dataset.id;
				this.tabMainScrollLeft = (e.currentTarget.dataset.id - 1) * 60 * this.screenPixelRatio;
				this.tabMainSetCur();
			},
			//选取大标签页 EDITOR 中的小标签页
			tabEditorSelected(e) {
				//console.log('--> tabEditorSelected e:', e);
				this.tabEditorCur = e.currentTarget.dataset.id;
				this.tabEditorScrollLeft = (e.currentTarget.dataset.id - 1) * 60 * this.screenPixelRatio;
				this.tabPopupCur = 0;
				this.tabPopupScrollLeft = 0;
			},
			//选取大标签页 ART 中的小标签页
			tabArtSelected(e) {
				//console.log('--> tabArtSelected e:', e);
				this.tabArtCur = e.currentTarget.dataset.id;
				this.tabArtScrollLeft = (e.currentTarget.dataset.id - 1) * 60 * this.screenPixelRatio;
				this.tabPopupCur = 0;
				this.tabPopupScrollLeft = 0;
			},
			//选取大标签页 FUN 中的小标签页
			tabFunSelected(e) {
				//console.log('--> tabFunSelected e:', e);
				this.tabFunCur = e.currentTarget.dataset.id;
				this.tabFunScrollLeft = (e.currentTarget.dataset.id - 1) * 60 * this.screenPixelRatio;
			},
			//选取底部弹窗中的标签页
			tabSelectPopup(e) {
				//console.log('--> tabSelectPopup e:', e);
				this.tabPopupCur = e.currentTarget.dataset.id;
				this.tabPopupScrollLeft = (e.currentTarget.dataset.id - 1) * 90 * this.screenPixelRatio; // 适应不同屏幕像素率
			},
			
			//点击底部次级标签页中的子项
			tapTabItem(index, obj) {
				//console.log('tapTabItem index:', index, 'obj:', obj);
				let tabCur = null;
				let tabFunctions = null;
				let tabFuncImages = null;
				if (this.tabMainCur == 0) {
					tabCur = this.tabEditorCur;
					tabFunctions = this.tabEditorFunctions;
					tabFuncImages = this.tabEditorFuncImages;
				} else if (this.tabMainCur == 1) {
					tabCur = this.tabArtCur;
					tabFunctions = this.tabArtFunctions;
					tabFuncImages = this.tabArtFuncImages;
				}
				//if (this.tabPopupData.length == 0 || tabCur != index) {
				if (true) {
					//根据所选重新生成底部弹窗内容
					this.tabPopupData = tabFunctions[index];
					this.tabPopupImages = tabFuncImages[index];
					this.tabItemIndex = index;
					//console.log('--> this.tabItemIndex:', this.tabItemIndex);
					//console.log('--> this.tabPopupImages:', this.tabPopupImages);
					this.tabPopupCur = 0;
				}
				//弹出底部次级操作菜单
				this.xpopupHidden = false;
			},
			
			callbackFunTaskSuccess(res_data, i18n_msg, funcGroup, funcData) {
				this.mainImageFun = res_data['image'];
				this.resultImageCacheSave(res_data['image'], funcGroup, funcData);
				apiFacemagi.setStorageValue(this.storeKeyImageCur, res_data['image']);
				this.hideImageBtns = false;
			},
			//点击 FUN 标签页中的子项
			tapFunItem(index, obj) {
				//console.log('tapFunItem index:', index, 'obj:', obj);
				let funcData = this.tabFunFunctions[index];
				let funcGroup = funcData.func_group;
				//首先检查本地缓存，如果有则直接使用，否则从后端获取
				let resultImageCacheName = this.getResultImageCacheName(funcData.func_class, funcGroup, funcData.func_name, funcData.func_params);
				let resultImageCache = apiFacemagi.getStorageValue(resultImageCacheName);
				if (resultImageCache) {
					console.log('--> 获取到处理结果图片本地缓存：' + resultImageCacheName);
					this.setResultImage(resultImageCache);
					apiFacemagi.setStorageValue(this.storeKeyImageCur, resultImageCache);
					this.hideImageBtns = false;
				} else {
					//调用后端进行图片处理
					this.backendProcess(funcGroup, funcData, this.callbackFunTaskSuccess);
				}
			},
			
			resultImageCacheSave(image, funcGroup, funcData) {
				//保存处理结果图片到本地缓存中，以便下次使用
				let resultImageCacheName = this.getResultImageCacheName(funcData.func_class, funcGroup, funcData.func_name, funcData.func_params);
				apiFacemagi.setStorageValue(resultImageCacheName, image);
				let allResultImageNames = apiFacemagi.getStorageValue('resultImageNames');
				if (allResultImageNames) {
					if(allResultImageNames.indexOf(resultImageCacheName) <= -1) {
						allResultImageNames.push(resultImageCacheName);
					}
				} else {
					allResultImageNames = [resultImageCacheName];
				}
				apiFacemagi.setStorageValue('resultImageNames', allResultImageNames);
				console.log('--> 处理结果图片已保存到本地缓存：' + resultImageCacheName);
			},
			//将处理结果图片应用到屏幕主图
			setResultImage(imageData) {
				if (this.tabMainCur == 0) {
					this.mainImageEditor = imageData;
				} else if (this.tabMainCur == 1) {
					this.mainImageArt = imageData;
				} else if (this.tabMainCur == 2) {
					this. mainImageFun = imageData;
				}
				this.xpopupNoCancel = false;
				this.xpopupNoConfirm = false;
			},
			
			//调用后端处理图片成功后执行的回调，设置主图、保存缓存
			callbackEditorTaskSuccess(res_data, i18n_msg, funcGroup, funcData) {
				this.setResultImage(res_data['image']);
				this.resultImageCacheSave(res_data['image'], funcGroup, funcData);
			},
			//清理全部处理结果图片本地缓存（以 result_ 开头的键值）
			cleanAllResultImageCache() {
				let allResultImageNames = apiFacemagi.getStorageValue('resultImageNames');
				if (allResultImageNames) {
					for (let i in allResultImageNames) {
						try {
							//uni.removeStorageSync(allResultImageNames[i]);
							uni.removeStorage({
								key: allResultImageNames[i],
								success: function (res) {
									console.log('removed ' + allResultImageNames[i]);
								}
							});
						} catch (e) {
							console.log('缓存删除失败：' + allResultImageNames[i]);
						}
					}
				}
				uni.removeStorageSync('resultImageNames');
				console.log('处理结果图片本地缓存清理完毕！');
			},
			//根据任务参数，生成处理结果本地缓存索引名称
			getResultImageCacheName(func_class=null, func_group=null, func_name=null, func_params=null) {
				let resultImageCacheName = 'result';
				if (func_class) {
					resultImageCacheName += '-' + String(func_class);
				}
				if (func_group) {
					resultImageCacheName += '-' + String(func_group);
				}
				if (func_name) {
					resultImageCacheName += '-' + String(func_name);
				}
				if (func_params) {
					resultImageCacheName += '-' + String(func_params);
				}
				resultImageCacheName += '_png';
				return resultImageCacheName;
			},
			//点击底部弹窗中的子项
			async tapPopupItem(index, obj) {
				console.log('tapPopupItem # popup item index:' + index);

				this.hideImageBtns = true;
				
				if (index == 0) { //恢复为原图
					let that = this;
					/*
					uni.showModal({
						title: this.translate('notice'),
						confirmText: this.translate('confirm'),
						cancelText: this.translate('cancel'),
						content: this.translate('msg_restore_original_notice'),
						success: function (res) {
							if (res.confirm) {
								console.log('restore original image ...');
								// 后端任务图片缓存恢复为原图
								let res = apiFacemagi.taskRestoreOriginalImage(that.m_id);
								//console.log('--> res:', res)
								if (res.errno == 0) {
									console.log('backend restore original success!');
									// 前端恢复为处理前的图片
									let that_2 = that;
									uni.getStorage({
										key: 'image_norm',
										success(e) {
											if (that_2.tabMainCur == 0) {
												that_2.mainImageEditor = e.data;
											} else if (that_2.tabMainCur == 1) {
												that_2.mainImageArt = e.data;
											}
											uni.setStorage({
												key: that_2.storeKeyImageCur,
												data: e.data,
												success: async function(e) {
													apiFacemagi.setStorageValue(that_2.storeKeyAlbumFlagCur, false);
												}
											});
										}
									});
								} else {
									console.log('restore image failed!', res.errmsg);
								}
							} else if (res.cancel) {
								//console.log('用户点击取消');
							}
						}
					});
					*/
					uni.getStorage({
						key: 'image_norm',
						success(e) {
							if (that.tabMainCur == 0) {
								that.mainImageEditor = e.data;
							} else if (that.tabMainCur == 1) {
								that.mainImageArt = e.data;
							} else if (that.tabMainCur == 2) {
								that.mainImageFun = e.data;
							}
							that.xpopupNoCancel = false;
							that.xpopupNoConfirm = false;
						}
					});
					return;
				}
				
				//动态设置图片模糊
				//this.cropperOpt.filter = "blur(30px)"
				//this.cropperOpt.transform = "scale(1.2)"
				
				this.tabPopupItemIndex = index;
				this.xpopupNoCancel = true;
				this.xpopupNoConfirm = true;
				//可尝试写法：self.viewer.style.display = 'none';
				
				let funcData = this.tabPopupData.func_list[index];
				let funcGroup = this.tabPopupData.func_group;
				this.funcData = funcData;
				this.funcGroup = funcGroup;
				
				//首先检查本地缓存，如果有则直接使用，否则从后端获取
				let resultImageCacheName = this.getResultImageCacheName(funcData.func_class, funcGroup, funcData.func_name, funcData.func_params);
				let resultImageCache = apiFacemagi.getStorageValue(resultImageCacheName);
				if (resultImageCache) {
					console.log('--> 获取到处理结果图片本地缓存：' + resultImageCacheName);
					this.setResultImage(resultImageCache);
				} else {
					//使用 VIP 功能前先检查用户权限，有则执行，无则开启内购
					if (funcData.vip == 1 && ! Vue.prototype.isLiteVersion) {
						//从本地缓存获取上次登录用户名及登录时间，如果无缓存或过期则执行登录
						let ios_user_info = apiFacemagi.getStorageValue('ios_user_info');
						if (ios_user_info && Date.parse(new Date())-ios_user_info['timestamp'] < 5*24*3600*1000) { //过期设时间为 5 天（TODO: 如果用户更改了 AppleID，则只能在~5天后才能使用新 AppleID 购买）
							//苹果账号有效，执行权限检查或内购及执行
							this.checkPaidIAPRun();
						} else {
							console.log('no apple login info found, try login now ...');
							//先执行苹果账号登录，再执行内购检查流程
							this.hideAppleLogin = false;
						}
					} else {
						//非 VIP 功能，调用后端进行图片处理
						this.backendProcess(funcGroup, funcData, this.callbackEditorTaskSuccess);
					}
				}
				
				//this.$emit('tapPopupItem', index, obj);
			},
			
			async backendProcess(funcGroup, funcData, taskSuccessCallback) {
				if (funcData.func_name != null) {
					let tk = "harekrishna10800"; //访问令牌（原则上应在登录后由后端动态生成）
					let m_id = this.m_id;
					let m_path = null; //非新图片，为空
					let user_id = apiFacemagi.getUserIdLocal();
					let func_group = funcGroup;
					let func_class = funcData.func_class;
					let func_name = funcData.func_name;
					let func_params = funcData.func_params;
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
							i18n_msg)
					.then((res_data, i18n_msg) => {
						taskSuccessCallback(res_data, i18n_msg, funcGroup, funcData);
					})
					.catch((e) => {
						console.log('taskProcess() error: ' + JSON.stringify(e));
						this.xpopupNoCancel = false;
						if (apiFacemagi.isString(e)) {
							uni.showModal({
								title: '',
								confirmText: this.translate('confirm'),
								content: e,
								showCancel: false
							});
						}
					});
				}
			},
			
			//点击底部弹窗中的 Cancel
			async popupCancel() {
				//console.log('cancel processed image.');
				// 前端恢复为处理前的图片
				let that = this;
				uni.getStorage({
					key: this.storeKeyImageCur,
					success(e) {
						if (that.tabMainCur == 0) {
							that.mainImageEditor = e.data;
						} else if (that.tabMainCur == 1) {
							that.mainImageArt = e.data;
						} else if (that.tabMainCur == 2) {
							that.mainImageFun = e.data;
						}
						apiFacemagi.setStorageValue(that.storeKeyAlbumFlagCur, false);
						that.xpopupNoCancel = false;
						that.xpopupNoConfirm = true;
						that.xpopupHidden = true;
					}
				});
			},
			//点击底部弹窗中的 Apply，前后端保存和应用处理图片。
			async popupApply() {
				console.log('apply processed image.');
				let that = this;
				let imageToSave = null;
				if (this.tabMainCur == 0) {
					imageToSave = that.mainImageEditor;
				} else if (this.tabMainCur == 1) {
					imageToSave = that.mainImageArt;
				}
				uni.setStorage({
					key: this.storeKeyImageCur,
					data: imageToSave,
					success: async function(e) {
						console.log('存储图片成功');
						apiFacemagi.setStorageValue(that.storeKeyAlbumFlagCur, true);
						let func_group = that.tabPopupData.func_group;
						//console.log('--> that.tabPopupItemIndex:', that.tabPopupItemIndex);
						let funcData = that.tabPopupData.func_list[that.tabPopupItemIndex];
						let func_class = funcData.func_class;
						let func_name = funcData.func_name;
						let func_params = funcData.func_params;
						//console.log('--> funcData:', funcData)
						// 只需对 editor（美妆）标签页中的图片做后端应用
						if (that.tabMainCur == 0) {
							// 在 art 中使用编辑后的图片
							//that.mainImageArt = that.mainImageEditor;
							// 后端保存图片以做后续处理
							let res = null;
							if (that.tabPopupCur == 0) {
								res = await apiFacemagi.taskRestoreOriginalImage(that.m_id);
								console.log('后端恢复原图');
							} else {
								res = await apiFacemagi.taskApplyImageSave(that.m_id, func_group, func_class, func_name, func_params);
								console.log('后端保存修改');
							}
							//console.log('--> res:', res)
							if (res.errno == 0) {
								console.log('apply image success!');
								that.xpopupNoCancel = false;
								that.xpopupNoConfirm = true;
								that.hideImageBtns = false;
								that.xpopupHidden = true;
							} else {
								console.log('apply image failed!', res.errmsg);
							}
						} else {
							that.xpopupNoCancel = false;
							that.xpopupNoConfirm = true;
							that.hideImageBtns = false;
							that.xpopupHidden = true;
						}
					},
					fail: function(e) {
						console.log('存储图片失败: ' + JSON.stringify(e));
					}
				});
			},
			
			//动态生成图片背景 style 语句
			setBackgroundStyle(item) {
				return "background-image:url('" + item.icon + "');"
			},

			//获取服务端支持的图片编辑功能清单
			//如果只需要获取 后端功能清单版本号，则指定 act='ver'
			async getFunctions(act = '', sex = 'all') {
				console.log("--> calling getFunctions() for " + sex);
				this.loadModal = true;
				const duration = 2000;

				//根据输入的组件属性参数，调用相应后端接口获取功能清单
				let res = await apiFacemagi.getConfigFunctions(act, sex);
				if (res.errno == 0) {
					this.loadModal = false;
					const data = res.data;
					if (data) {
						return data;
					}
				} else {
					this.loadModal = false;
					console.log('-->' + JSON.stringify(res));
					uni.showModal({
						title: 'Get functions fail',
						confirmText: this.translate('confirm'),
						content: JSON.stringify(res),
						showCancel: false
					});
				}
			},
		
			//检查是否有生成的主图片未保存
			checkAlbumFlags() {
				console.log('--> getStorageValue', this.storeKeyAlbumFlagEditor);
				let fEditor = apiFacemagi.getStorageValue(this.storeKeyAlbumFlagEditor);
				let fArt = apiFacemagi.getStorageValue(this.storeKeyAlbumFlagArt);
				return fEditor || fArt;
			},
			//清除主图片未保存标志
			clearAlbumFlag() {
				apiFacemagi.setStorageValue(this.storeKeyAlbumFlagCur, false);
				//console.log('--> this.storeKeyAlbumFlagCur', this.storeKeyAlbumFlagCur);
			},
			//保存主图片到本地相册
			saveImageToAlbum() {
				//console.log('--> this.tabMainCur', this.tabMainCur);
				//console.log('--> this.storeKeyImageCur', this.storeKeyImageCur);
				// 读取本地缓存中的图片，保存到照片文件夹
				let that = this;
				uni.getStorage({
					key: this.storeKeyImageCur,
					success(res) {
						//注意：以下代码在真实设备上会调用上述函数分别处理，调试环境则会忽略调用
						// #ifdef APP-PLUS
						// 根据设备类型调用不同函数
						if (plus.os.name == 'iOS') {
							//console.log('--> call saveImageToPhotosAlbum');
							//console.log('--> res.data:', res.data);
							//第一次保存时会询问权限
							apiFacemagi.saveBase64ImageFile(res.data, true)
							.then(function(value) {
								//console.log('image saved');
								if (value.code == 0) {
									uni.showToast({
										title: that.translate('image_saved'),
										mask: false,
										duration: 1500
									});
									that.clearAlbumFlag();
								} else {
									// 判断iOS设备上当前App是否有某项权限
									if (! permission.judgeIosPermission("photoLibrary")) {
										uni.showModal({
											title: that.translate('msg_no_save_permission'),
											confirmText: that.translate('confirm'),
											cancelText: that.translate('cancel'),
											content: that.translate('msg_ask_change_settings'),
											success: function (res) {
												if (res.confirm) {
													permission.gotoAppPermissionSetting(); //跳转到设置
												} else if (res.cancel) {
													//pass
												}
											}
										});
									}
								}
							})
							.catch(function(value) {
								console.log('saveBase64ImageFile rejected:' + value);
								uni.showToast({
									title: that.translate('image_save_failed'),
									icon: 'none',
									mask: false,
									duration: 1500  
								});
								return false;
							});
						} else {
							// 获取Android设备上当前App是否有某项权限
							//TODO: 安卓接口为异步调用
							requestAndroidPermission(android.permission.WRITE_EXTERNAL_STORAGE, saveImageAlbum);
						}
						// #endif
					}
				});
			},
			
			signInAndRun() {
				this.hideAppleLoginModal();
				apiFacemagi.checkApplLogin()
				.then((res) => {
					this.checkPaidIAPRun();
				})
				.catch((e) => {
				});
			},
			hideAppleLoginModal() {
				this.hideAppleLogin = true;
				this.xpopupNoCancel = false;
			},
			
			//定时从苹果获取最新已购项，直到获取完毕
			loopUpdatePaidCache() {
				apiFacemagi.updatePaidCache()
				.then((res) => {
					this.paidCacheUpdated = true;
					console.log('远程获取已购项完毕！');
				})
				.catch((e) => {
					//如果更新失败，则间隔 60 秒后再次执行
					if (! this.paidCacheUpdated) {
						setTimeout(() => {
							this.loopUpdatePaidCache();
						}, 30000);
					}
				});
			},
			
			execIAP() {
				//使用苹果账号执行内购
				let funcData = this.funcData;
				let funcGroup = this.funcGroup;
				if (Vue.prototype.apple_user_id) {
					let that = this;
					uni.showModal({
						title: this.translate('notice'),
						confirmText: this.translate('confirm'),
						cancelText: this.translate('cancel'),
						content: this.translate('msg_vip_function_notice'),
						success: function (res) {
							if (res.confirm) {
								//console.log('用户点击确定');
								//uni.showLoading({mask: true, title: that.translate('api_processing')});
								apiFacemagi.execAppleIAP()
								.then((res) => {
									//用户购买权限 OK，调用后端进行图片处理
									that.backendProcess(funcGroup, funcData, that.callbackEditorTaskSuccess);
								})
								.catch((e) => {
									uni.showModal({
										confirmText: that.translate('confirm'),
										content: that.translate('msg_purchase_failed'),
										showCancel: false
									});
								});
							} else if (res.cancel) {
								//console.log('用户点击取消');
								that.xpopupNoCancel = false;
							}
						}
					});
				} else {
					console.log('用户没有正常登录，忽略内购和功能执行');
				}
			},
			
			async checkPaidIAPRun() {
				let funcData = this.funcData;
				let funcGroup = this.funcGroup;
				uni.showLoading();
				if (Vue.prototype.apple_user_id) {
					//检查权限缓存
					if (apiFacemagi.checkPaidCache()) {
						//用户已有权限，调用后端进行图片处理
						uni.hideLoading();
						this.backendProcess(funcGroup, funcData, this.callbackEditorTaskSuccess);
					} else {
						//没有权限，远程同步获取
						apiFacemagi.updatePaidCache()
						.then((res) => {
							this.paidCacheUpdated = true;
							//权限已同步，再次检查有效性
							if (apiFacemagi.checkPaidCache()) {
								uni.hideLoading();
								this.backendProcess(funcGroup, funcData, this.callbackEditorTaskSuccess);
							} else {
								uni.hideLoading();
								this.execIAP();
							}
						})
						.catch((e) => {
							console.log('远程同步获取已购项失败。');
							uni.hideLoading();
							this.execIAP();
						});
					}
				} else {
					console.log('用户没有正常登录，忽略内购和功能执行');
				}
			},
			
			//调用系统分享，分享主图片到社交网路等地方
			shareImage() {
				//console.log('--> shareImage() this.storeKeyImageCur', this.storeKeyImageCur);
				let that = this;
				uni.getStorage({
					key: this.storeKeyImageCur,
					success(e) {
						apiFacemagi.saveBase64ImageFile(e.data, false)
						.then(function(value) {
							//console.log('saved image temp file:', value.filePath);
							// #ifdef APP-PLUS
							//分享内容，开发者可自定义
							//参考：http://www.html5plus.org/doc/zh_cn/share.html
							/*
							var message = {
								//type: 'text', //默认
								title: "Share the picture", //应用名字
								content: "FaceMagi - " + that.translate('app_advert'),
								href: "http://www.dcloud.io/hellomui", //分享出去后，点击跳转地址
								thumbs: ["http://img-cdn-qiniu.dcloud.net.cn/icon3.png"] //分享缩略图
							} */
							//let value = 'http://img-cdn-qiniu.dcloud.net.cn/icon2.png';
							let message = {
								type: 'image/png',
								content: 'FaceMagi - ' + that.translate('app_advert'),
								title: 'Share the picture', //应用名字
								pictures: [value.filePath], //分享图片，本地路径
								thumbs: [value.filePath]
							}
							//调起分享
							plusShare.plusShare(message, function(res) {
								//分享回调函数
								if(res) {
									//plus.nativeUI.toast("sharing success");
									uni.showToast({
										title: that.translate('sharing_success'),
										mask: false,
										duration: 1500
									});
								} else {
									//plus.nativeUI.toast("sharing fail");
									uni.showToast({
										title: that.translate('sharing fail'),
										mask: false,
										duration: 1500
									});
								}
							})
							// #endif
						})
						.catch(function(value) {
							console.log('saveBase64ImageFile rejected:', value);
						});
					}
				})
			},
			
			onClickBackHome() {
				// 如果图片有修改但未保存，询问是否放弃
				//let isFlag = this.checkAlbumFlags();
				let isFlag = true; //强制问询
				//console.log('--> isFlag:', isFlag);
				let that = this;
				if (isFlag) {
					uni.showModal({
						title: this.translate('notice'),
						content: this.translate('msg_image_save_notice'),
						confirmText: this.translate('confirm'),
						cancelText: this.translate('cancel'),
						success: function (res) {
							if (res.confirm) {
								that.cleanAllResultImageCache();
								//uni.navigateBack({
								//	delta: 1
								//});
								uni.navigateTo({
									url: '/pages/tabbar/face/index'
								});
							} else if (res.cancel) {
								//console.log('用户点击取消');
							}
						}
					});
				} else {
					uni.navigateTo({
						url: '/pages/tabbar/face/index'
					});
				}
			},
			
			onClickShare() {
				//console.log('share image ...');
				this.shareImage();
			},
			
			onClickSaveImage() {
				//console.log('save image into album ...');
				this.saveImageToAlbum();
			}
		}
	}
</script>

<style lang="scss" scoped="">
	.page {
		//background: #808080;
		display: flex;
		flex-direction: column;
		//font-size: 16px;
		justify-content: center;
	}
	
	.hide {
		opacity: 1;
		visibility: hidden; //or visible;
	}
	
	.float-modal-view {
		position: fixed;
		z-index: 999;
		text-align: center;
		padding: 20rpx;
	}
	
	.float-btns-view {
		position: fixed;
		z-index: 990;
		width: 100%;
		text-align: center;
		padding: 20rpx;
	}
	.float-btn-view-pst01 {
		top: 120rpx;
	}
	.float-btn-view-pst02 {
		bottom: 340rpx;
	}
	
	.float-btn-left {
		float: left;
		left: 0rpx;
		font-size: 32rpx;
		opacity: 0.7; //1-不透明
	}
	.float-btn-right {
		float: right;
		right: 0rpx;
		font-size: 32rpx;
		opacity: 0.7;
	}
	
	.nav .cu-item.cur {
		border-bottom: 4rpx none;
	}

	.main-image {
		//position: fixed;
		//top: 116rpx; //对于 iPad Pro 需设置为 0
		background: #f4f5f7; //#f2f2f2, f4f5f7（组件默认背景色）
		width: 100%;
		height: 100%;
		text-align: center;
		margin-bottom: -12rpx;
	}
	.main-image image {
		width: 100%;
		height: 100%;
		/*width: 480rpx;
		height: 600rpx;*/
		margin: 0rpx auto;
	}
	
	.image-fun {
		//position: fixed;
		//top: 220rpx;
		background: #f4f5f7; //#f2f2f2, f4f5f7（组件默认背景色）
		width: 100%;
		height: 100%;
		text-align: center;
	}
	.image-fun image {
		width: 480rpx;
		height: 600rpx;
		margin-bottom: 100rpx;
	}

	.editor-tab {
		background: #ffffff;
		height: 188rpx;
		padding: 8rpx;
	}

	.big-tab {
		background: #f2f2f2;
		margin-top: 4rpx;
	}
	
	.tab-item {
		//border-bottom: 4rpx none;
	}
	
	.tab-color-red {
		background: #f2e2e2;
	}
	.tab-color-green {
		background: #e2f2e2;
	}
	.tab-color-blue {
		background: #e2e2f2;
	}
	.tab-color-default {
		background: #ffffff;
	}
	
	.editor-item-container {
		flex-direction: column;
		justify-content: center;
		text-align: center;
		padding: 4rpx;
		font-weight: bold;
	}

	.editor-item {
		width: 120rpx;
		height: 120rpx;
		border: 4rpx none #EFEFEF;
		border-radius: 20rpx;
		//will-change: transform;
	}
	
	.editor-item-big {
		width: 160rpx;
		height: 160rpx;
		border: 6rpx solid #EFEFEF;
		border-radius: 20rpx;
	}
	
	.editor-item-label {
		//margin-bottom: 8rpx;
		//padding-bottom: 8rpx;
	}
	
	.signin-button {
		width:130pt;
		height:30pt;
		radius: 6pt;
	}
	
</style>
