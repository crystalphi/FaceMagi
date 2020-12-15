<template>
	<view class="ts-timeline-rows">
		<view class="ts-timeline-time">
      <slot name="time"></slot>
		</view>
		<view class="ts-timeline-tips">
			<view class="ts-timeline-circular">
        <slot name="icon"></slot>			
			</view>
		</view>
		<view class="ts-timeline-content">
			<slot name="content"></slot>
		</view>
		<view v-if="!isLastItem" class="ts-timeline-line"></view>
	</view>
</template>

<script>
	export default {
		name: 'ts-timeline-item',
		props: {
			isLastItem: {
				type: Boolean,
				default: false
			}
		}
	}
</script>

<style>
	/* 时间轴 */
/* 	.ts-timeline {
		display: flex;
		flex-direction: column;
		flex: 1;
		width: 100%;
	} */

	.ts-timeline-rows {
		display: flex;
		flex-direction: row;
    padding: 20upx;
    flex-wrap: nowrap;
    justify-content: space-between;
    position: relative;
	}

	.ts-timeline-time {
		display: flex;
		flex-direction: column;
		width: 130upx;
		flex-shrink: 0;
		overflow: hidden;
	}

	.ts-timeline-time view {
		font-size: 22upx;
		color: #ccc;
		justify-content: flex-end;
		overflow: hidden;
		line-height: 1.5em;
	}

	.ts-timeline-time view:last-child {
		font-size: 32upx;
		color: #46A4DA;
	}

	.ts-timeline-tips {
		width: 70upx;
		height: 100%;
		margin: 0 15upx;
		flex-shrink: 0;
		position: relative;
	}

	.ts-timeline-circular {
		width: 50upx;
		height: 50upx;
		border: 10rpx solid #AFDCF8;
		border-radius: 100%;
		line-height: 50upx;
		justify-content: center;
		background: #46A4DA;
		color: #FFF;
		position: absolute;
		left: 0;
		top: 0;
		z-index: 2
	}

	.ts-timeline-circular image {
		border-radius: 100%;
		font-size: 0;
		width: 100%;
	}

	.ts-timeline-content {
		display: flex;
		flex-direction: column;
		flex: 1;
		background-color: #AFDCF8;
		padding: 18upx;
		border-radius: 12upx;
		border: #46A4DA solid 1px;
	}

	.ts-timeline-line {
		width: 8upx;
		height: 100%;
		background: #AFDCF8;
		position: absolute;
		z-index: 1;
		left: 195upx;
		top: 30upx;
	}
</style>
