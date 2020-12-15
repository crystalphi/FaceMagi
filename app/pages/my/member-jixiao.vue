<template>
	<view class="ts-flex ts-column ts-flex-item">

		<view class="ts-flex ts-row ts-padding" style="justify-content: space-between; align-items: center;">
			<text class="ts-text-bold">2018年10月会员绩效</text>
			<view><button type="warn" size="mini">往期绩效</button></view>
		</view>
		<view class="ts-flex ts-row">
			<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
				<text class="ts-h6">本月社群销售额</text>
				<text>451.20</text>
			</view>
			<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
				<text class="ts-h6">本月社群新增人数</text>
				<text>0</text>
			</view>
			<view class="ts-flex ts-column ts-flex-item  ts-center ts-padding">
				<text class="ts-h6">会员活跃度</text>
				<text>11.54%</text>
			</view>
		</view>

		<view class="ts-gap"></view>


		<view class="ts-flex ts-row ts-padding">
			<text class="ts-text-bold">2018年会员新增人数及社区收益按月统计图</text>
		</view>
		<view class="ts-row">
			<view class="ts-flex ts-column ts-flex-item ts-padding" style="height: 500upx;">
				<mpvue-echarts :echarts="echarts" :onInit="lineInit" canvasId="line" />
			</view>
		</view>

		<view class="ts-gap"></view>
		<view class="ts-flex ts-flex-item ">
			<ts-segmented-control class="ts-flex ts-flex-item" :values="tabs" :current="currentTab" @clickItem="onClickItem"></ts-segmented-control>
		</view>

		<view class="ts-flex ts-column ts-flex-item">
			<view v-show="currentTab == 0">
				<view class="ts-flex ts-column ts-flex-item ts-padding-top">
					<view class="table">
						<view class="table-head">
							<view class="table-col">
								店主姓名
							</view>
							<view class="table-col">
								本月成交额
							</view>
						</view>
						<block v-for="(item,index) in memberData" :key="index">
							<view class="table-row">
								<view class="table-col">
									{{item.name}}
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
				<view class="ts-flex ts-column ts-flex-item ts-padding-top">
					<view class="table">
						<view class="table-head">
							<view class="table-col">
								店主姓名
							</view>
							<view class="table-col">
								本月成交额
							</view>
						</view>
						<block v-for="(item,index) in hasTraded" :key="index">
							<view class="table-row">
								<view class="table-col">
									{{item.name}}
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
				<view class="ts-flex ts-column ts-flex-item ts-padding-top">
					<view class="table">
						<view class="table-head">
							<view class="table-col">
								店主姓名
							</view>
							<view class="table-col">
								本月成交额
							</view>
						</view>
						<block v-for="(item,index) in noTraded" :key="index">
							<view class="table-row">
								<view class="table-col">
									{{item.name}}
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
</template>


<script>
	// import * as echarts from 'components/echarts/echarts.simple.min.js';
	import * as echarts from '@/components/echarts/echarts.common.min.js';

	import mpvueEcharts from '@/components/mpvue-echarts/src/echarts.vue';

	import * as utils from '@/common/util.js';



	function getLineOption() {
		return {
			animation: false,
			color: ['#37A2DA', '#F00'],
			legend: {
				type: 'plain',
				data: ['新增会员', '销售额']
			},
			grid: {
				x: 50,
				y: 50,
				x2: 50,
				y2: 20
			},
			calculable: false,
			xAxis: [{
				type: 'category',
				data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
			}],
			yAxis: [{
				name: '会员人数',
				type: 'value',
				axisLabel: {
					formatter: '{value}'
				},
				splitLine: {
					show: false
				},
				scale: true,
			}, {
				name: '销售额',
				type: 'value',
				axisLabel: {
					// formatter: '{value} 10<sup>6</sup>m³'
					formatter: '{value}'
				},
				splitLine: {
					show: false
				},
				scale: true,
			}],

			series: [{
				name: '新增会员',
				type: 'line',
				data: [2, 4, 22, 23, 2, 7, 13, 16, 8, 20, 6, 3],
				yAxisIndex: 0,
			}, {
				name: '销售额',
				type: 'line',
				data: [26, 9, 90, 64, 287, 707, 1756, 182.2, 48.7, 18.8, 6.0, 2.3],
				yAxisIndex: 1,
			}]
		}
	}

	var self;
	export default {
		components: {

			mpvueEcharts,
		},
		data() {
			return {
				echarts,
				lineInit: function(canvas, width, height) {
					let lineChart = echarts.init(canvas, null, {
						width: width,
						height: height
					});
					canvas.setChart(lineChart);

					lineChart.setOption(getLineOption());
					return lineChart;
				},
				currentTab: 0,
				tabs: ['全部', '已开单', '未开单'],
				memberData: [],
			};
		},
		onLoad: function(e) {
			self = this;

			for (let i = 1; i <= 20; i++) {
				this.memberData.push({
					name: `user ${i}`,
					volume: utils.formatMoney(Math.round((Math.random() * 5e6) * 100)), //单位为分
					hasTraded: true,
				})
			}

			for (let i = 21; i <= 30; i++) {
				this.memberData.push({
					name: `user ${i}`,
					volume: 0,
					hasTraded: false,
				})
			}

		},
		computed: {
			hasTraded() {
				return this.memberData.filter(item => item.hasTraded == true);
			},
			noTraded() {
				return this.memberData.filter(item => item.hasTraded == false);
			},

		},
		methods: {
			onClickItem(index) {

				if (this.currentTab !== index) {
					this.currentTab = index;
				}
				console.log(index);
			},
		},

	}
</script>

<style lang="scss">
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
