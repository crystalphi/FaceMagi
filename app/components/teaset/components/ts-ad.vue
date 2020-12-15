<template>
	<view class="ts-ad-wraper" v-if="!bannerHidden">
		<view class="ts-ad">
			<view class="ts-ad-content" @tap="handleTap">
				<slot></slot>
			</view>
			<view class="ts-ad-close-button" @tap="handleClose">
				<image :src="closeButtonImage" mode="widthFix"></image>
			</view>
		</view>
	</view>

</template>

<script>
	export default {
		name: 'ts-ad',
		data() {
			return {
				bannerHidden: false,
			}
		},
		model: {
			prop: 'hidden',
			event: 'close'
		},
		props: {
			hidden: {
				type: [Boolean, String],
				default: false
			},
			closeButtonImage: {
				type: String,
				default: 'data:image/png;base64,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'
			}
		},
		watch: {
			bannerHidden(val) {
				this.$emit('close', val);
			},
			hidden(val) {
				console.log(val)
				this.updateValue(val);
			}
		},
		mounted() {
			this.updateValue(this.hidden);
		},
		methods: {
			updateValue(val) {
				this.bannerHidden = !!val;
			},
			handleClose() {
				this.bannerHidden = true;
			},
			handleTap() {
				console.log('Tap')
				this.$emit('tap');
			}
		}
	}
</script>

<style>
	.ts-ad-wraper {
		display: flex;
		flex-direction: column;
		flex: 1;
	}

	.ts-ad {
		background: #DEF0F0;
		display: block;
		position: relative;
		width: 100%;
	}

	.ts-ad-content {
		display: block;
		width: 100%;
	}

	.ts-ad-close-button {
		display: block;
		position: absolute;
		right: 0;
		top: 0;
	}

	.ts-ad-close-button image {
		width: 60px;
	}
</style>
