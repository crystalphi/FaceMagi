<template>

	<view class="ts-column ts-flex-item">

		<swiper :indicator-dots="true" :autoplay="true" :interval="3000" :duration="1000">
			<swiper-item>
				<view class="swiper-item">
					<ts-banner class="ts-row ts-flex-item" image="http://via.placeholder.com/750x375" :height="350"></ts-banner>
				</view>
			</swiper-item>
			<swiper-item>
				<view class="swiper-item">
					<ts-banner class="ts-row ts-flex-item" image="http://via.placeholder.com/750x375" :height="350"></ts-banner>
				</view>
			</swiper-item>
			<swiper-item>
				<view class="swiper-item">
					<ts-banner class="ts-row ts-flex-item" image="http://via.placeholder.com/750x375" :height="350"></ts-banner>
				</view>
			</swiper-item>

			<swiper-item>
				<view class="swiper-item">
					<ts-banner class="ts-row ts-flex-item" image="http://via.placeholder.com/750x375" :height="350"></ts-banner>
				</view>
			</swiper-item>


			<swiper-item>
				<view class="swiper-item">
					<ts-banner class="ts-row ts-flex-item" image="http://via.placeholder.com/750x375" :height="350"></ts-banner>
				</view>
			</swiper-item>

		</swiper>
		<ts-search-bar :keywords="keywords" @search="onSearch"></ts-search-bar>
		<view class="ts-row ts-flex-item">
			<ts-segmented-control class="ts-row ts-flex-item" :values="tabs" styleType="text" @clickItem="onClickItem"></ts-segmented-control>
		</view>


		<view class="ts-column" v-for="(item ,index) in searchResult" :key="index">
			<navigator :url="'/pages/app/lost/events/detail?id='+item.id">
				<view class="ts-section">
					<view class="ts-section-title">
						<view class="ts-row">
							<view class="ts-flex-item" style="align-items: flex-end;">
								<text class="ts-h2 ts-text-bold">{{item.linkman}}</text>
								<text class="ts-h6 ts-padding-left">{{item.mobile}}</text>
							</view>
							<view style="justify-content: center; align-items: center;">
								<ts-badge :text="item.type" type="error"></ts-badge>
							</view>
						</view>
					</view>
					<view class="ts-section-body">
						<view class="ts-row ts-h2 ts-text-bold ts-ellipsis">
							{{item.title}}
						</view>
						<view class="ts-row ts-padding-top" style="flex-wrap: wrap;">
							<view class="ts-row ts-padding-right ts-padding-bottom" v-for="(img,idx) in item.images" :key="idx" style="width: 150upx; height: 150upx;"
							 @tap="previewImage(item.images)">
								<image :src="img" style="width: 100%; height: 100%;"></image>
							</view>
						</view>
						<view class="ts-row ts-ellipsis-3" style="flex-wrap: wrap;">
							{{item.description}}
						</view>
						<ts-line></ts-line>
						<view class="ts-row">
							<view>地址：</view>
							<view>{{item.address}}</view>
						</view>
						<view class="ts-row">
							<view>时间：</view>
							<view>{{item.create_time}}</view>
						</view>

					</view>
				</view>
			</navigator>
			<ts-gap></ts-gap>
		</view>

		<ts-load-more :loadingType="loadingType"></ts-load-more>
		<ts-gap></ts-gap>

		<ts-fab :pattern="pattern" :content="content" horizontal="left" vertical="bottom" direction="horizontal" @trigger="trigger"
		 ref="fab"></ts-fab>

	</view>
</template>

<script>
	import * as api from "@/common/api/lost"

	export default {

		data() {
			return {
				currentTab: 0,
				tabs: ['全部', '丢失', '捡到'],
				searchResult: [],
				type: '全部',
				keywords: '',

				page: 0,
				loadingType: 0,

				//FAB属性
				pattern: {
					color: '#7A7E83',
					backgroundColor: '#fff',
					selectedColor: '#007AFF',
					buttonColor: '#007AFF'
				},
				content: [{
						iconPath: '/static/images/component.png',
						selectedIconPath: '/static/images/componentHL.png',
						text: '发布',
						active: false
					},
					// {
					// 	iconPath: '/static/images/api.png',
					// 	selectedIconPath: '/static/images/apiHL.png',
					// 	text: '我的',
					// 	active: false
					// },
				]
			}
		},
		async onReachBottom() {
			await this.loadMoreSearcheResult();
		},

		async onLoad() {
			await this.loadMoreSearcheResult();
		},
		methods: {
			previewImage(imageList) {
				//预览图片
				uni.previewImage({
					urls: imageList
				});
			},

			trigger(e) {
				console.log(e);			
				
				this.$refs.fab.close(); //关闭工具条
				// this.content[e.index].active = !e.item.active;
				if (!this.content[e.index].active) {
					if (e.index === 0) {
						uni.navigateTo({
							url: '/pages/app/lost/publish/index'
						})
					} else if (e.index === 1) {
						uni.switchTab({
							url: '/pages/tabbar/my/index'
						})
					}
				}
				
				
			},

			async onSearch(keywords) {
				this.keywords = keywords;
				await this.doSearch();
			},
			async doSearch() {
				this.page = 0;
				this.loadingType = 0;
				this.searchResult = [];

				let types = ['', '丢失', '捡到'];
				this.type = types[this.currentTab];

				await this.loadMoreSearcheResult();
			},
			async loadMoreSearcheResult() {
				//上拉的状态：0-loading前；1-loading中；2-没有更多了
				if (this.loadingType !== 0) {
					return;
				}
				this.loadingType = 1;
				this.page = this.page + 1;

				let res = await api.event.getList({
					page: this.page,
					key: this.keywords,
					type: this.type === "全部" ? '' : this.type,
					pageSize: 10,
				});

				if (res.errno === 0) {
					const data = res.data;
					if (data && data.data) {
						// console.log(data);
						this.searchResult = this.searchResult.concat(data.data);
					}
					if (data.totalPages === data.currentPage) {
						this.loadingType = 2; //2-没有更多了
					} else {
						this.loadingType = 0; //开启新一轮加载
					}
				} else {
					console.log(res.errmsg);
				}

			},

			async onClickItem(index) {
				if (this.currentTab !== index) {
					this.currentTab = index;
					await this.doSearch();
				}
			}
		}
	}
</script>

<style>
</style>
