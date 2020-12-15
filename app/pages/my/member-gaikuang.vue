<template>
	<view class="ts-flex ts-column ts-flex-item">

		<view class="ts-flex ts-row">
			<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
				<text class="ts-h6">总会员数</text>
				<text>26</text>
			</view>
			<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
				<text class="ts-h6">有效会员数</text>
				<text>26</text>
			</view>
			<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
				<text class="ts-h6">会员累计销售额</text>
				<text>12.5万</text>
			</view>
		</view>


		<view class="ts-gap"></view>
		<view class="ts-flex ts-column ts-flex-item">
			<view class="ts-flex ts-flex-item">
				<ts-segmented-control class="ts-flex ts-flex-item" :values="tabs" :current="currentTab" @clickItem="onClickItem"></ts-segmented-control>
			</view>
			<view class="ts-flex ts-column ts-flex-item ts-padding-top">
				<view v-show="currentTab == 0">
					<view class="ts-flex ts-column ts-flex-item">
						<view class="table">
							<view class="table-head">
								<view class="table-col">
									店主姓名
								</view>
								<view class="table-col">
									邀请人/导师
								</view>
								<view class="table-col">
									加盟时间
								</view>
								<view class="table-col">
									累计收益
								</view>
							</view>
							<block v-for="(item ,index) in memberData" :key="index">
								<view class="table-row">
									<view class="table-col">
										{{item.name}}
									</view>
									<view class="table-col">
										{{item.inviter}}
									</view>
									<view class="table-col">
										{{item.date}}
									</view>
									<view class="table-col">
										{{item.volume}}
									</view>
								</view>
							</block>
						</view>
					</view>
				</view>


				<view v-show="currentTab == 1">
					<view class="ts-flex ts-column ts-flex-item">
						<view class="table">
							<view class="table-head">
								<view class="table-col">
									店主姓名
								</view>
								<view class="table-col">
									邀请人/导师
								</view>
								<view class="table-col">
									加盟时间
								</view>
								<view class="table-col">
									累计收益
								</view>
							</view>
							<block v-for="(item ,index) in goldMemberData" :key="index">
								<view class="table-row">
									<view class="table-col">
										{{item.name}}
									</view>
									<view class="table-col">
										{{item.inviter}}
									</view>
									<view class="table-col">
										{{item.date}}
									</view>
									<view class="table-col">
										{{item.volume}}
									</view>
								</view>
							</block>
						</view>
					</view>
				</view>


				<view v-show="currentTab == 2">
					<view class="ts-flex ts-column ts-flex-item">
						<view class="table">
							<view class="table-head">
								<view class="table-col">
									店主姓名
								</view>
								<view class="table-col">
									邀请人/导师
								</view>
								<view class="table-col">
									加盟时间
								</view>
								<view class="table-col">
									累计收益
								</view>
							</view>
							<block v-for="(item ,index) in normalMemberData" :key="index">
								<view class="table-row">
									<view class="table-col">
										{{item.name}}
									</view>
									<view class="table-col">
										{{item.inviter}}
									</view>
									<view class="table-col">
										{{item.date}}
									</view>
									<view class="table-col">
										{{item.volume}}
									</view>
								</view>
							</block>
						</view>
					</view>
				</view>

			</view>
		</view>

	</view>
</template>


<script>
	var self;




	export default {
		components: {


		},
		data() {
			return {

				keywords: '',
				currentTab: 0,
				tabs: ['全部会员', '金牌会员', '普通会员'],

				memberData: []
			};
		},
		computed: {
			goldMemberData() {
				return this.memberData.filter(item => item.type == '金牌');
			},
			normalMemberData() {
				return this.memberData.filter(item => item.type == '普通');
			}
		},
		onLoad: function(e) {
			self = this;

			for (let i = 1; i <= 10; i++) {
				this.memberData.push({
					name: `user ${i}`,
					inviter: `Inviter ${i}`,
					date: '2018-01-01',
					volume: Math.round(Math.random() * 100000) / 100.0,
					type: '金牌',
				})
			}

			for (let i = 11; i <= 20; i++) {
				this.memberData.push({
					name: `user ${i}`,
					inviter: `Inviter ${i}`,
					date: '2018-01-01',
					volume: Math.round(Math.random() * 10000) / 100.0,
					type: '普通',
				})
			}

		},
		methods: {
			onClickItem(index) {
				if (this.currentTab !== index) {
					this.currentTab = index;
				}
			},
		},

	}
</script>

<style>
	/* 	page view {
		display: flex;
		flex-direction: row;
		font-size: 28upx;
	} */

	page {
		min-height: 100%;
	}


	.table {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.table-row {
		display: flex;
		flex-direction: row;
		width: 100%;
		border-top: #C0C0C0 solid 1upx;
		height: 80upx;
		justify-content: center;
		align-items: center;
	}

	.table-row:nth-child(odd) {
		background: #EEEEEE;
	}

	.table-head {
		display: flex;
		flex-direction: row;
		width: 100%;
		border-top: #C0C0C0 solid 1upx;
		height: 80upx;
		justify-content: center;
		align-items: center;

		font-weight: bold;
		color: #FFF;
		background-color: #000000;
	}

	.table-row:last-child {
		border-bottom: #C0C0C0 solid 1upx;
	}

	.table-col {
		display: flex;
		flex: 1;
		justify-content: center;
		align-items: center;
	}
</style>
