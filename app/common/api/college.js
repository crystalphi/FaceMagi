import request from '@/common/request'

export default {

  create(data) {
    return new Promise((resolve, reject) => {
      request.post('/college', data).then(response => {
        resolve(response)
      })
    })
  },

  getList(map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/college', map).then(response => {
        resolve(response)
      })
    })
  },

  getInfo(id, map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/college/' + id, {
        params: map
      }).then(response => {
        resolve(response)
      })
    })
  },

  update(id, data) {
    return new Promise((resolve, reject) => {
      request.put('/college/' + id, data).then(response => {
        resolve(response)
      })
    })
  },

  delete(id) {
    return new Promise((resolve, reject) => {
      request.delete('/college/' + id).then(response => {
        resolve(response)
      })
    })
  }
}
