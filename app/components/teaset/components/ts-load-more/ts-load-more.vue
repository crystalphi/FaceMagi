<template>
	<view class="ts-load-more" @tap="handleTap">
		<view class="ts-loading-img" v-show="loadingType === 1 && showImage">
			<view class="ts-load1">
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
			</view>
			<view class="ts-load2">
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
			</view>
			<view class="ts-load3">
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
				<view :style="{background:color}"></view>
			</view>
		</view>
		<text class="ts-loading-text" :style="{color:color}">{{loadingType === 0 ? contentText.contentdown : (loadingType === 1 ? contentText.contentrefresh : contentText.contentnomore)}}</text>
	</view>
</template>

<script>
	export default {
		name: "ts-load-more",
		props: {
			loadingType: {
				//上拉的状态：0-loading前；1-loading中；2-没有更多了
				type: Number,
				default: 0
			},
			showImage: {
				type: Boolean,
				default: true
			},
			color: {
				type: String,
				default: "#777777"
			},
			contentText: {
				type: Object,
				default () {
					return {
						contentdown: "上拉显示更多",
						contentrefresh: "正在加载...",
						contentnomore: "没有更多数据了"
					}
				}
			}
		},
		data() {
			return {}
		},
    methods:{
      handleTap(e){
        if (this.loadingType ===0){
          this.$emit('tap')          
        }
      }
    }
	}
</script>

<style>
	.ts-load-more {
		display: flex;
		flex-direction: row;
		height: 80upx;
		align-items: center;
		justify-content: center;
	}

	.ts-loading-img {
		height: 24px;
		width: 24px;
		margin-right: 10px;
	}

	.ts-loading-text {
		font-size: 15px;
		color: #777777;
	}

	.ts-loading-img>view {
		position: absolute;
	}

	.ts-load1,
	.ts-load2,
	.ts-load3 {
		height: 24px;
		width: 24px;
	}

	.ts-load2 {
		transform: rotate(30deg);
	}

	.ts-load3 {
		transform: rotate(60deg);
	}

	.ts-loading-img>view view {
		width: 6px;
		height: 2px;
		border-top-left-radius: 1px;
		border-bottom-left-radius: 1px;
		background: #777;
		position: absolute;
		opacity: 0.2;
		transform-origin: 50%;
		-webkit-animation: load 1.56s ease infinite;
	}

	.ts-loading-img>view view:nth-child(1) {
		transform: rotate(90deg);
		top: 2px;
		left: 9px;
	}

	.ts-loading-img>view view:nth-child(2) {
		-webkit-transform: rotate(180deg);
		top: 11px;
		right: 0px;
	}

	.ts-loading-img>view view:nth-child(3) {
		transform: rotate(270deg);
		bottom: 2px;
		left: 9px;
	}

	.ts-loading-img>view view:nth-child(4) {
		top: 11px;
		left: 0px;
	}

	.ts-load1 view:nth-child(1) {
		animation-delay: 0s;
	}

	.ts-load2 view:nth-child(1) {
		animation-delay: 0.13s;
	}

	.ts-load3 view:nth-child(1) {
		animation-delay: 0.26s;
	}

	.ts-load1 view:nth-child(2) {
		animation-delay: 0.39s;
	}

	.ts-load2 view:nth-child(2) {
		animation-delay: 0.52s;
	}

	.ts-load3 view:nth-child(2) {
		animation-delay: 0.65s;
	}

	.ts-load1 view:nth-child(3) {
		animation-delay: 0.78s;
	}

	.ts-load2 view:nth-child(3) {
		animation-delay: 0.91s;
	}

	.ts-load3 view:nth-child(3) {
		animation-delay: 1.04s;
	}

	.ts-load1 view:nth-child(4) {
		animation-delay: 1.17s;
	}

	.ts-load2 view:nth-child(4) {
		animation-delay: 1.30s;
	}

	.ts-load3 view:nth-child(4) {
		animation-delay: 1.43s;
	}

	@-webkit-keyframes load {
		0% {
			opacity: 1;
		}

		100% {
			opacity: 0.2;
		}
	}
</style>
