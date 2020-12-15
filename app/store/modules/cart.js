import api from '@/common/api'
import types from '../types.js'

// initial state
const state = {
	cartList: uni.getStorageSync(types.CART_LIST) || [],
}

// getters
const getters = {
	cartList: state => {
		return state.cartList;
	}
}

// actions
const actions = {

}

// mutations
const mutations = {
	addCart(state, {
		value,
		count
	}) {

		let product_id = value.product_id;
		const isAdded = state.cartList.find(e => e.product_id === product_id);
		if (isAdded) {
			isAdded.count += count;
		} else {
			state.cartList.push({
				product_id: product_id, //商品唯一id
				count: count, //购买数量
				checked: true, //是否选中支付
				value: value //商品详细信息
			})
		}

		uni.setStorage({
			key: types.CART_LIST,
			data: state.cartList,
			success: function() {}
		});

	},
	editCartCount(state, {
		product_id,
		count
	}) {
		const product = state.cartList.find(item => item.product_id === product_id);
		product.count += count;

		uni.setStorage({
			key: types.CART_LIST,
			data: state.cartList,
			success: function() {
				// console.log('数据缓存成功');
			}
		});
	},
	deleteCart(state, product_id) {
		const index = state.cartList.findIndex(item => item.product_id === product_id);
		state.cartList.splice(index, 1);

		uni.setStorage({
			key: types.CART_LIST,
			data: state.cartList,
			success: function() {
				// console.log('数据缓存成功');
			}
		});

	},
	//改变购物车中项目选中状态
	editCartItemStatus(state, payload) {
		let product = state.cartList.find(item => item.product_id === payload.product_id);

		if (payload.hasOwnProperty('checked')) {
			product.checked = payload.checked;
		} else {
			product.checked = product.checked ? false : true;
		}

		uni.setStorage({
			key: types.CART_LIST,
			data: state.cartList,
			success: function() {
				// console.log('数据缓存成功');
			}
		});
	},

	//改变购物车中项目选中状态
	editAllCartItemStatus(state, payload) {
		// let product = state.cartList.find(item => item.product_id === payload.product_id);

		// 			console.log(JSON.stringify(payload))
		// 
		// 			console.log(JSON.stringify(state.cartList));

		for (let product of state.cartList) {
			product.checked = payload;
			// 				if (payload.hasOwnProperty('checked')) {
			// 					product.checked = payload.checked;
			// 				} else {
			// 					product.checked = product.checked ? false : true;
			// 				}
		}

		uni.setStorage({
			key: types.CART_LIST,
			data: state.cartList,
			success: function() {
				// console.log('数据缓存成功');
			}
		});

	},

	emptyCart(state) {
		state.cartList = [];
		uni.removeStorage({
			key: types.CART_LIST,
			success: function(res) {}
		});
	},

}

export default {
	namespaced: true,
	state,
	getters,
	actions,
	mutations
}
