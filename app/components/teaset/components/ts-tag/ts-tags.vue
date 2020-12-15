<template>
	<view class="tagController">
		<view class="tagContainer">
			<view :class="computedClass" :key="index" v-for="(tagText,index) in tagList">
				<text @tap="tapTag" :data-text="tagText">{{tagText}}</text>
				<text v-if="isShowDelIcon" class="tagDelIcon" @tap="delTag" :data-text="tagText">x</text>
			</view>
			<view class="tagInput" v-if="isShowAdd">
				<input type="text" v-model="tagString" placeholder="新增标签(组)" @blur="createTags" :class="computedClass" />
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
		props: {
			enableDel: {
				type: [Boolean],
				defalut: false
			},
			enableAdd: {
				type: [Boolean],
				defalut: false
			},
			value: {
				type: [Array, String],
				defalut() {
					return []
				}
			},
			size: { //标签大小 normal, small, large
				type: String,
				default: 'small'
			},
			type: { //标签类型default、primary、success、warning、error
				type: String,
				default: 'default'
			},
			disabled: { //是否为禁用状态
				type: [String, Boolean],
				defalut: false
			},
			inverted: { //是否为空心
				type: [String, Boolean],
				defalut: false
			},
			circle: { //是否为圆角
				type: [String, Boolean],
				defalut: false
			},
			dashed: { //是否为虚线框
				type: [String, Boolean],
				defalut: false
			},
			mark: { //是否为标记样式
				type: [String, Boolean],
				defalut: false
			}
		},
		data() {
			return {
				tagString: '',
				tagList: (typeof(this.value) === 'string' ? this.value.split(',') : this.value) || [],
				isShowDelIcon: this.enableDel || false,
				isShowAdd: this.enableAdd || false,
			}
		},
		watch: {
			value(newValue, oldValue) {
				if (typeof(newValue) === 'string') {
					this.tagList = newValue.split(',')
				}
				this.tagList = newValue || [];
			}
		},
		computed: {
			computedClass() {
				let classArr = ['ts-tag'];

				if (this.disabled === true || this.disabled === 'true') {
					classArr.push('ts-tag--disabled');
				}
				if (this.inverted === true || this.inverted === 'true') {
					classArr.push('ts-tag--inverted');
				}
				if (this.circle === true || this.circle === 'true') {
					classArr.push('ts-tag--circle');
				}
				if (this.mark === true || this.mark === 'true') {
					classArr.push('ts-tag--mark');
				}

				if (this.dashed === true || this.dashed === 'true') {
					classArr.push('ts-tag--dashed');
				}

				classArr.push('ts-tag--' + this.size);
				classArr.push('ts-tag--' + this.type);
				// console.log(classArr);
				return classArr;
			},
		},
		methods: {
			createTags: function() {
				let tempTagArr = []
				if (this.tagString.length > 0) {
					let newTagList = this.tagString.split(/,|，|;|；/)
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

				// console.log(this.value);

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
	$tag-pd:0upx 10upx;
	$tag-small-pd:0upx 5upx;

	.tagController {
		padding: 10upx 0upx;
		display: flex;
		flex-direction: column;
	}

	.tagContainer {
		display: flex;
		flex-wrap: wrap;
		justify-content: flex-start;
	}

	.tagDelIcon {
		padding-left: 20upx;
	}

	.tagInput {}

	.tagInput input {
		width: 200upx;
	}

	@mixin tag-disabled {
		opacity: 0.5;
	}

	.ts-tag {
		box-sizing: border-box;

		justify-content: center;
		align-items: center;

		padding: $tag-pd;
		margin: 5upx;

		background-color: $uni-bg-color-grey;
		border: 1upx solid $uni-bg-color-grey;
		color: $uni-text-color;
		font-size: $uni-font-size-base;
		border-radius: $uni-border-radius-base;

font-weight: normal;

		&--circle {
			border-radius: 20upx;
		}

		&--mark {
			border-radius: 0 30upx 30upx 0
		}

		&--dashed {
			border: 1upx dashed;
		}

		&--disabled {
			@include tag-disabled;
		}

		&--normal {}

		&--small {
			padding: $tag-small-pd;
			font-size: $uni-font-size-sm;
		}

		&--large {
			padding: $tag-pd;
			font-size: $uni-font-size-lg;
		}

		&--default {}

		&--primary {
			color: $uni-text-color-inverse;
			background-color: $uni-color-primary;
			border: 1upx solid $uni-color-primary;

			&.ts-tag--inverted {
				color: $uni-color-primary;
				background-color: $uni-bg-color;
				border: 1upx solid $uni-color-primary;
			}

		}

		&--success {
			color: $uni-text-color-inverse;
			background-color: $uni-color-success;
			border: 1upx solid $uni-color-success;

			&.ts-tag--inverted {
				color: $uni-color-success;
				background-color: $uni-bg-color;
				border: 1px solid $uni-color-success;
			}

			&.ts-tag--dashed {
				border: 1upx dashed;
			}
		}

		&--warning {
			color: $uni-text-color-inverse;
			background-color: $uni-color-warning;
			border: 1upx solid $uni-color-warning;

			&.ts-tag--inverted {
				color: $uni-color-warning;
				background-color: $uni-bg-color;
				border: 1upx solid $uni-color-warning;
			}

			&.ts-tag--dashed {
				border: 1upx dashed;
			}
		}

		&--error {
			color: $uni-text-color-inverse;
			background-color: $uni-color-error;
			border: 1upx solid $uni-color-error;

			&.ts-tag--inverted {
				color: $uni-color-error;
				background-color: $uni-bg-color;
				border: 1upx solid $uni-color-error;
			}

			&.ts-tag--dashed {
				border: 1upx dashed;
			}
		}

		&--inverted {
			color: $uni-text-color;
			background-color: $uni-bg-color;
			border: 1upx solid $uni-bg-color-grey;
		}
	}
</style>
