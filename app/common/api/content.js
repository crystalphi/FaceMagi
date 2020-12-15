import request from '@/common/request'

export default {

  create(data) {
    return new Promise((resolve, reject) => {
      request.post('/content', data).then(response => {
        resolve(response)
      })
    })
  },

  getList(map = {}) {
    map.type = map.type || 'default'
    return new Promise((resolve, reject) => {
      request.get('/content', map).then(response => {
        resolve(response)
      })
    })
  },

  getInfo(slug, map = {}) {
    map['slug'] = slug;
    return new Promise((resolve, reject) => {
      request.get('/content', map).then(response => {
        resolve(response)
      })
    })
  },

  update(id, data) {
    return new Promise((resolve, reject) => {
      request.put('/content/' + id, data).then(response => {
        resolve(response)
      })
    })
  },

  delete(id) {
    return new Promise((resolve, reject) => {
      request.delete('/content/' + id).then(response => {
        resolve(response)
      })
    })
  }
}
