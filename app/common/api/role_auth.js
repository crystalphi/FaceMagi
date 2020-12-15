import request from '@/common/request'

export default {
  
  getList (map = {}) {
    //map['all']=true;
    return new Promise((resolve, reject) => {
      request.get('/role_auth', map).then(response => {
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
  
  update (id, data) {
    return new Promise((resolve, reject) => {
      request.put('/role_auth?id=' + id, data).then(response => {
        resolve(response)
      })
    })
  },
  
  addRuler(data) {
    return new Promise((resolve, reject) => {
      request.post('/role_auth', data).then(response => {
        resolve(response)
      })
    })
  },
  
  delete (id) {
    return new Promise((resolve, reject) => {
      request.delete('/role_auth?id=' + id).then(response => {
        resolve(response)
      })
    })
  }
}
