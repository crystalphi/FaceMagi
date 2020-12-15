//引入常量
import types from '../types.js'

// initial state
const state = {
	value: uni.getStorageSync(types.TOKEN)
}

// getters
const getters = {
	getToken: state => state.value,
	verifyToken: state => {
		if (!state.value) {
			return false
		}
		return true
	}
}

// mutations
const mutations = {
	setToken(state, value) {
		uni.setStorageSync(types.TOKEN, value);
		state.value = value;
	},

	clearToken(state, value) {
		uni.removeStorageSync(types.TOKEN);
		state.value = ''
	}
}

// actions
const actions = {

}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations
}
