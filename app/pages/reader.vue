<template>
	<view class="marked-document-conent">
		<wxParse :content="article" @preview="preview" @navigate="navigate" />
	</view>
</template>

<script>
	import marked from 'components/marked/index.js'
	import wxParse from 'components/mpvue-wxparse/src/wxParse.vue'
	import service from 'services/document.js'

	export default {
		components: {
			wxParse
		},
		data(){return {
			article: " ",
		}},
		methods: {
			preview(src, e) {
				console.log("src: " + src);
			},
			navigate(href, e) {
				console.log("href: " + href);
				//#ifdef APP-PLUS
				plus.runtime.openURL(href);
				//#endif

				//#ifdef MP-WEIXIN
				uni.setClipboardData({
					data: href
				})
				//#endif
			}
		},
		onLoad: async function(e) {

			// 			var rendererMD = new marked.Renderer();
			// 			marked.setOptions({
			// 				renderer: rendererMD,
			// 				// 				gfm: true,
			// 				// 				tables: true,
			// 				// 				breaks: false,
			// 				// 				pedantic: false,
			// 				// 				sanitize: true,
			// 				// 				smartLists: true,
			// 				// 				smartypants: false
			// 			}); //基本设置
			// console.log(marked('I am <template> </template> using __markdown__.'));
			const documentUrl = e.document;
			uni.setNavigationBarTitle({
				title: e.title || '文档阅读器'
			})
			let mdcontend = await service.getMarkdownFileContent(documentUrl);
			let htmlString = marked(mdcontend);
			//&lt; &gt;会被过滤掉，换成全角符号暂时解决先
			// htmlString = htmlString.replace(/(&lt;)/g, "<\r"); //破坏原始结构按时解决显示问题
			this.article = htmlString
			// console.log(this.article)
		},
	}
</script>

<style>
	@import url("../components/mpvue-wxparse/src/wxParse.css");

	page view {
		display: block;
	}

	.marked-document-conent {
		padding-left: 20upx;
		padding-right: 20upx;
		word-break: break-word;
		overflow: auto;
		display: flex;
		flex: 1;
		flex-direction: column;
	}
</style>
