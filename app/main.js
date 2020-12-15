import Vue from 'vue';
import VueI18n from 'vue-i18n';
import App from '@/App';
import store from '@/store/index';
//import request from '@/common/request';
import {
	logger,
	dump
} from '@/common/logger'

//常用组件，全局注册
import tsBadge from "@/components/teaset/components/ts-badge/ts-badge.vue";
import tsButton from "@/components/teaset/components/ts-button/ts-button.vue";
import tsBanner from "@/components/teaset/components/ts-banner/ts-banner.vue";
//import tsCityPicker from '@/components/teaset/components/ts-city-picker.vue';
//import tsDrawer from "@/components/teaset/components/ts-drawer.vue";
import tsFab from "@/components/teaset/components/ts-fab/ts-fab.vue";
//import tsFeedbackStar from '@/components/teaset/components/ts-feedback-star.vue';
import tsGap from '@/components/teaset/components/ts-gap/ts-gap.vue';

import tsIcon from "@/components/teaset/components/ts-icon/ts-icon.vue";
import tsLeftCategory from '@/components/teaset/components/ts-left-category.vue';
import tsList from "@/components/teaset/components/ts-list/ts-list.vue";
import tsListItem from "@/components/teaset/components/ts-list/ts-list-item.vue";
import tsLoadMore from "@/components/teaset/components/ts-load-more/ts-load-more.vue";
import tsLine from '@/components/teaset/components/ts-line/ts-line.vue';
import tsNoticeBar from "@/components/teaset/components/ts-notice-bar/ts-notice-bar.vue";
import tsPopup from "@/components/teaset/components/ts-popup/ts-popup.vue";
//import tsPopupAd from "@/components/teaset/components/ts-popup/ts-popup-ad.vue";

import tsSearchBar from "@/components/teaset/components/ts-search-bar/ts-search-bar.vue";
import tsSegmentedControl from "@/components/teaset/components/ts-segmented-control/ts-segmented-control.vue";
import tsSection from '@/components/teaset/components/ts-section/ts-section.vue'
import tsSectionTitle from '@/components/teaset/components/ts-section/ts-section-title.vue'
import tsSectionBody from '@/components/teaset/components/ts-section/ts-section-body.vue'
import tsSectionFooter from '@/components/teaset/components/ts-section/ts-section-footer.vue'
//import tsSwipeAction from "@/components/teaset/components/ts-swipe-action/ts-swipe-action.vue";

import tsTag from "@/components/teaset/components/ts-tag/ts-tag.vue";
import tsTags from "@/components/teaset/components/ts-tag/ts-tags.vue";
import tsTagSelector from "@/components/teaset/components/ts-tag/ts-tag-selector.vue";
//import tsSteps from "@/components/teaset/components/ts-steps/ts-steps.vue";
//import tsTimeline from '@/components/teaset/components/ts-timeline/ts-timeline.vue';
//import tsTimelineItem from '@/components/teaset/components/ts-timeline/ts-timeline-item.vue';

import pageHead from '@/components/page-head.vue';
import pageFoot from '@/components/page-foot.vue';
import uLink from '@/components/uLink.vue';
import cuCustom from '@/colorui/components/cu-custom.vue';

//注册全局组件
Vue.component('ts-badge', tsBadge);
Vue.component('ts-banner', tsBanner);
Vue.component('ts-button', tsButton);
Vue.component('ts-fab', tsFab);
Vue.component('ts-gap', tsGap);
Vue.component('ts-icon', tsIcon);
Vue.component('ts-line', tsLine);
Vue.component('ts-load-more', tsLoadMore);
Vue.component('ts-list', tsList);
Vue.component('ts-list-item', tsListItem);
Vue.component('ts-notice-bar', tsNoticeBar);
Vue.component('ts-popup', tsPopup);
Vue.component('ts-search-bar', tsSearchBar);
Vue.component('ts-segmented-control', tsSegmentedControl);
Vue.component('ts-left-category', tsLeftCategory);
Vue.component('ts-section', tsSection);
Vue.component('ts-section-title', tsSectionTitle);
Vue.component('ts-section-body', tsSectionBody);
Vue.component('ts-section-footer', tsSectionFooter);
Vue.component('ts-tag', tsTag);
Vue.component('ts-tags', tsTags);
Vue.component('ts-tag-selector', tsTagSelector);

