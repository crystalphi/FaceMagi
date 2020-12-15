<template>
	<view class="page-section">
		<block v-if="hasLogin">
			<view class="ts-column" style=" background-color:#FFF;">
				<view class="ts-flex ts-row">
					<view class="ts-list-cell-navigate ts-navigate-right ts-navigate-badge" hover-class="ts-list-cell-hover" @tap="navigateTo('profile/profile')">
						<view class="ts-flex ts-row">
							<image class="app-avator" :src="userInfo.avator"></image>
							<view class="ts-flex ts-column ts-padding-left">
								<view>{{userInfo.username}}</view>
								<view>{{userInfo.mobile}}</view>
							</view>
						</view>
						<view class="ts-pull-right" v-if="userInfo.mobile">

							<ts-badge text="实名认证" type="error"></ts-badge>
						</view>
					</view>
				</view>

				<view class="ts-flex ts-column ts-flex-item" style="margin-left: 20upx; margin-right: 20upx; color: #FFFFFF;  border-top-right-radius: 20upx; border-top-left-radius: 20upx; background-color: #46A4DA;">
					<view class="ts-flex ts-row">
						<view class="ts-flex ts-column ts-flex-item ts-center ts-padding">
							<text>累计收益(元)</text>
							<text class="ts-h3">0.00</text>
						</view>
					</view>
					<view class="ts-flex ts-row">

						<navigator hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
								<text>0</text>
								<text>订单数</text>
							</view>
						</navigator>
						<navigator hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
								<text>0</text>
								<text>粉丝数</text>
							</view>
						</navigator>
						<navigator hover-class="navigator-hover" class="ts-flex-item">
							<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
								<text>0</text>
								<text>会员数</text>
							</view>
						</navigator>
					</view>
				</view>
				<view class="ts-flex ts-row">
					<navigator hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text>0.00</text>
							<text>余额(元)</text>
						</view>
					</navigator>

					<navigator hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text>0.00</text>
							<text>待入账(元)</text>
						</view>
					</navigator>

					<navigator hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text>0</text>
							<text>U币</text>
						</view>
					</navigator>

					<navigator hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text>0</text>
							<text>优惠券</text>
						</view>
					</navigator>
				</view>

			</view>
			<view class="ts-gap"></view>
			<view class="ts-list">
				<view class="ts-list-cell" hover-class="ts-list-cell-hover">
					<view class="ts-list-cell-navigate ts-navigate-right ts-navigate-badge">
						微友管家
						<ts-badge text="团队管理" type="default" inverted></ts-badge>
					</view>
				</view>
				<view class="ts-flex ts-row">

					<navigator url="member-jixiao" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>会员绩效</text>
						</view>
					</navigator>

					<navigator url="member-gaikuang" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>会员概况</text>
						</view>
					</navigator>

					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>会员明细</text>
						</view>
					</navigator>

					<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
						<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
						<text>帮助中心</text>
					</view>
				</view>

				<view class="ts-gap"></view>
				<view class="ts-list-cell" hover-class="ts-list-cell-hover">
					<view class="ts-list-cell-navigate ts-navigate-right ts-navigate-badge">
						我的店铺
						<ts-badge text="自营店铺" type="default" inverted></ts-badge>
					</view>
				</view>
				<view class="ts-flex ts-row">
					<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
						<text>0.00</text>
						<text>今日订单</text>
					</view>
					<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
						<text>0.00</text>
						<text>本月订单</text>
					</view>
					<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
						<text>0</text>
						<text>营业额</text>
					</view>
				</view>

				<view class="ts-gap"></view>

				<view class="ts-list-cell" hover-class="ts-list-cell-hover" @tap="navigateTo('order?tab=0')">
					<view class="ts-list-cell-navigate ts-navigate-right ts-navigate-badge">
						订单中心
						<ts-badge text="查看全部订单" type="default" inverted></ts-badge>
					</view>
				</view>


				<view class="ts-flex ts-row">

					<navigator url="order?tab=1" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>待付款</text>
						</view>
					</navigator>

					<navigator url="order?tab=2" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>待收货</text>
						</view>
					</navigator>

					<navigator url="order?tab=3" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>已完成</text>
						</view>
					</navigator>
					<navigator url="order?tab=4" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image style="width: 80upx; height: 80upx;" src="../../static/photo.jpg"></image>
							<text>售后/退款</text>
						</view>
					</navigator>
				</view>
			</view>


			<view class="ts-gap"></view>
			<ts-list>
				<ts-list-item title="购物车" @click="gotoCart()"></ts-list-item>
				<ts-list-item title="我的地址" :showBadge="true" badgeText="收货地址" @click="navigateTo('address/list')"></ts-list-item>
				<!-- <ts-list-item title="我的账户" @click="navigateTo('/pages/app/esc/job/demand/my-applied-job')"></ts-list-item> -->
			</ts-list>


			<view class="ts-flex ts-column ts-flex-item" style="margin: 20upx; border-radius: 20upx; background-color:#FFF;">
				<view class="ts-center ts-padding-top">
					<text style="font-size: 48upx;">招聘管理</text>
				</view>
				<ts-line></ts-line>

				<view class="ts-row">
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text class="ts-h2 ts-text-bold ts-text-error">5个</text>
							<text class="ts-h2">本月邀请面试</text>
						</view>
					</navigator>
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text class="ts-h2 ts-text-bold ts-text-error">1个</text>
							<text class="ts-h2">本月面试成功记录</text>
						</view>
					</navigator>
				</view>


				<view class="ts-row">
					<navigator url="/pages/app/esc/job/demand/my-dispatched-company-list" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>发布岗位</text>
						</view>
					</navigator>
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>简历管理</text>
						</view>
					</navigator>
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>公司管理</text>
						</view>
					</navigator>
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>人才收藏</text>
						</view>
					</navigator>
				</view>
			</view>





			<view class="ts-flex ts-column ts-flex-item" style="margin: 20upx; border-radius: 20upx;  background-color:#FFF;">
				<view class="ts-center ts-padding-top">
					<text style="font-size: 48upx;">求职管理</text>
				</view>
				<ts-line></ts-line>

				<view class="ts-row">
					<navigator url="/pages/app/esc/job/demand/my-applied-job'" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text class="ts-h2 ts-text-bold ts-text-error">5个</text>
							<text class="ts-h2">简历投递记录</text>
						</view>
					</navigator>
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<text class="ts-h2 ts-text-bold ts-text-error">1个</text>
							<text class="ts-h2">面试记录</text>
						</view>
					</navigator>
				</view>



				<view class="ts-row">
					<navigator url="/pages/app/esc/job/finder/my-resume" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>发布简历</text>
						</view>
					</navigator>
					<navigator url="/pages/app/esc/job/finder/my-resume" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>简历管理</text>
						</view>
					</navigator>
					<navigator url="/pages/app/esc/job/finder/my-resume" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>档案管理</text>
						</view>
					</navigator>
					<navigator url="member-mingxi" hover-class="navigator-hover" class="ts-flex-item">
						<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
							<image class="app-icon" src="../../static/plus.png"></image>
							<text>岗位收藏</text>
						</view>
					</navigator>
				</view>
			</view>


			<view class="ts-gap"></view>
			<ts-list>
				<ts-list-item title="创业大赛" note="我参加的创业大赛项目" @click="navigateTo('/pages/app/syb/match/my-match')"></ts-list-item>
			</ts-list>

			<view class="ts-gap"></view>



			<ts-list>
				<ts-list-item title="分享" thumb="https://img-cdn-qiniu.dcloud.net.cn/new-page/hx.png" note="推广给好友获得积分" @click="navigateTo('share')"></ts-list-item>
				<ts-list-item title="清除缓存" @click="handleClearStorage()"></ts-list-item>
				<ts-list-item title="关于" thumb="https://img-cdn-qiniu.dcloud.net.cn/new-page/uni.png" :showBadge="true" badgeText="1.0.0"
				 badgeType="error" @click="navigateTo('about')"></ts-list-item>
			</ts-list>
		</block>
		<view class="ts-row">
			<view class="btn-row">
				<button v-if="!hasLogin" @tap="bindLogin" type="primary">登录</button>
				<button v-if="hasLogin" type="warn" @tap="bindLogout">退出登录</button>
			</view>
		</view>
	</view>
