<template>
	<view class="feedback-star-view">
		<text class="feedback-star" v-for="(value,key) in stars" :key="key" :style="key < selectedScore ? 'color:'+ activeColor: ''"
		 @tap="chooseStar(value)"></text>
	</view>
</template>

<script>
	export default {
		props: {
			score: {
				type: Number,
				default: 1
			},
			stars: {
				type: Array,
				default () {
					return [1, 2, 3, 4, 5]
				}
			},

			activeColor: {
				type: String,
				default: '#FFB400'
			}
		},
		data() {
			return {
				selectedScore: 0,
			}
		},
		mounted() {
			this.selectedScore = this.score;
		},
		methods: {
			chooseStar(e) { //点击评星
				this.selectedScore = e;
				this.$emit('change', this.selectedScore)
			},
		}

	}
</script>

<style>
	.feedback-star {
		font-family: uniicons;
		font-size: 40upx;
		margin-left: 6upx;
	}

	.feedback-star-view {
		margin-left: 20upx;
	}

	.feedback-star:after {
		content: '\e408';
	}

	.feedback-star.active {
		color: #FFB400;
	}

	.feedback-star.active:after {
		content: '\e438';
	}
</style>