Vue.component('page-head', pageHead);
Vue.component('page-foot', pageFoot);
Vue.component('uLink', uLink);
Vue.component('cu-custom', cuCustom);

Vue.config.productionTip = false;
//挂载全局对象
Vue.prototype.$store = store;
//Vue.prototype.$request = request;
Vue.prototype.$logger = logger; //日志记录器

logger.log('App state:', dump(store.state));

/*
//第三方登录
//#ifdef APP-PLUS
uni.getProvider({
	service: 'share',
	success: (e) => {
		console.log('--> success', JSON.stringify(e.provider));
		//logger.log(e.provider);
		let data = []
		for (let i = 0; i < e.provider.length; i++) {
			switch (e.provider[i]) {
				case 'weixin':
					data.push({
						name: '分享到微信好友',
						id: 'weixin',
						icon: 'weixin',
						type: 'WXSceneSession', //default value
						sort: 0
					})
					data.push({
						name: '分享到微信朋友圈',
						id: 'weixin',
						icon: 'wechat',
						type: 'WXSenceTimeline',
						sort: 1
					})
					break;
				case 'qq':
					data.push({
						name: '分享到QQ',
						id: 'qq',
						icon: 'qq',
						sort: 2
					})
					break;
				case 'sinaweibo':
					data.push({
						name: '分享到新浪微博',
						id: 'sinaweibo',
						icon: 'sinaweibo',
						sort: 3
					})
					break;
				default:
					break;
			}
		}
		Vue.prototype.$providerList = data.sort((x, y) => {
			return x.sort - y.sort
		});
		//微信登录
		if (~e.provider.indexOf('weixin')) {
			uni.login({
				provider: 'weixin',
				success: function(loginRes) {
					console.log('-------获取openid(unionid)-----');
					console.log(JSON.stringify(loginRes));
					//获取用户信息
					uni.getUserInfo({
						provider: 'weixin',
						success: function(infoRes) {
							console.log('-------获取微信用户所有-----');
							console.log(JSON.stringify(infoRes.userInfo));
						}
					});
				}
			});
		}
	},
	fail: (e) => {
		console.log('获取登录通道失败', e);
		//    uni.showModal({
		//      content: '获取登录通道失败',
		//      showCancel: false
		//    })
	}
});
//#endif
*/

//语言国际化
Vue.use(VueI18n);
Vue.config.productuinTip = false;

let system_info = uni.getStorageSync('system_info');
if (! system_info) {
	// 获取设备信息
	system_info = uni.getSystemInfoSync();
	uni.setStorageSync('system_info', system_info);
}

//语言检测及设置
//若增加支持其他语言，需添加到下述列表项以及增加对应 messages 字段定义
let sys_language = 'en_US';
// #ifdef APP-PLUS
console.log('--> plus.os.language: ' + plus.os.language); //zh-Hans-US
sys_language = plus.os.language;
// #endif
// #ifndef APP-PLUS
console.log('--> system_info.language: ' + system_info.language);
sys_language = system_info.language;
// #endif
sys_language = sys_language.replace(/-/g, '_');
console.log('--> sys_language: ' + sys_language);

