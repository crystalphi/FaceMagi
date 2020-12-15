<template>
	<view class="ts-city-picker">
		<view class="ts-popup-wraper">
			<view class="ts-mask" v-show="!hiddenPopupWindow" @click="closePopupWindow"></view>
			<view class="ts-popup ts-popup-bottom" v-show="!hiddenPopupWindow">
				<view class="ts-row ts-padding ts-flex-item" style="justify-content: space-between;">
					<view class="ts-text-bold">当前城市: {{currentCity}}</view>
					<view><button @tap="selectCity" type="warn" size="mini">确定</button></view>
				</view>
			</view>
		</view>

		<view class="search-box-wraper">
			<view class="search-box-title">{{currentCity}}</view>
			<input placeholder="中文/拼音/首字母" class="search-box" @input='bindSarchInput' placeholder-class='search-input-placeholder' />
		</view>

		<view class='a-z-wraper'>
			<block v-for="(item, index) in cityAZ" :key="index">
				<view class="a-z-item" :data-id="item.cityName" @tap='bindAZ'>{{item.cityName}}</view>
			</block>
		</view>

		<view class="ts-flex ts-column ts-flex-item">

			<view class='city-item-content'>
				<view v-for="(item, index) in cityResults" :key="index">
					<view v-if="item.cityPinYin.length > 1" class="city-item" :data-cityname="item.cityName" @tap='citySelected'>{{item.cityName}}</view>
					<view v-else class="city-item-A-Z" :data-cityname="item.cityName">{{item.cityName}}</view>
				</view>
			</view>
		</view>
	</view>
