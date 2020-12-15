import request from '@/common/request'

export default {

  create(data) {
    return new Promise((resolve, reject) => {
      request.post('/district', data).then(response => {
        resolve(response)
      })
    })
  },

  getList(map = {}) {
    map.type = map.type || 'province';
    return new Promise((resolve, reject) => {
      request.get('/district', map).then(response => {
        resolve(response)
      })
    })
  },

  getInfo(id, map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/district/' + id, map).then(response => {
        resolve(response)
      })
    })
  },

  update(id, data) {
    return new Promise((resolve, reject) => {
      request.put('/district/' + id, data).then(response => {
        resolve(response)
      })
    })
  },

  delete(id) {
    return new Promise((resolve, reject) => {
      request.delete('/district/' + id).then(response => {
        resolve(response)
      })
    })
  }
}
