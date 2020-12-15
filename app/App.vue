<script>
	//import request from '@/common/request.js';
	import Vue from 'vue'
	
	export default {
		onLaunch: function() {
			//console.log('App Launch');
			//#ifdef APP-PLUS
			/* 5+环境锁定屏幕方向 */
			plus.screen.lockOrientation("portrait-primary"); //锁定
			/* 5+环境升级提示 */
			//var server = "http://www.zengqs.com/update"; //检查更新地址
			var server = "http://192.168.212.143:8360/update/index"; //检查更新地址
			var req = {
				//升级检测数据
				appid: plus.runtime.appid, //要更新的客户端，统一平台支持多客户端
				version: plus.runtime.version,
				imei: plus.device.imei,
				os: plus.os.name
			};
			//{"appid":"HBuilder","version":"9.1.23","imei":"861141032461568,861141030109839","os":"Android"}
			//console.log('update request:' + JSON.stringify(req))
			//http://192.168.212.143:8360/update/index?appid=HBuilder&version=9.1.23&imei=861141032461568,861141030109839&os=Android
			//服务端返回数据类型
			//      {
			//        status:true, //是否需要更新，true|false
			//        url:'http://www.zengqs.com/data/uniapp-labs.apk',//根据请求的操作系统类型动态生成下载的链接
			//        version:'1.0', //新的版本号
			//        note:'',//升级说明文字
			//      }
			//				const res = await request.get(server, req);
			//				console.log("update server response:" + JSON.stringify(res));
			//				//{"errno":0,"errmsg":"","data":{"status":true,"url":"http://www.zengqs.com/data/uniapp-labs.apk","version":"1.0","note":""}}
			//				if (res.data.status) {
			//					//提示用于检测到新的版本，是否更新
			//					uni.showModal({ //提醒用户更新
			//						title: '更新提示',
			//						content: res.data.note ? res.data.note : `检测到新的版本${res.data.version}，是否选择更新?`,
			//						success: function(res1) {
			//							if (res1.confirm) {
			//								plus.runtime.openURL(res.data.url);
			//							}
			//						}
			//					});
			//				}
			//#endif

			//this.$store.dispatch('loadStorage'); //加载本地缓存的数据

			//colorui组件库所需的系统信息
			uni.getSystemInfo({
				success: function(e) {
					//#ifndef MP
					Vue.prototype.StatusBar = e.statusBarHeight;
					if (e.platform == 'android') {
						Vue.prototype.CustomBar = e.statusBarHeight + 50;
					} else {
						Vue.prototype.CustomBar = e.statusBarHeight + 45;
					};
					//#endif
					//#ifdef MP-WEIXIN
					Vue.prototype.StatusBar = e.statusBarHeight;
					let custom = wx.getMenuButtonBoundingClientRect();
					Vue.prototype.Custom = custom;
					Vue.prototype.CustomBar = custom.bottom + custom.top - e.statusBarHeight;
					//#endif		
					//#ifdef MP-ALIPAY
					Vue.prototype.StatusBar = e.statusBarHeight;
					Vue.prototype.CustomBar = e.statusBarHeight + e.titleBarHeight;
					//#endif
				}
			});
			
			//用户登录后的全局信息，在各页面的 data 部分中可以通过 this.gLoginInfo 获取。
			Vue.prototype.gLoginInfo = {};
			
			//应用功能列表 - 化妆
			Vue.prototype.FaceMakeupList = [{
					name: "Fashion Makeup", //时尚化妆
					title: "Fashion",
					url: "fashion-makeup",
					info: "Hundreds of latest trends effects",
					desc: "[FACIAL STICKERS] Using facial recognition, create customized hairstyles, beards and eye wear stickers for men with just one touch. Exclusive women\'s hairstyles and eye wear stickers that let you freely try on new styles",
					color: 'cyan',
					icon: 'loading2'
				},
				{
					name: "Realtime Filters", //各种滤镜
					title: "Filters", /*'　'*/
					url: "realtime-filters",
					info: "Define your style with 100+ filters",
					desc: "Various Filter: Whether you want to create a fashionable, sweet, lazy, or everyday style, our filters can always help you! Real-time Skin and Facial Reshaping: Beautify your selfie when taking pictures, no need to edit afterwards!",
					color: 'blue',
					icon: 'colorlens'
				},
				{
					name: "Skin Tone", //调整肤色
					title: "Skin Tone",
					url: "skin-tone",
					info: "Make your skin tone and texture even out",
					desc: "Easily adjust your skin tone, whether you want bronze, dark or fair skin, Facetify can do it for you.",
					color: 'red',
					icon: 'myfill'
				},
				{
					name: "Auto Skin Retouch", //自动润色
					title: "Auto Retouch",
					url: "auto-skin-retouch",
					info: "Custom your own beauty effects",
					desc: "Smooth Skin: Creates smooth skin while keeping the area outside the skin unaffected, no longer have to worry about exaggerated smoothing!\nFix the redness: Cool down skin redness and give you healthy and natural skin.\nRosy skin – Rejuvenate pale skin and make it rosy and energetic.\nBright eyes - Brighten your eyes with a vibrant glow. \nGet rid of dark circles – Remove the annoying dark circles. \nTeeth whitening – Whiten your teeth and make your smile confident.",
					color: 'pink',
					icon: 'newsfill'
				},
				{
					name: "Manly Stickers", //曼利贴纸
					title: "Manly Stickers",
					url: "manly-stickers",
					info: "Change hair styles, beards and glasses in 1 min",
					desc: "Manly stickers description",
					color: 'green',
					icon: 'font'
				},
			];
			
			//应用功能列表 - 创意
			Vue.prototype.FaceCreativeList = [{
					name: "Convert Gender",
					title: "Convert Gender",
					url: "convert-gender",
					info: "Unlimit your imagination",
					desc: "Are you curious to know what you would look like as another gender?",
					color: 'orange',
					icon: 'home'
				},
				{
					name: "Time Machine",
					url: "time-machine",
					title: "See you in the future",
					desc: "[Aging] Journey thru time to see what you will look like in 30 years time",
					color: 'green',
					icon: 'home'
				},
				{
					name: "Dreamy Scene",
					url: "dream-scene",
					title: "One tap to transform scenes",
					desc: "[Face swap] To a wedding scene; be a mermaid princess; be like the Mona Lisa, or other such famous art subjects; there are a variety of character scenes for you to choose from",
					color: 'blue',
					icon: 'home'
				},
				{
					name: "Premium Frame",
					url: "premium-frames",
					title: "Use the frames to get creative",
					desc: "Choose from a variety of frames and backgrounds and improve your photos!",
					color: 'pink',
					icon: 'home'
				},
			];
		},
		onShow: function() {
			this.$logger.log("App Show");
		},
		onHide: function() {
			this.$logger.log("App Hide");
		}
	};
