import api from '@/common/api/index.js' //远程数据访问API函数
import types from '../types.js'; //引入常量
import {logger,dump} from '@/common/logger.js'
// initial state
const state = {
	username: uni.getStorageSync(types.USER_NAME),
}

// getters
const getters = {
	username: state => {
		return state.username;
	}
}

// mutations
const mutations = {
	setUserName(state, value) {
		uni.setStorageSync(types.USER_NAME, value)
		state.username = value
	},
}

// actions
const actions = {
	//用户信息需要从服务器上获取，以便及时更新账户信息
	async getUserInfo(context) {
		const username = context.getters.username;
		if (username) {
			const res = await api.user.getInfoByName(username).catch(e=>{
				console.log(e);
			});
      logger.info(res);
			if (res.errno === 0) {        
				return res.data;
			} else {
				return false;
			}
		} else {
			return false;
		}
	}
}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations
}
