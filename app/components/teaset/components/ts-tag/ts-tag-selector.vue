<template>
	<view v-if="tags" class="ts-tag-selector-row">
		<block v-for="(tag, index) in tags" :key="index">
			<view class="ts-tag-selector-tag">
				<ts-tag :text="tag" :size="size" :circle="circle" :type="type" :inverted="!(selected[index])" @click="setInverted(index)"></ts-tag>
			</view>
		</block>
	</view>
</template>

<script>
	export default {
		name: 'ts-tag-selector',
		props: {
			defaultIndex: {
				type: [Array, Number],
				default () {
					return 0;
				}
			},
			tags: {
				type: Array,
				default () {
					return [];
				}
			},
			multiple: { //允许多选
				type: Boolean,
				default: false
			},
			type: { //标签类型default、primary、success、warning、danger、royal
				type: String,
				default: 'default'
			},
			size: { //标签大小 normal, small
				type: String,
				default: 'normal'
			},
			circle: { //是否为圆角
				type: [String, Boolean],
				defalut: false
			}
		},
		data() {
			return {
				selected: [],
			}
		},
		mounted() {
			this.selected = [];
			for (let i = 0; i < this.tags.length; i++) {
				this.selected.push(false);
			}

			const val = this.defaultIndex;
			//设置默认值
			if (Array.isArray(val)) {
				//多选
				for (let i = 0; i < val.length; i++) {
					const idx = val[i];
					this.$set(this.selected, idx, true)
				}
			} else {
				//单选
				this.$set(this.selected, val, true)
			}

			//       console.log('mounted:');
			//       console.log(JSON.stringify(this.selected))
		},
		methods: {

			setInverted(index) {

				const v = !this.selected[index];
				if (this.multiple) {
					this.$set(this.selected, index, v); //

					let selectedIndex = [];
					for (let i = 0; i < this.selected.length; i++) {
						if (this.selected[i]) {
							selectedIndex.push(i);
						}
					}

					this.$emit('change', {
						multiple: this.multiple,
						tags: this.tags,
						selected: this.selected,
						selectedIndex: selectedIndex,
					})
				} else {
					let selectedIndex = index;

					//不允许多选，清除所有选项，只设置一个值
					if (this.selected[index] === false) {
						for (let i = 0; i < this.tags.length; i++) {
							if (this.selected[i] === true) {
								this.$set(this.selected, i, false);
							}
						}
						this.$set(this.selected, index, v);
					} else {
						return; //没有改变，不触发事件
					}

					this.$emit('change', {
						multiple: this.multiple,
						tags: this.tags, //标签
						selected: this.selected, //全部索引的选中状态
						selectedIndex: selectedIndex, //当前选中的索引
					})
				}

			},
		}
	}
</script>


<style>
	.ts-tag-selector-row {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
	}

	.ts-tag-selector-tag {
		display: flex;
		flex-direction: row;
		padding-top: 10upx;
		padding-right: 10upx;
	}
</style>