</script>

<style lang="scss">
	/* uni.css - 通用组件、模板样式库，可以当作一套ui库应用 */
	@import 'common/uni.css';

	/*teaset组件库的样式文件*/
	//@import "components/teaset/teaset.scss";

	/*colorui组件库的样式文件*/
	@import "colorui/main.css";
	@import "colorui/icon.css";

	.nav-list {
		display: flex;
		flex-wrap: wrap;
		padding: 0px 40upx 0px;
		justify-content: space-between;
	}

	.nav-li {
		padding: 30upx;
		border-radius: 12upx;
		width: 45%;
		margin: 0 2.5% 40upx;
		background-image: url(https://cdn.nlark.com/yuque/0/2019/png/280374/1552996358352-assets/web-upload/cc3b1807-c684-4b83-8f80-80e5b8a6b975.png);
		background-size: cover;
		background-position: center;
		position: relative;
		z-index: 1;
	}

	.nav-li::after {
		content: "";
		position: absolute;
		z-index: -1;
		background-color: inherit;
		width: 100%;
		height: 100%;
		left: 0;
		bottom: -10%;
		border-radius: 10upx;
		opacity: 0.2;
		transform: scale(0.9, 0.9);
	}

	.nav-li.cur {
		color: #fff;
		background: rgb(94, 185, 94);
		box-shadow: 4upx 4upx 6upx rgba(94, 185, 94, 0.4);
	}

	.nav-title {
		font-size: 32upx;
		font-weight: 300;
	}

	.nav-title::first-letter {
		font-size: 40upx;
		margin-right: 4upx;
	}

	.nav-name {
		font-size: 28upx;
		text-transform: Capitalize;
		margin-top: 20upx;
		position: relative;
	}

	.nav-name::before {
		content: "";
		position: absolute;
		display: block;
		width: 40upx;
		height: 6upx;
		background: #fff;
		bottom: 0;
		right: 0;
		opacity: 0.5;
	}

	.nav-name::after {
		content: "";
		position: absolute;
		display: block;
		width: 100upx;
		height: 1px;
		background: #fff;
		bottom: 0;
		right: 40upx;
		opacity: 0.3;
	}

	.nav-name::first-letter {
		font-weight: bold;
		font-size: 36upx;
		margin-right: 1px;
	}

	.nav-li text {
		position: absolute;
		right: 30upx;
		top: 30upx;
		font-size: 52upx;
		width: 60upx;
		height: 60upx;
		text-align: center;
		line-height: 60upx;
	}

	.text-light {
		font-weight: 300;
	}

	@keyframes show {
		0% {
			transform: translateY(-50px);
		}

		60% {
			transform: translateY(40upx);
		}

		100% {
			transform: translateY(0px);
		}
	}

	@-webkit-keyframes show {
		0% {
			transform: translateY(-50px);
		}

		60% {
			transform: translateY(40upx);
		}

		100% {
			transform: translateY(0px);
		}
	}
	
	/*项目定义的样式文件*/
	@import "common/variables.scss";

	/*项目定义的样式文件*/
	@import "common/app.scss";

	/* 以下样式用于 hello uni-app 演示所需 */
	page {
		background-color: #F4F5F6;
		height: 100%;
		font-size: 28upx;
		line-height: 1.8;
	}

	.uni-header-logo {
		padding: 30upx;
		text-align: center;
		margin-top: 10upx;
	}

	.uni-header-logo image {
		width: 140upx;
		height: 140upx;
	}

	.uni-hello-text {
		color: #7A7E83;
	}

	.uni-hello-addfile {
		text-align: center;
		line-height: 300upx;
		background: #FFF;
		padding: 50upx;
		margin-top: 10px;
		font-size: 38upx;
		color: #808080;
	}
</style>
