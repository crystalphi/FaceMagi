import Vue from 'vue'
import Vuex from 'vuex'
import createLogger from 'vuex/dist/logger'
import token from './modules/token'
import user from './modules/user'
import cart from './modules/cart'
import * as api from '@/common/api'
import types from './types'
const debug = true;
const getters = {
	userType: state => {
		return state.userType;
	}
}
const state = {
	forcedLogin: false,
	hasLogin: uni.getStorageSync(types.USER_NAME) === '' ? false : true,
	// hasLogin:true,
	userType: 'student', //登陆用户类型(角色)，支持：guest|student|company|school
}
const mutations = {
	/**
	 * 记录登录状态
	 */
	login(state) {
		state.hasLogin = true;
	},
	/**
	 *  退出登录状态
	 */
	logout(state) {
		state.hasLogin = false;
		state.token.value = '';
		state.user.username = '';
	},
}
const actions = {

	//检查用户是否已经登陆，如果没有登陆跳转到登陆页面
	async checkLogin(context) {
		if (context.state.hasLogin) {
			// console.log('用户没有登陆')
			return true;

		} else {
			// console.log('跳转到登陆页面')
			context.commit('logout');
			uni.navigateTo({
				url: '/pages/auth/login'
			});
		}
	},

	/**
	 * 根据用户名和密码登录，并设置相应的状态信息
	 */
	async login(context, {
		username,
		password
	}) {
		const userInfo = {
			username,
			password
		}
		const res = await api.token.create(userInfo);
		if (res.errno === 0 && res.data.token) {
			context.commit('user/setUserName', res.data.username);
			context.commit('token/setToken', res.data.token);
			context.commit('login'); //修改登录状态			
			return true;
		} else {
			return false;
		}
	},
	/**
	 * 注册账号
	 */
	async register(context, userInfo) {
		const res = await api.user.create(userInfo)
		if (res.errno === 0) {
			return await context.dispatch('login', userInfo);
		} else {
			return false;
		}
	},
	/**
	 * 注销，退出登录
	 */
	logout(context) {
		context.commit('logout'); //修改登录状态
		uni.clearStorage(); //清除本地缓存
	},
}
Vue.use(Vuex)
export default new Vuex.Store({
	modules: {
		token,
		user,
		cart
	},
	state,
	actions,
	// getters,
	mutations,
	strict: debug, //设置运行模式
	plugin: debug ? [createLogger()] : [] //调试模式加入日志插件
})