</template>
<style>
	page view {
		display: flex;
		flex-direction: row;
	}

	.ts-city-picker {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.search-box-wraper {
		position: fixed;
		top: 0;
		display: flex;
		flex-direction: row;
		width: 100%;
		background: #eee;
		font-size: 30upx;
		align-items: center;
		padding: 10upx;
	}

	.search-box-title {
		display: flex;
		flex-direction: row;
		width: 150upx;

		justify-content: flex-end;
		padding-right: 20upx;
	}

	.search-box {
		display: flex;
		flex-direction: row;
		flex: 1;

		height: 70upx;
		line-height: 60upx;
		border-radius: 10upx;
		background: #fff;
		font-size: 26upx;
		margin-right: 20upx;
	}

	.search-input-placeholder {
		text-align: center;
	}

	.currentCity {

		width: 90%;
		height: 90upx;
		line-height: 90upx;
		font-size: 30upx;
		padding-left: 5%;
		background-color: #fff;
	}

	.a-z-wraper {
		display: block;

		width: 40upx;
		position: fixed;
		top: 100upx;
		text-align: center;
		justify-content: center;
		align-content: center;
		right: 5upx;
		color: #3F51B5;

	}

	.a-z-item {
		font-size: 30upx;
	}

	.city-item-content {
		margin-top: 90upx;


		padding: 10upx;
		display: flex;
		flex-direction: column;
		flex: 1;
		justify-content: center;
		background-color: #fff;
		margin-right: 50upx;


	}

	.city-item {
		display: flex;
		flex-direction: column;
		flex: 1;

		background: #fff;
		width: 90%;
		padding-left: 5%;
		height: 90upx;
		font-size: 30upx;
		line-height: 100upx;
		border-bottom: 1upx solid #d1d1d1;
	}

	.city-item-A-Z {
		width: 95%;
		height: 90upx;
		line-height: 90upx;
		font-size: 30upx;
		padding-left: 5%;
		background-color: #f6f6f6;
		color: #999;
	}

	.ts-popup-wraper {
		display: flex;
		flex-direction: row;
		justify-content: flex-start;
		align-content: flex-start;
	}

	/* 遮罩层 */
	.ts-mask {
		background: rgba(0, 0, 0, 0.6);
		position: fixed;
		width: 100%;
		height: 100%;
		left: 0;
		top: 0;
		z-index: 1000;
	}

	/* 弹出层形式的广告 */
	.ts-popup {
		position: fixed;
		display: flex;
		flex-direction: column;
		flex: 1;
		z-index: 1001;
		background-color: #ffffff;
		-webkit-box-shadow: 0 0 30px rgba(0, 0, 0, .1);
		box-shadow: 0 0 30px rgba(0, 0, 0, .1);
	}

	.ts-popup-bottom {
		bottom: 0;
		width: 100%;
	}

	.ts-popup-top {
		top: 0;
		width: 100%;
	}
</style>
<script>
	var pixelRatio = 1;
	import cityData from '../common/city-data.js';

	export default {
		name: 'ts-city-picker',
		components: {},
		mounted: function() {
			if (this.cityResults == null) {
				this.cityResults = this.citys;
			}
			var winInfo = wx.getSystemInfo({
				success: function(res) {
					pixelRatio = 750 / res.windowWidth;
				}
			});
		},
		onPageScroll: function(e) {
			this.scrollNow = e.scrollTop;
		},
		methods: {
			bindAZ: function(e) {
				var currentCityName = e.currentTarget.dataset.id
				var that = this;
				if (that.scrollAZ == null) {
					uni.createSelectorQuery().selectAll('.city-item-A-Z').fields({
						dataset: true,
						size: true,
						rect: true
					}, function(res) {
						res.forEach(function(re) {
							if (currentCityName == re.dataset.cityname) {
								uni.pageScrollTo({
									scrollTop: re.top + that.scrollNow - 100 / pixelRatio,
									duration: 0
								})
							}
						})
					}).exec();
				} else {
					that.scrollAZ.forEach(function(re) {
						if (currentCityName == re.dataset.cityname) {
							uni.pageScrollTo({
								scrollTop: re.top + that.scrollNow - 100 / pixelRatio,
								duration: 0
							})
						}
					})
				}
			},
			citySelected: function(e) {
				var cityNameTemp = e.currentTarget.dataset.cityname;

				this.currentCity = cityNameTemp;
				// 				uni.showToast({
				// 					title: cityNameTemp,
				// 					icon: 'none'
				// 				});
				// console.log(this.currentCity);
				//显示弹出窗口
				this.hiddenPopupWindow = false;
			},
			bindSarchInput: function(e) {
				uni.pageScrollTo({
					scrollTop: 0,
					duration: 0
				});
				var inputVal = e.detail.value;
				var cityResultsTemp = new Array()
				var citys = this.citys;
				if (inputVal == null || inputVal.trim() == '') {
					this.cityResults = citys;
					return;
				}
				for (var i = 0; i < citys.length; i++) {
					if (citys[i].cityName.indexOf(inputVal) == 0 || citys[i].cityPY.indexOf(inputVal.toLowerCase()) == 0 || citys[i].cityPinYin
						.indexOf(inputVal.toLowerCase()) == 0) {
						//去除热门城市
						if (citys[i].cityPY.indexOf("#") != -1) {
							continue;
						}
						var ifHas = false;
						for (var j = 0; j < cityResultsTemp.length; j++) {
							if (cityResultsTemp[j] == citys[i]) {
								ifHas = true;
								break;
							}
						}
						if (!ifHas) {
							cityResultsTemp.push(citys[i]);
						}
					}
				}
				this.cityResults = cityResultsTemp;
			},

			closePopupWindow: function() {
				this.hiddenPopupWindow = true;
			},
			selectCity: function() {
				this.$emit('change', this.currentCity);
				this.hiddenPopupWindow = true;
			}
		},
		data() {
			return Object.assign({},
				cityData, {
					hiddenPopupWindow: true,
					currentCity: "北京市",
					scrollAZ: null,
					scrollNow: 0,
					cityResults: null,
				}
			)
		}
	}
</script>
