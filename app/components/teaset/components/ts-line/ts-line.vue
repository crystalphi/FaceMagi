<template>
	<view class="ts-line-wraper">
		<view class="ts-line"></view>
	</view>
</template>

<script>
	export default {
		name: 'ts-line',
	}
</script>

<style lang="scss">
  @import '../../variables.scss';
  
	.ts-line-wraper{
		display: flex;
		width: 100%;
		flex-direction: row;
		padding-top: $ts-padding;
		padding-bottom: $ts-padding;
	}
	.ts-line {
		position: relative;
		width: 100%;
		display: flex;
		flex-direction: row;		
		height: 1upx;
	}

	.ts-line:before {
		position: absolute;
		z-index: 10;
		right: 0;
		top: 0;
		left: 0;
		height: 1upx;
		content: '';
		-webkit-transform: scaleY(.5);
		transform: scaleY(.5);   
    background-color: $uni-border-color
	}
</style>
