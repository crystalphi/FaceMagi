<template>
	<view class="ts-column ts-flex-item ts-padding">
		<view>
			带删除，带添加，primary背景色
		</view>
		<ts-tags v-model="tabData" type="error" :enable-del="showDel" :enable-add="showAdd" size="normal" :mark='false'
		 :inverted='true' :circle="true" @add='addTag' @delete="deleteTag"></ts-tags>
		<view :key="index" v-for="(tag,index) in tabData">
			{{index}}. {{tag}}
		</view>
	</view>
</template>

<script>
	import tsTags from '@/components/teaset/components/ts-tag/ts-tags.vue'
	export default {
		components: {
			tsTags
		},
		data() {
			return {
				tabData: ['建筑', '动漫', '艺术'],
				// tabData: "计算机,体育",
				showDel: true,
				showAdd: true
			}
		},
		methods: {
			clickTag: function(e) {
				console.log(e)
			},
			deleteTag: function(e) {
				console.log(e)
			},
			addTag: function(e) {
				console.log(e)
				
				console.log(this.tabData)
			}
		}
	}
</script>

<style>
</style>
