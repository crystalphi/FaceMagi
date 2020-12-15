<template>


	<view class="ts-flex ts-column ts-full-width">

		<view class="ts-flex ts-flex-item">
			<ts-segmented-control class="ts-flex ts-flex-item" :values="tabs" :current="currentTab" @clickItem="onClickItem"></ts-segmented-control>
		</view>

		<view v-show="currentTab == 0">
			<!-- 全部 -->
			<view class="ts-flex ts-column ts-full-width">

				<block v-for="(item,index1) in orderData.items" :key="index1">

					<view class="ts-padding" style="justify-content: space-between;">
						<view>
							<ts-badge :text="item.actionType" type="error"></ts-badge>
							<text class="ts-padding-left">{{item.orderTime}}</text>
						</view>
						<ts-tag :text="item.status" type="error" :inverted="true"></ts-tag>
					</view>


					<view class="ts-column ts-flex-item">
						<view class="ts-list">
							<block v-for="(subOrderItem,index2) in item.items" :key="index2">

								<view class="ts-list-cell">
									<view class="ts-list-cell-navigate">
										<view class="product-cover">
											<image src="http://via.placeholder.com/80x80"></image>
										</view>
										<view class="ts-column ts-flex-item ts-padding-left">
											<view class="">{{subOrderItem.title}}</view>
											<view class="" style="justify-content: space-between;">
												<view class="">标题</view>
												<view class="">赚4.90</view>
											</view>
											<view class="" style="justify-content: space-between; ">
												<view class="">{{subOrderItem.price/100}}</view>
												<view class="">x{{subOrderItem.count}}</view>
											</view>
										</view>
									</view>
								</view>

							</block>

						</view>

						<view class="ts-column ts-padding ts-flex-item">
							<view style="justify-content: flex-end;">
								<view class="">共1件商品</view>
								<view class="ts-padding-left">总计：￥49.00元</view>
							</view>
							<view class="ts-pull-right">
								<view class="ts-margin-top">
									<button type="primary" size="mini">查看物流</button>
								</view>
							</view>
						</view>

					</view>

					<view class="ts-gap"></view>

				</block>

			</view>
		</view>

		<view v-show="currentTab == 1">
			<!-- 待付款 -->
			<view class="ts-flex ts-column ts-full-width">

				<view class="ts-padding" style="justify-content: space-between;">
					<view class="">
						<ts-badge text="买" type="error"></ts-badge>
						<text class="ts-padding-left">2018-10-11 13:39</text>
					</view>
					<ts-tag text="待付款" type="error" :inverted="true"></ts-tag>
				</view>

				<view class="ts-column ts-flex-item">
					<view class="ts-list">
						<view class="ts-list-cell">
							<view class="ts-list-cell-navigate">
								<view class="product-cover">
									<image src="http://via.placeholder.com/80x80"></image>
								</view>
								<view class="ts-flex-item ts-column ts-padding-left">
									<view class="">标题</view>
									<view class="" style="justify-content: space-between;">
										<view class="">标题</view>
										<view class="">赚4.90</view>
									</view>
									<view class="" style="justify-content: space-between; ">
										<view class="">￥49.00</view>
										<view class="">x1</view>
									</view>
								</view>
							</view>
						</view>
					</view>

					<view class="ts-column ts-padding ts-flex-item">
						<view style="justify-content: flex-end;">
							<view class="">共1件商品</view>
							<view class="ts-padding-left">总计：￥49.00元</view>
						</view>
						<view class="ts-pull-right">
							<view class="ts-margin-top">
								<button type="primary" size="mini">查看物流</button>
							</view>
						</view>
					</view>

				</view>
			</view>
		</view>


		<view v-show="currentTab == 2">
			<!-- 待收货 -->
			<view class="ts-flex ts-column ts-full-width">
				<view class="ts-padding" style="justify-content: space-between;">
					<view class="">
						<ts-badge text="卖" type="error"></ts-badge>
						<text class="ts-padding-left">2018-10-11 13:39</text>
					</view>
					<ts-tag text="已发货" type="error" :inverted="true"></ts-tag>
				</view>

				<view class="ts-column ts-flex-item">
					<view class="ts-list">
						<view class="ts-list-cell">
							<view class="ts-list-cell-navigate">
								<view class="product-cover">
									<image src="http://via.placeholder.com/80x80"></image>
								</view>
								<view class="ts-flex-item ts-column ts-padding-left">
									<view class="">标题</view>
									<view class="" style="justify-content: space-between;">
										<view class="">标题</view>
										<view class="">赚4.90</view>
									</view>
									<view class="" style="justify-content: space-between; ">
										<view class="">￥49.00</view>
										<view class="">x1</view>
									</view>
								</view>
							</view>
						</view>
					</view>

					<view class="ts-column ts-padding ts-flex-item">
						<view style="justify-content: flex-end;">
							<view class="">共1件商品</view>
							<view class="ts-padding-left">总计：￥49.00元</view>
						</view>
						<view class="ts-pull-right">
							<view class="ts-margin-top">
								<button type="primary" size="mini">查看物流</button>
							</view>
						</view>
					</view>

				</view>
			</view>
		</view>

		<view v-show="currentTab == 3">
			<!-- 已完成 -->
			<view class="ts-flex ts-column ts-full-width">

				<view class="ts-padding" style="justify-content: space-between;">
					<view class="">
						<ts-badge text="卖" type="error"></ts-badge>
						<text class="ts-padding-left">2018-10-11 13:39</text>
					</view>
					<ts-tag text="已签收" type="error" :inverted="true"></ts-tag>
				</view>

				<view class="ts-column ts-flex-item">
					<view class="ts-list">
						<view class="ts-list-cell">
							<view class="ts-list-cell-navigate">
								<view class="product-cover">
									<image src="http://via.placeholder.com/80x80"></image>
								</view>
								<view class="ts-flex-item ts-column ts-padding-left">
									<view class="">标题</view>
									<view class="" style="justify-content: space-between;">
										<view class="">标题</view>
										<view class="">赚4.90</view>
									</view>
									<view class="" style="justify-content: space-between; ">
										<view class="">￥49.00</view>
										<view class="">x1</view>
									</view>
								</view>
							</view>
						</view>
					</view>

					<view class="ts-column ts-padding ts-flex-item">
						<view style="justify-content: flex-end;">
							<view class="">共1件商品</view>
							<view class="ts-padding-left">总计：￥49.00元</view>
						</view>
						<view class="ts-pull-right">
							<view class="ts-margin-top">
								<button type="primary" size="mini">查看物流</button>
							</view>
						</view>
					</view>

				</view>
			</view>
		</view>

	</view>


</template>


<script>
	export default {
		components: {

		},
		data() {
			return {
				keywords: '',
				currentTab: 0,
				tabs: ['全部', '待付款', '待收货', '已完成'],

				orderData: {
					items: [],
					count: 0,
				},
			};
		},
		onLoad(e) {
			setTimeout(()=>{
					this.currentTab = parseInt(e.tab);
			},100)
		

			let subOrderData = {
				items: [],
				actionType: '买',
				orderTime: '2018-10-11 13:39',
				status: '已发货'
			};

			for (let i = 0; i < 3; i++) {
				subOrderData.items.push({
					title: `商品名称${i}`,
					productId: i,
					count: 2,
					price: 4900,
				})
			}

			this.orderData.items.push(subOrderData);
			this.orderData.items.push(subOrderData);
			this.orderData.items.push(subOrderData);

		},
		methods: {
			onClickItem(index) {
				// console.log('CurrentTab:' + this.currentTab)
				if (this.currentTab !== index) {
					this.currentTab = index;
				}
			},
		},

	}
</script>

<style>
	.product-cover {
		width: 200upx;
		height: 200upx;
	}

	.product-cover image {
		width: 100%;
		height: 100%;
	}
</style>
