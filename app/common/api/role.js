import request from '@/common/request'

export default {

	create(data) {
		return new Promise((resolve, reject) => {
			request.post('/role', data).then(response => {
				resolve(response)
			})
		})
	},

	delete(id) {
		return new Promise((resolve, reject) => {
			request.delete('/role/' + id).then(response => {
				resolve(response)
			})
		})
	},

	deleteUser(id, uid) {
		return new Promise((resolve, reject) => {
			request.delete('/role/' + id, {
				uid: uid
			}).then(response => {
				resolve(response)
			})
		})
	},

	addUser(data) {
		return new Promise((resolve, reject) => {
			request.post('/role', data).then(response => {
				resolve(response)
			})
		})
	},

	getList(map = {}) {
		return new Promise((resolve, reject) => {
			request.get('/role', map).then(response => {
				resolve(response)
			})
		})
	},

	getInfo(id, map = {}) {
		//查询参数可以指定member=1查询会员信息，而不是用户本身的信息
		return new Promise((resolve, reject) => {
			request.get('/role/' + id, map).then(response => {
				resolve(response)
			})
		})
	},

	//更新用户基本信息
	update(id, data) {
		return new Promise((resolve, reject) => {
			request.put('/role/' + id, data).then(response => {
				resolve(response)
			})
		})
	},

}
