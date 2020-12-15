import request from '@/common/request'
export default {

  create (data) {
    data.type = 'category'
    return new Promise((resolve, reject) => {
      request.post('/meta', data).then(response => {
        resolve(response)
      })
    })
  },

  getList (map = {}) {
    map.type = 'category'
    return new Promise((resolve, reject) => {
      request.get('/meta', map).then(response => {
        resolve(response)
      })
    })
  },

  getInfo (id, map = {}) {
    map.type = 'category'
    return new Promise((resolve, reject) => {
      request.get('/meta/' + id, map).then(response => {
        resolve(response)
      })
    })
  },

  update (id, data) {
    data.type = 'category'
    return new Promise((resolve, reject) => {
      request.put('/meta/' + id, data).then(response => {
        resolve(response)
      })
    })
  },

  delete (id) {
    return new Promise((resolve, reject) => {
      request.delete('/meta/' + id).then(response => {
        resolve(response)
      })
    })
  }
}
