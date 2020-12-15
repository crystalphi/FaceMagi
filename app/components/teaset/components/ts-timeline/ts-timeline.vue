<template>
	<view class="ts-timeline">
		<slot></slot>
	</view>
</template>

<script>
	export default {
		name: 'ts-timeline',

	}
</script>

<style>
	/* 时间轴 */
	.ts-timeline {
		display: flex;
		flex-direction: column;
		flex: 1;
	}
</style>
