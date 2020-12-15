<template>
	<view class="ts-drawer" :class="{'ts-drawer-visible':visible,'ts-drawer-right':rightMode}">
		<view v-if="showMask" class="ts-drawer-mask" @tap="close"></view>
		<view class="ts-drawer-content">
			<view style="display: flex; flex-direction: row; flex: 1; ; height: 100%;" >	
			<slot></slot>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		props: {
			/**
			 * 显示状态
			 */
			visible: {
				type: Boolean,
				default: false
			},
			/**
			 * 显示模式（左、右），只在初始化生效
			 */
			mode: String,
			/**
			 * 蒙层显示状态
			 */
			mask: {
				type: [Boolean, String],
				default: true
			}
		},
		data() {
			return {
				rightMode: false
			}
		},
		computed: {
			showMask() {
				return String(this.mask) === 'true'
			},
			heightPx(){
				let windowHeight = uni.getSystemInfoSync().windowHeight;
				return windowHeight;
			}
		},
		created() {
			this.rightMode = this.mode === 'right'
		},
		methods: {
			close() {
				this.$emit('close')
			}
		}
	}
</script>

<style scoped>
	.ts-drawer {
		display: block;
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		overflow: hidden;
		visibility: hidden;
		z-index: 99;
	}

	.ts-drawer>.ts-drawer-mask {
		display: block;
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.4);
	}

	.ts-drawer>.ts-drawer-content {
		display: block;
		position: absolute;
		top: 0;
		left: 0;
		width: 61.8%;
		height: 100%;
		background: #FFFFFF;
		transition: all 0.3s ease-out;
		transform: translatex(-100%);
	}

	.ts-drawer.ts-drawer-right>.ts-drawer-content {
		left: auto;
		right: 0;
		transform: translatex(100%);
	}

	.ts-drawer.ts-drawer-visible {
		visibility: visible;
	}

	.ts-drawer.ts-drawer-visible>.ts-drawer-mask {
		display: block;
	}

	.ts-drawer.ts-drawer-visible>.ts-drawer-content {
		transform: translatex(0);
	}
</style>
