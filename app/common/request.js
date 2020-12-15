import store from '@/store'
import config from '@/common/api/config'

// #ifdef H5
// import Fly from 'flyio/dist/npm/fly'
const fly = require('flyio')
console.log('--> under H5');
// #endif

// #ifndef H5
import Fly from 'flyio/dist/npm/wx'
const fly = new Fly();
console.log('--> not H5');
// #endif

//设置超时
//fly.config.timeout = 5000;
//显示加载提示框
const show_loading = false;

fly.interceptors.request.use((request) => {
	if (show_loading) {
		uni.showLoading({
			title: 'Loading...'
		});
	}
	request.baseURL = config.BASE_URL;
	
	const token = store.getters['token/getToken'];
	if (token) {
		//给所有请求添加自定义header
		request.headers["Authorization"] = token;
	}

	// 防止缓存
	if (request.method.toUpperCase() === 'POST' && request.headers['Content-Type'] !== 'multipart/form-data') {
		request.body = {
			...request.body,
			_t: Date.parse(new Date()) / 1000
		}
	} else if (request.method.toUpperCase() === 'GET') {
		request.params = {
			_t: Date.parse(new Date()) / 1000,
			...request.params
		}
	}
	return request
})

fly.interceptors.response.use(function(response) { //不要使用箭头函数，否则调用this.lock()时，this指向不对 
	let errmsg = '';
	const data = response.data;
	if (!data || typeof data !== 'object') {
		errmsg = 'invalid response data';
		uni.showToast({
			title: errmsg,
			icon: 'none'
		})
	} else {
		const errno = data.errno;
		switch (errno) {
			case 1001:
				// 数据检验未通过
				for (const i in data.data) {
					errmsg += data.data[i] + ';'
				}
				break;
			default:
				errmsg = data.errmsg;
				break
		}
		if (errmsg !== '' && errno !== 0) {
			uni.showToast({
				title: errmsg,
				icon: 'none'
			})
		}
		if (errmsg !== '' && errno === 0) {
			uni.showToast({
				title: errmsg,
				icon: 'none'
			})
		}
	}
	if (show_loading) {
		uni.hideLoading();
	}
	return response.data; //只返回业务数据部分
}, function(err) {
	// return Promise.resolve("ssss")
	// console.error("error-interceptor:" + JSON.stringify(err))
	if (show_loading) {
		uni.hideLoading();
	}
	let errmsg = err.message;
	switch (err.status) {
		case 0:
			errmsg = "network connection fail";
			uni.showToast({
				title: errmsg,
				icon: 'none'
			})
			break;
		case 401:
			store.dispatch('logout');
			uni.navigateTo({
				url: '/pages/auth/login'
			});
			break;
		default:
			uni.showToast({
				title: errmsg,
				icon: 'none'
			})
	}
})

export default fly

export {
	fly,
	config
}
