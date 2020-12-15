import request from '@/common/request'

export default {

  create(data) {
    return new Promise((resolve, reject) => {
      request.post('/resource', data).then(response => {
        resolve(response)
      })
    })
  },

  getList(map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/resource', {
        params: map
      }).then(response => {
        resolve(response)
      })
    })
  },

  getInfo(id, map = {}) {
    return new Promise((resolve, reject) => {
      request.get('/resource/' + id, {
        params: map
      }).then(response => {
        resolve(response)
      })
    })
  },

  update(id, data) {
    return new Promise((resolve, reject) => {
      request.put('/resource/' + id, data).then(response => {
        resolve(response)
      })
    })
  },

  delete(id) {
    return new Promise((resolve, reject) => {
      request.delete('/resource/' + id).then(response => {
        resolve(response)
      })
    })
  }
  ,
  
  //撤销授权
  deleteRole(id,role_id) {
    return new Promise((resolve, reject) => {
      request.delete('/resource/' + id,{role_id:role_id}).then(response => {
        resolve(response)
      })
    })
  },
  
  //增加授权
  addRole(data) {
    return new Promise((resolve, reject) => {
      request.post('/resource', data).then(response => {
        resolve(response)
      })
    })
  },
}
