import request from '@/common/request'

export default {
  
  getList (map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/user_tag', map).then(response => {
        resolve(response)
      })
    })
  },
  
  //getInfo (slug) {
  //  return new Promise((resolve, reject) => {
  //    request.get('/userTag/' + slug).then(response => {
  //      resolve(response)
  //    })
  //  })
  //},
  
  //update (id, data) {
  //  return new Promise((resolve, reject) => {
  //    request.put('/userTag/' + id, data).then(response => {
  //      resolve(response)
  //    })
  //  })
  //},
  
  addTag(data) {
    return new Promise((resolve, reject) => {
      request.post('/user_tag', data).then(response => {
        resolve(response)
      })
    })
  },
  
  delete (id) {
    return new Promise((resolve, reject) => {
      request.delete('/user_tag?id=' + id).then(response => {
        resolve(response)
      })
    })
  }
}