</template>

<script>
	import {
		mapState,
		mapMutations,
		mapActions
	} from 'vuex'

	export default {
		components: {

		},
		data() {
			return {

				hasUserInfo: false,
				userInfo: {
					avatarUrl: '../../static/photo.png',
					nickName: '用户名',
				}
			}
		},
		computed: {
			...mapState(['hasLogin', 'userType']),
		},
		async onLoad() {
			if (this.hasLogin) {
				//必须先登录才能获取用户的信息
				this.hasUserInfo = true;
				this.userInfo = await this.getUserInfo();
				this.$logger.debug(this.$logger.dump(this.userInfo));
			}
		},

		onUnload() {

		},
		onShow: async function() {


			// 			if (!this.hasUserInfo) {
			// 				uni.getUserInfo({
			// 					provider: this.loginProvider,
			// 					success: (e) => {
			// 						console.log("得到用户信息", e);
			// 						this.hasUserInfo = true;
			// 						this.userInfo = e.userInfo
			// 					},
			// 					fail: (e) => {
			// 						console.log("fail", e);
			// 						let content = e.errMsg;
			// 						if (~content.indexOf("uni.login")) {
			// 							//content = "请在登录页面完成登录操作"
			// 						}
			// 					}
			// 				});
			// 			}
		},
		onNavigationBarButtonTap(e) {
			uni.navigateTo({
				url: '/platforms/app-plus/about/about'
			})
		},
		methods: {

			// ...mapMutations(['logout']),
			// ...mapActions(['getUserInfo', 'logout']),
			...mapActions({
				getUserInfo: 'user/getUserInfo',
				logout: 'logout'
			}),

			bindLogin() {
				uni.navigateTo({
					url: '../auth/login',
				});
			},

			bindLogout() {

				this.logout();
				uni.reLaunch({
					url: '/pages/tabbar/home/index',
				})
				/**
				 * 如果需要强制登录跳转回登录页面
				 */
				// if (this.forcedLogin) {
				// 	uni.reLaunch({
				// 		url: '../auth/login',
				// 	});
				// }
			},
			handleClearStorage() {
				this.logout();
				uni.showToast({
					title: '缓存已清理',
				})
			},
			navigateTo(url = '') {
				if (url) {
					uni.navigateTo({
						url: url,
					})
				}
			},
			gotoCart() {
				uni.navigateTo({
					url: '/pages/my/shopingcart/index'
				});
			},
		}
	}
</script>

<style scoped lang="scss">
	// 	page {
	// 		// background: $uni-bg-color-grey;
	// 		background-color: #007AFF;
	// 	}
	// 

	page {
		background-color: #f1f1f1;
	}

	.page-section {
		display: flex;
		flex: 1;
		flex-direction: column;
		justify-content: flex-start;
	}

	.ts-section {
		margin-left: 20upx;
		margin-right: 20upx;
		// color: #FFFFFF;
		border-top-right-radius: 20upx;
		border-top-left-radius: 20upx;
		// background-color: #46A4DA;
	}

	.ts-section-title {
		text-align: center;
	}

	.btn-row {
		margin: 50upx 20upx;
		display: flex;
		flex: 1;
		flex-direction: row;
	}

	.btn-row button {
		justify-content: center;
		align-items: center;
		display: flex;
		flex-direction: row;
		flex: 1;
	}
</style>
