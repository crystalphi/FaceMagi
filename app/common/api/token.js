import request from '@/common/request'

export default {
	create(userInfo) {
		return new Promise((resolve, reject) => {
			request.post('/token', userInfo).then(response => {
				// console.log(response)
				resolve(response)
			})
		})
	}
}
