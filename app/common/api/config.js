//后端访问基础地址
//let base_url = 'http://127.0.0.1:5000'; //本地调试
let base_url = 'http://192.168.3.4:5000'; //开发环境，指向开发服务器 IP
//let base_url = 'http://server.facemagi.com:5000'; //生产环境

//API请求基础地址
let api_url = base_url + '/api/v1';

export default {
	//后端访问基础地址
	BASE_URL: base_url,

	//API请求基础地址
	API_URL: api_url
}
