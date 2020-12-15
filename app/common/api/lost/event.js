import request from '@/common/request'
export default {

  create (data) {
    return new Promise((resolve, reject) => {
      request.post('/lost/event', data).then(response => {
        resolve(response)
      })
    })
  },

  getList (map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/lost/event', map).then(response => {
        resolve(response)
      })
    })
  },

  getInfo (id, map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/lost/event/' + id, map).then(response => {
        resolve(response)
      })
    })
  },

  update (id, data) {
    return new Promise((resolve, reject) => {
      request.put('/lost/event/' + id, data).then(response => {
        resolve(response)
      })
    })
  },

  delete (id) {
    return new Promise((resolve, reject) => {
      request.delete('/lost/event/' + id).then(response => {
        resolve(response)
      })
    })
  }
}
