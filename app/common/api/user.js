import request from '@/common/request'

export default {

	create(data) {
		return new Promise((resolve, reject) => {
			request.post('/user', data).then(response => {
				resolve(response)
			})
		})
	},

	delete(id) {
		return new Promise((resolve, reject) => {
			request.delete('/user/' + id).then(response => {
				resolve(response)
			})
		})
	},

	deleteTag(id, tag_id) {
		return new Promise((resolve, reject) => {
			request.delete('/user/' + id, {
				tag_id: tag_id
			}).then(response => {
				resolve(response)
			})
		})
	},

	addTag(data) {
		return new Promise((resolve, reject) => {
			request.post('/user', data).then(response => {
				resolve(response)
			})
		})
	},

	getList(map) {
		return new Promise((resolve, reject) => {
			request.get('/user', map).then(response => {
				resolve(response)
			})
		})
	},

	getInfo(id, map = {}) {
		//查询参数可以指定member=1查询会员信息，而不是用户本身的信息
		return new Promise((resolve, reject) => {
			request.get('/user/' + id, map).then(response => {
				resolve(response)
			})
		})
	},

	getMemberInfo(uid) {
		//查询参数可以指定member=1查询会员信息，而不是用户本身的信息
		return new Promise((resolve, reject) => {
			request.get('/user/' + uid, {
				member: 1
			}).then(response => {
				resolve(response)
			})
		})
	},

	getInfoByName(userName) {
		return new Promise((resolve, reject) => {
			request.get('/user', {
				username: userName
			}).then(response => {
				// console.log(response)
				resolve(response)
			})
		})
	},

	//更新用户基本信息
	update(id, data) {
		return new Promise((resolve, reject) => {
			request.put('/user/' + id, data).then(response => {
				resolve(response)
			})
		})
	},

	//更新user_member信息
	updateMemberInfo(uid, data) {
		return new Promise((resolve, reject) => {
			request.put('/user/' + uid + '?member=1', data).then(response => {
				resolve(response)
			})
		})
	}
}