//IDE 环境下”PC模式“预览为 'zh'；真机中文环境下为 'zh_Hans_US'
if (['zh', 'zh_CN', 'zh_Hans_US'].indexOf(sys_language) >= 0) {
	Vue.prototype.language = 'zh_CN';
} else if (['en_US'].indexOf(sys_language) >= 0) { //TODO 英文真机值待测试
	Vue.prototype.language = 'en_US';
} else { //其他语言暂不支持，暂设为英文
	//Vue.prototype.language = sys_language;
	Vue.prototype.language = 'en_US';
}
console.log('当前系统语言设置为: ' + Vue.prototype.language);
const i18n = new VueI18n({
	locale: Vue.prototype.language || 'en_US',  // 默认选择的语言
	messages: {
		'en_US': {
			index: {
				ok: 'OK',
				cancel: 'Cancel',
				confirm: 'Confirm',
				close: 'Close',
				Continue: 'Continue',
				apply: 'OK', //目前后端默认关闭了对连续编辑的支持，故此改为 OK，否则为 Apply
				back: 'Back',
				Return: 'Return',
				save: 'Save',
				notice: 'Notice',
				error: 'Error',
				photo: 'Photo',
				forward: 'Forward',
				face_makeup: 'FACE MAKEUP',
				face_creative: 'FACE CREATIVE',
				skin_tone: 'Skin Tone',
				face_demo: 'Demo Faces',
				face_photo: 'Face Photo From Camera',
				app_advert: 'Unlimited possibilities for photos',
				uploading: 'Uploading',
				editor: 'MAKEUP', //EDITOR
				art: 'ART',
				fun: 'TRY',
				settings: 'Settings',
				version: 'Version',
				comment_app: 'Evaluating it in App Store',
				share_app: 'Sharing this application',
				restore_paid: 'Restore purchase',
				privacy: 'Privacy Policy',
				terms: 'Terms of Service',
				invalid_image:'Invalid image',
				image_transmit: 'Image transmiting',
				image_too_small: 'Image too small, 432x540 px at least',
				image_too_large: 'Image too large, 3456x4320 px at most',
				image_saved: 'Image saved',
				image_save_failed: 'Image saving failed',
				network_error: 'Network error',
				please_try_later: 'Please try again later',
				app_start_notice: 'This application is suitable for processing pictures containing front faces. The pictures will be uploaded to the server for processing and will be kept as cache for up to 24 hours. \n\nWe promise never to store these pictures permanently or for any other purpose. To view the specific privacy terms, tap the "Settings" icon in the upper left corner.',
				api_processing: 'Processing ...',
				api_failed: 'API request failed',
				api_process_timeout: 'Process timeout',
				api_add_task_err: 'Task adding failed',
				api_query_task_err: 'Task quering failed',
				api_msg_cannot_process: 'Cannot process this picture',
				msg_no_save_permission: 'No permission to save',
				msg_ask_change_settings: 'Do you want to change the settings now?',
				msg_image_save_notice: 'Returning to the home page will result in the loss of currently unsaved pictures. Are you sure to continue?',
				msg_restore_original_notice: 'Restoring the original image will cause all current modifications to be lost. Are you sure to continue?',
				msg_vip_function_notice: 'This is a paid feature, you need to purchase PRO permission to use it. Are you sure to continue?',
				msg_get_confg_fail: 'get config failed',
				msg_check_network: 'Please check the network status.',
				msg_check_network_try_again: 'Processing failed. \nPlease use another photo or try again.',
				msg_paid_updating: 'IAP Updating ...',
				msg_paid_updated: 'Your purchase has been restored to this device.',
				msg_paid_valid: 'You have already made a purchase before, no need to make another purchase.',
				msg_purchase_success: 'Purchase success.',
				msg_purchase_failed: 'Purchase failed.',
				apple_login_request: 'Apply For Sign In',
				apple_login_notify: 'It will make the PRO features available to all supported iOS devices owned by you.',
				apple_login_fail: 'Sign in with Apple failed',
				subscription_title: 'PRO subscription',
				subscription_banner1: 'Access all advanced features',
				subscription_banner2: 'Transfer photos with cartoon or painting or print styles, different makeup styles, change skin or hair color and more',
				subscription_button_text1: 'Semi-Annually: $9.99',
				subscription_button_text2: 'Plan auto-renews semi-annually after 3-day trial',
				subscription_description: 'Payment will be charged to your iTunes Account at the confirmation of purchase. Subscription automatically renews unless it is canceled at least 24 hours before the end of the current period. Your account will be charged for renewal within 24 hours prior to the end of the current period. You can manage or cancel your subscriptions by going to your account settings on the App Store after purchase. Any unused portion of a free trial period will be forfeited when the user purchase a subscription to that publication, where applicable.',
				app_store_href: 'https://apps.apple.com/cn/app/facemagi/id1502256892'
			}
		},
		'zh_CN': {
			index: {
				ok: '确认',
				cancel: '取消',
				confirm: '确定',
				close: '关闭',
				Continue: '继续',
				apply: '保留', //目前后端默认关闭了连续编辑的支持，故改为“保留”，否则为“应用”
				back: '回退',
				Return: '返回',
				save: '保存',
				notice: '提示',
				error: '错误',
				photo: '照片',
				forward: '分享',
				face_makeup: '头像装扮',
				face_creative: '头像创意',
				skin_tone: '肤色调整',
				face_demo: '人脸示例',
				face_photo: '人脸照片',
				app_advert: '照片的无限种可能...',
				uploading: '正在上传...',
				editor: '美妆',
				art: '艺术',
				fun: '玩玩',
				settings: '设置',
				version: '版本',
				comment_app: '在 App Store 评价应用',
				share_app: '分享应用',
				restore_paid: '恢复购买',
				privacy: '隐私政策',
				terms: '使用条款',
				invalid_image:'无效的图片',
				image_transmit: '图片传送',
				image_too_small: '图片太小。最小为 432x540',
				image_too_large: '图片太大。最大为 3456x4320',
				image_saved: '图片已保存',
				image_save_failed: '图片保存失败',
				network_error: '网络错误',
				please_try_later: '请稍后再试',
				app_start_notice: '本应用适合对包含正面人脸的图片进行处理。图片将被上传到服务器上进行处理，处理完毕后将作为缓存保留最多24小时。\n\n我们承诺绝不永久存储这些图片，或做任何其他用途。查看具体隐私条款可点击左上角“设置”图标。',
				api_processing: '处理中...',
				api_failed: 'API 请求失败...',
				api_process_timeout: '处理超时',
				api_add_task_err: '新建任务失败',
				api_query_task_err: '查询任务失败',
				api_msg_cannot_process: '无法处理该图片',
				msg_no_save_permission: '没有存储权限',
				msg_ask_change_settings: '您想现在修改设置吗？',
				msg_image_save_notice: '返回首页将导致当前未保存的图片丢失。确定继续吗？',
				msg_restore_original_notice: '恢复原图将导致当前所有修改丢失。确定继续吗？',
				msg_vip_function_notice: '这是一个付费功能，需购买 VIP 权限才能使用。确定继续吗？',
				msg_get_confg_fail: '获取配置信息失败',
				msg_check_network: '请检查网络状态',
				msg_check_network_try_again: '处理失败。请更换为其他照片，或者再次尝试。',
				msg_paid_updating: '正在同步您的购买项……',
				msg_paid_updated: '您的购买已恢复到本设备上',
				msg_paid_valid: '您之前已有购买，无需再次购买',
				msg_purchase_success: '购买成功。',
				msg_purchase_failed: '购买失败。',
				apple_login_request: '申请通过 Apple 登录',
				apple_login_notify: '这会让 PRO 功能在您拥有的所有可支持 IOS 设备上生效。',
				apple_login_fail: '通过 Apple 登录失败',
				subscription_title: 'PRO 订阅',
				subscription_banner1: '访问所有高级特性',
				subscription_banner2: '使用卡通漫画、油画、版画等风格转换照片，不同的人脸妆容风格，更改人脸肤色或头发颜色等等',
				subscription_button_text1: '半年订阅价: $9.99',
				subscription_button_text2: '经过3天的试用后，计划每半年自动更新订阅一次',
				subscription_description: '购买确认后，付款将从您的iTunes帐户中扣除。除非在当前周期结束前至少24小时取消，否则订阅将自动续订。您的账户将在本期结束前24小时内进行续费。购买后，您可以通过在应用商店上转到您的帐户设置来管理或取消您的订阅。当用户购买该出版物的订阅时，免费试用期的任何未使用部分将被收回。',
				app_store_href: 'https://apps.apple.com/us/app/facemagi/id1502256892'
			}
		}
	}
});
Vue.prototype._i18n = i18n;

Vue.prototype.app_name = 'FaceMagi';
Vue.prototype.apple_user_id = null; //已登录用户信息
Vue.prototype.app_start_notice_viewed = false; //是否已展示 app 启动提示信息
Vue.prototype.demoFacesSaveDir = null;
Vue.prototype.demoFacesFileNames = {}; //序号、短文件名
Vue.prototype.IAPOrders = ['facemagi.vip.4weeks']; //IAP 内购产品ID

Vue.prototype.isLiteVersion = true; //是否 lite 版本（true 为免费有广告版本，否则为付费版本）
if (Vue.prototype.isLiteVersion) {
	Vue.prototype.app_name += ' Lite';
	Vue.prototype.app_start_notice_viewed = true;
}

App.mpType = 'app';
const app = new Vue({
	store,
	//request,
	...App
})
app.$mount();
