<template>
	<view class="ts-search-wraper">
		<view class="header">
			<block v-if="readonly=== true || readonly=== 'true'">
				<view class="input-view" @tap="handleTap" hover-class="navigator-hover">
					<ts-icon type="search" color="#666666" size="22"></ts-icon>
					<input class="input" type="text" :placeholder="placeholder" disabled />
				</view>
			</block>
			<block v-else>
				<view class="ts-row ts-padding-right" v-if="filterButton" @tap="handleFilter">
					<ts-icon type="bars" color="#666666" size="50"></ts-icon>
				</view>
				<view class="input-view">
					<ts-icon type="search" color="#666666" size="30" v-if="!filterButton"></ts-icon>
					<input class="input" type="text" :value="keywords" @input="handleInput" :placeholder="placeholder" />
				</view>
				<view class="ts-padding-left">
					<button size="mini" @tap="handleSearch">搜索</button>
				</view>
			</block>
		</view>
	</view>
</template>

<script>
	/**
	 * 
	 * 使用v-model后实际代码，根据组件的model属性来生成
	 * 使用方法
	 * <ts-search-bar v-model="keywords" @search="search"></ts-search-bar>
	 * <ts-search-bar :readonly="true" @tap="gotoSearchPage"></ts-search-bar>
	 */

	import tsIcon from '../ts-icon/ts-icon.vue';
	export default {
		name: 'ts-search-bar',
		components: {
			tsIcon,
		},
		//自定义prop名字，事件名字，使用v-model会自动修改生成的代码
		model: {
			prop: 'keywords',
			event: 'change'
		},
		props: {
			readonly: {
				type: [Boolean, String],
				default: false,
			},
			keywords: {
				type: String,
				default: ""
			},
			placeholder: {
				type: String,
				default: '检索关键字'
			},
			showFilterButton: {
				type: [Boolean, String],
				default: false,
			},
		},
		data() {
			return {
				keywords_: '',
			}
		},
		computed: {
			filterButton() {
				return (this.showFilterButton === "true" || this.showFilterButton === true)
			}
		},
		mounted() {
			this.keywords_ = this.keywords;
		},
		methods: {
			handleInput(e) {
				if (this.readonly === true || this.readonly === 'true') {} else {
					this.keywords_ = e.target.value;
					this.$emit('change', e.target.value)
				}
			},
			handleSearch(e) {
				if (this.readonly === true || this.readonly === 'true') {} else {
					this.$emit('search', this.keywords_)
				}
			},
			//用于构造搜索框占位符，点击跳转到新的搜索页面
			handleTap() {
				if (this.readonly === true || this.readonly === 'true') {
					this.$emit('tap');
				}
			},
			handleFilter(){
				if (this.filterButton){
					this.$emit('filter');
				}
			}
		},
	}
</script>

<style>
	.ts-search-wraper {
		display: flex;
		flex-direction: row;
		width: 100%;
	}

	.header {
		display: flex;
		flex-direction: row;
		padding: 10upx 10upx;
		align-items: center;
		width: 100%;
	}

	.input-view {
		display: flex;
		align-items: center;
		flex-direction: row;
		background-color: #e7e7e7;
		height: 50upx;
		border-radius: 15upx;
		padding: 0 10upx;
		flex: 1;
	}

	.input {
		flex: 1;
		padding: 0 5upx;
		height: 50upx;
		line-height: 50upx;
		font-size: 30upx;
	}
</style>
