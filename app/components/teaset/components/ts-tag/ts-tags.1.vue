<template>
	<view class="tagController">
		<view class="tagContainer">
			<view class="tagItem" :class="tagAttributes" :key="index" v-for="(tagText,index) in tagList">
				<text @tap="tapTag" :data-text="tagText">{{tagText}}</text>
				<text v-if="isShowDelIcon" class="tagDelIcon" @tap="delTag" :data-text="tagText">x</text>
			</view>
			<view class="tagInput" v-if="isShowAdd">
				<view class="tagInputWraper">
					<input type="text" v-model="tagString" placeholder="输入新的标签,逗号间隔" @blur="createTags" />
				</view>
				<!-- <ts-button :type="bgColorType" @tap="createTags" :height="48">添加</ts-button> -->
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		name: 'ts-tags',
		model: {
			prop: 'value',
			event: 'input'
		},
		props: ['enableDel', 'bgColorType', 'value', 'enableAdd', 'size'],
		data() {
			return {
				tagString: '',
				tagList: this.value || [],
				isShowDelIcon: this.enableDel || false,
				isShowAdd: this.enableAdd || false,
			}
		},
		watch: {
			value(newValue, oldValue) {
				this.tagList = newValue || [];
			}
		},
		computed: {
			tagBgColor: function() {
				if (this.bgColorType === null) {
					return 'tagBgDefault'
				} else if (this.bgColorType === 'primary') {
					return 'tagBgPrimary'
				} else if (this.bgColorType === 'success') {
					return 'tagBgSuccess'
				} else if (this.bgColorType === 'warn') {
					return 'tagBgWarning'
				} else if (this.bgColorType === 'error') {
					return 'tagBgError'
				} else {
					return 'tagBgDefault'
				}
			},
			tagSize: function() {
				let size = ['tagItem'];
				if (this.size == 'mini') {
					size.push('tagItemMini')
				}
				return size;
			},

			tagAttributes: function() {
				return [this.tagBgColor, this.tagSize]
			}

		},
		methods: {
			createTags: function() {
				let tempTagArr = []
				if (this.tagString.length > 0) {
					let newTagList = this.tagString.split(/,|，/)
					for (let i = 0; i < newTagList.length; i++) {
						let newTag = newTagList[i].trim()

						if (newTag !== '' && this.tagList.indexOf(newTag) < 0) {
							tempTagArr.push(newTag)
						}
					}
				}
				this.tagString = ''
				this.tagList.splice(this.tagList.length, 0, ...tempTagArr)
				this.$emit('add', {
					currentTag: tempTagArr,
					allTags: this.tagList
				})

				console.log(this.value);

				this.$emit('input', this.tagList)
			},
			delTag: function(e) {
				let delTagText = e.currentTarget.dataset.text
				let delTagIndex = this.tagList.indexOf(delTagText)
				this.tagList.splice(delTagIndex, 1)
				this.$emit("delete", {
					currentTag: delTagText,
					allTags: this.tagList
				})
				this.$emit('input', this.tagList)
			},
			tapTag: function(e) {
				let selTagText = e.currentTarget.dataset.text
				this.$emit("click", selTagText)
			}
		}
	}
</script>

<style scoped lang="scss">
	.tagController {
		padding: 10upx;
		display: flex;
		flex-direction: column;
	}

	.tagContainer {
		display: flex;
		flex-wrap: wrap;
		justify-content: flex-start;
	}

	.tagItem {
		padding: 10upx 20upx;
		margin: 10upx;
		border-radius: 40upx;
		color: white;
		font-size: $uni-font-size-base;
	}

	.tagItemMini {
		padding: 5upx 10upx;
		margin: 5upx;
		border-radius: 10upx;
		color: white;
		font-size: $uni-font-size-sm;
	}

	.tagBgDefault {
		background-color: $uni-bg-color-grey;
		color: black;
	}

	.tagBgPrimary {
		background-color: $uni-color-primary;
	}

	.tagBgSuccess {
		background-color: $uni-color-success;
	}

	.tagBgWarning {
		background-color: $uni-color-warning;
	}

	.tagBgError {
		background-color: $uni-color-error;
	}

	.tagDelIcon {
		padding-left: 20upx;
	}

	.tagInput {
		padding: 5upx;
		display: flex;
		flex-direction: row;
		// border: solid 1px;
		height: 24upx;
		// justify-content: center;
		
	}

	.tagInputWraper {
		display: flex;
		flex: 1;
		flex-direction: row;
		padding-right: 10upx;
	}

	.tagInputWraper input {
		width: 300upx;
		display: inline-flex;
		border: solid 1px;
	}

	.tagInput button {
		padding: 5upx 10upx;
	}
</style>
