import Vue from 'vue';
//import * as request from '@/common/request' //flyio
// app 权限判断及引导：https://ext.dcloud.net.cn/plugin?id=594
import permission from "@/js_sdk/wa-permission/permission.js"
import payment from '@/common/payment.js'
import CryptoJS from "@/js_sdk/crypto-js.js"


export default {

	//从主配置服务器获取基本配置信息
	//如果验证失败, 则等待 1 秒后重新尝试, 最多 3 次
	getBaseCfg(retry=3) {
		return new Promise(async (resolve, reject) => {
			let that = this;
			//访问外网太慢，针对开发调试使用单独配置 base.cfg.dev
			let cfgUrl = 'http://facemagi.com/config/base.cfg';
			switch(uni.getSystemInfoSync().platform) {
				case 'ios':
				case 'android':
				case 'weixin': //？
					break;
				default: //开发环境
					cfgUrl = 'http://facemagi.com/config/base.cfg.dev';
					break;
			}
			await uni.request({
				url: cfgUrl,
				success: (res) => {
					if(res.statusCode == 200){
						console.log('远程获取配置成功：' + JSON.stringify(res.data));
						//解析配置
						let cfg = res.data;
						let baseCfg = null;
						switch(uni.getSystemInfoSync().platform){
							case 'ios':
								console.log('运行iOS上');
								baseCfg = cfg.ios;
								break;
							case 'android':
								console.log('运行Android上');
								baseCfg = cfg.android;
								break;
							case 'weixin': //？
								console.log('运行在微信上');
								baseCfg = cfg.weixin;
								break;
							default:
								console.log('运行在开发者工具上');
								baseCfg = cfg.ios;
								break;
						}
						Vue.prototype.$BASE_URL = baseCfg.base_url;
						Vue.prototype.$API_URL = baseCfg.base_url + '/api/v1';
						Vue.prototype.IAPOrders = baseCfg.IAPOrders;
						resolve(baseCfg);
					} else {
						console.log('远程获取配置失败。错误信息：' + JSON.stringify(res.statusCode));
						//reject({"errno": -1, "msg": JSON.stringify(res.statusCode)});
					}
				},
				fail: (e) => {
					console.log('远程获取配置失败。1s 后再次尝试~ 错误信息：' + JSON.stringify(e));
					retry = retry - 1;
					if (retry > 0) {
						setTimeout(() => {
							this.getBaseCfg(retry)
							.then((baseCfg) => {
								resolve(baseCfg);
							})
							.catch(() => {
								reject();
							});
						}, 1000); //1s
					} else {
						reject();
					}
				},
				complete: () => {
				}
			});
		});
	},
	
	//提交设备信息等相关数据到服务端，执行登录验证。若本地无 user_id 缓存，则后端生成。
	//如果验证失败, 则等待 5 秒后重新尝试, 最多 5 次
	async execUserLogin(retry=5) {
		return new Promise((resolve, reject) => {
			let retry_max = retry;
			console.log('执行设备登录 ... #' + (retry_max - retry));
			let loginSuccess = false;
			
			let _user_id = this.getUserIdLocal();
			if (_user_id) {
				console.log('本地缓存 user_id: ' + _user_id);
			}
			
			let res = this.backendUserLogin(_user_id)
			.then((res) => {
				//console.log('--> userLogin res:', res);
				if (res.errno === 0) { //登录成功，存储相关信息，半小时后再刷新登录
					let rdata = res.data;
					//console.log('登录返回信息:', rdata);
					if (rdata) {
						if (rdata.login_success) {
							uni.setStorageSync('user_id', rdata.user_id);
							uni.setStorageSync('token', rdata.token);
							// 注意：虽然返回了 token，但后续接口鉴权实际上还是基于自定义算法校验
							// 原因是 token 校验依赖于数据库，存在可靠性风险
							console.log('后端登录成功！user_id: ' + rdata.user_id + 
										'，token：' + rdata.token);
							loginSuccess = true;
							setTimeout(() => {
								this.execUserLogin(retry);
							}, 1800000); //30min
							resolve();
						} else {
							uni.removeStorageSync('user_id');
							uni.removeStorageSync('token');
						}
					}
				}
				if (loginSuccess == false) { //登录失败，每 5s 重试登录，连续 5 次
					retry = retry - 1;
					if (retry > 0) {
						setTimeout(() => {
							this.execUserLogin(retry);
						}, 5000); //5s
					}
					console.log('登录失败！5s 后再次尝试~');
				}
			})
			.catch((e) => {
				let that = this;
				uni.showModal({
					title: e.errMsg,
					content: 'Please check the network status.',
					showCancel: false,
					confirmText: 'Confirm',
					cancelText: 'Cancel',
					success: () => {
						that.exitApp();
					}
				});
			});
		});
	},
	
	getTimeStamp() {
		Date.prototype.getUTCTime = function() { //有 bug，获取到的仍为时区时间
		  return new Date(
		    this.getUTCFullYear(),
		    this.getUTCMonth(),
		    this.getUTCDate(),
		    this.getUTCHours(),
		    this.getUTCMinutes(), 
		    this.getUTCSeconds(),
			this.getMilliseconds()
		  ).getTime();
		}
		
		//let _timestamp = Math.floor((new Date()).getUTCTime() / 60000)
		let _timestamp = (new Date()).toISOString(); //2020-04-04T14:07:24.058Z
		_timestamp = _timestamp.slice(0, 16); //2020-04-04T14:07
		_timestamp = _timestamp.replace(':', '-'); //2020-04-04T14-07
		
		return _timestamp;
	},
	
	getCurrentTimeStr() {
		// 对Date的扩展，将 Date 转化为指定格式的String
		// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符， 
		// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) 
		// 例子： 
		// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423 
		// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18 
		Date.prototype.Format = function (fmt) {
		    var o = {
		        "M+": this.getMonth() + 1, //月份 
		        "d+": this.getDate(), //日 
		        "H+": this.getHours(), //小时 
		        "m+": this.getMinutes(), //分 
		        "s+": this.getSeconds(), //秒 
		        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
		        "S": this.getMilliseconds() //毫秒 
		    };
		    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
		    for (var k in o)
		    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
		    return fmt;
		}
		
		var _now = new Date().Format("yyyy-MM-dd HH:mm:ss");
		return _now;
	},
	
	//执行服务端登录并获取用户信息 -- 使用uniapp方法
	backendUserLogin(_user_id) {
		return new Promise((resolve, reject) => {
			let deviceInfo = this.getDeviceInfo();
			let _timestamp = this.getTimeStamp();
			//console.log('--> backendUserLogin _timestamp:' + _timestamp);
			uni.request({
				url: Vue.prototype.$API_URL + '/auth/user_login',
				data: {'device_info': deviceInfo,
						'user_id': _user_id,
						'vr_code': this.zzzHash(deviceInfo + String(_timestamp))},
				header: {
					"Content-Type": "application/x-www-form-urlencoded"
				},
				method: 'POST',
				success: (res) => {
					//console.log('--> res.data:', res.data);
					resolve(res.data);
				},
				fail: (e) => {
					reject(e);
				}
			});
		});
	},
	
	// 从本地存储获取苹果账号信息，如果没有或过期则执行苹果账号登录
	async getAppleLoginInfo() {
		return new Promise((resolve, reject) => {
			//TODO: 判断 IOS OS 版本，若低于 13 则返回失败
			//Sign in with Apple is available with iOS / iPadOS 13 or later.
			if (uni.getSystemInfoSync().platform == 'ios' 
			&& uni.getSystemInfoSync().system < '13') {
				reject({"errno": -1, "msg": "Cannot sign in with Apple. It is available with iOS / iPadOS 13 or later."});
			}
			uni.getProvider({
				service: 'oauth',
				success: function (res) {
					console.log('获取可用的 oauth 提供者:' +  JSON.stringify(res));
					let use_provider = null;
					if (~res.provider.indexOf('apple')) {
						use_provider = 'apple';
					} else if (~res.provider.indexOf('weixin')) {
						use_provider = 'weixin';
					}
					if (use_provider) {
						uni.login({
							provider: use_provider,
							success: function (loginRes) {
								uni.getUserInfo({
									provider: use_provider,
									success(res) {
										console.log('获取用户信息成功：' + use_provider);
										//console.log('用户信息：' + JSON.stringify(res));
										// 获取用户信息成功：apple,{"errMsg":"getUserInfo:ok","rawData":"{\"openId\":\"001141.e2e2372ea...485d31d5a.1027\",\"fullName\":{\"familyName\":\"jayadvaita\",\"giveName\":\"das\",\"givenName\":\"das\"},\"email\":\"vbcswggka7@privaterelay.appleid.com\",\"authorizationCode\":\"c8da705871ec24151.....TYY7XS9t7iLFbIqg\",\"identityToken\":\"eyJraWQi.....-ifw\",\"realUserStatus\":2}","userInfo":{"openId":"001141.e2e2372ea...485d31d5a.1027","fullName":{"familyName":"jayadvaita","giveName":"das","givenName":"das"},"email":"vbcswggka7@privaterelay.appleid.com","authorizationCode":"c8da705871ec24151b582e2531d8bcab7.0.nrrur.mBcS.....aJ8-ifw","realUserStatus":2},"signature":""}
										let _user_id = res.userInfo.openId;
										let user_info = {'user_id': _user_id, 'timestamp': Date.parse(new Date())};
										resolve({"errno": 0, "user_info": user_info});
									}
								})
							},
							fail: function (err) {
								reject({"errno": -1, "msg": "apple login fail, " + JSON.stringify(err)});
							}
						});
					} else {
						reject({"errno": -1, "msg": "no wanted login method"});
					}
				},
				fail: function(err) {
					// 获取 services 失败
					reject({"errno": -1, "msg": "getProvider error"});
				}
			});
			
			/*
			// #ifdef APP-PLUS
			let appleOauth = null;
			plus.oauth.getServices(function(services) {
				console.log('--> services:' + JSON.stringify(services));
				for (var i in services) {
					var service = services[i];
					// 获取苹果授权登录对象，苹果授权登录id 为 'apple' iOS13以下系统，不会返回苹果登录对应的 service
					console.log('--> service.id:' + service.id);
					if (service.id == 'apple') {
						appleOauth = service;
						break;
					}
				}
				if (appleOauth != null) {
					appleOauth.login((oauth) => { // 授权成功
						// 苹果授权返回的信息在 oauth.target.appleInfo 中
						console.log('apple login success! user:' + oauth.target.appleInfo.user);
						let user_info = {'user': oauth.target.appleInfo.user, 
									 'timestamp': Date.parse(new Date())};
						resolve({"errno": 0, "user_info": user_info});
					}, function(err) { // 授权失败
						reject({"errno": -1, "msg": "apple login fail, " + JSON.stringify(err)});
					}, { // 默认只请求用户名，如请求用户邮箱，需要设置 scope: 'email'
						scope: 'email'
					})
				} else {
					reject({"errno": -1, "msg": "apple login unsupported"});
				}
			}, function(err) {
				// 获取 services 失败
				reject({"errno": -1, "msg": "oauth getServices error"});
			})
			// #endif
			
			// #ifndef APP-PLUS
			reject({code: -1, err: "not supported in this environment!"});
			// #endif
			*/
		});
	},
	
	checkApplLogin() {
		return new Promise((resolve, reject) => {
			if (Vue.prototype.apple_user_id) {
				resolve();
			} else {
				this.getAppleLoginInfo()
				.then((res) => {
					console.log('apple 登录成功:' +  JSON.stringify(res));
					//res: {"errno":0,"user_info":{"user_id":"001141.e2e2372eaa554136b3de658485d31d5a.1027","timestamp":1588597310000}}
					this.setStorageValue('ios_user_info', res.user_info);
					Vue.prototype.apple_user_id = res.user_info.user_id;
					resolve();
				})
				.catch((e) => {
					console.log('apple 登录失败:' +  JSON.stringify(e));
					//console.log('--> e.msg: ' + e.msg);
					//e.msg 示例: apple login fail, {"code":1001,"errMsg":"login:fail:Canceled"}
					if (e.msg.indexOf("login:fail:Canceled") <= 0) { //非用户取消登录
						uni.showModal({
							title: this.translate('apple_login_fail'),
							confirmText: this.translate('confirm'),
							content: e.msg,
							showCancel: false
						});
					}
					reject();
				});
			}
		});
	},
	
	//获取演示图片数据
	getDemoList(map = {}) {
		map.storage = map.storage || '';
		return new Promise((resolve, reject) => {
			//console.log('map:' + map);
			/*
			request.fly.get('/api/v1/media/face_demo', map)
				.then(response => {
					resolve(response);
				})
				.catch(error => {
					console.log('--> fly error:', error);
					// fly 错误码含义：
					//	0	网络错误
					//	1	请求超时
					//	2	文件下载成功，但保存失败，此错误只出现node环境下
					//	>=200	http请求状态码
					uni.showToast({
						title: error.status + ' - ' + error.message,
						duration: 2000,
						icon: 'none'
					});
					resolve({
						"errno": -1
					}); //将错误作为结果返回
					//reject(error); //抛出错误
				});
			*/
			uni.request({
				url: Vue.prototype.$API_URL + '/media/face_demo',
				data: map,
				header: {},
				method: 'GET',
				success: (res) => {
					if(res.statusCode == 200){
						resolve(res.data);
					} else {
						console.log('--> res:', JSON.stringify(res));
						reject({"errno": -1});
					}
				},
				fail: (e) => {
					//console.log('--> e.data:', e.data);
					reject({"errno": -1});
				}
			});
		})
	},

	//获取后端图片处理功能清单
	getConfigFunctions(act = '', sex = 'all') {
		return new Promise((resolve, reject) => {
			/*
			request.fly.get('/api/v1/media/functions', {
					'act': act,
					'sex': sex
				})
				.then(response => {
					resolve(response);
				});
			*/
			//console.log('--> getConfigFunctions(): ' + Vue.prototype.$API_URL + '/media/functions');
			uni.request({
				url: Vue.prototype.$API_URL + '/media/functions',
				data: {
					'act': act,
					'sex': sex
				},
				success: (res) => {
					if(res.statusCode == 200){
						resolve(res.data);
					} else {
						resolve({'errno': -1, 'msg': JSON.stringify(res)});
					}
				}
			});
		})
	},
	
	//向后端提交图片处理任务，并循环查询处理结果
	async taskProcess(tk, 			//访问令牌（非空）
					m_id, 			//图片 ID（新图片为空，处理任务非空）
					m_path, 		//上传图片路径（新图片非空，处理任务为空）
					user_id, 		//用户 ID（非空）
					func_group, 	//处理功能类别（新图片为空，处理任务非空）
					func_class, 	//处理功能类型（新图片为空，处理任务非空）
					func_name, 		//处理功能名称（新图片为空，处理任务非空）
					func_params,	//处理功能参数（新图片为空，处理任务非空）
					i18n_msg = {	//多语言支持
						'api_processing': 'processing ...',
						'api_failed': 'failed to req API ...',
						'api_process_timeout': 'process timeout',
						'api_add_task_err': 'add task error',
						'api_query_task_err': 'query task error'
					},
					demo_idx = null
	) {
		return new Promise(async (resolve, reject) => {
			let args = "?tk=" + tk;
			if (m_id != null) {
				args += "&m_id=" + m_id;
			}
			if (demo_idx != null) {
				args += "&demo_idx=" + demo_idx;
			}
			let formdata = {
				"params": JSON.stringify({
					"user_id": user_id,
					"func_group": func_group,
					"func_class": func_class,
					"func_name": func_name,
					"func_params": func_params
				})
			}
			uni.showLoading({mask: true, title: i18n_msg["api_processing"]});
			await this.taskAdd(m_path, args, formdata)
			.then(async (res) => {
				uni.hideLoading();
				//console.log('--> res:' + res);
				if (res.errno === 0 && res.data != null) {
					console.log('transmit taskAdd response data: ' + JSON.stringify(res.data));
					//Response data: Object {task_id: 1569843399.2440996}
					//根据返回的 task_id 查询任务状态
					if ('task_id' in res.data) {
						let args2 = "?task_id=" + res.data['task_id'];
						if ('m_id' in res.data) {
							args2 += "&m_id=" + res.data['m_id'];
						}
						if (func_group) {args2 += "&func_group=" + func_group;}
						if (func_class) {args2 += "&func_class=" + func_class;}
						if (func_name) {args2 += "&func_name=" + func_name;}
						if (func_params) {args2 += "&func_params=" + func_params;}
						let max_times = 15; //最多查询结果次数(s)
						let progress = 0; //处理进度
						for (let i = 0; i < max_times; i++) { //每秒查询一次
							uni.hideLoading();
							uni.showLoading({mask: true, title: i18n_msg["api_processing"] + ' ' + progress + '%'});
							await this.taskQuery(args2)
							.then((res2) => {
								if (res2.errno === 0 && res2.data != null) {
									console.log('0 - transmit taskQuery response data. m_id:' + res2.data['m_id'] + ', msg:' + res2.data['msg']);
									progress = res2.data['progress'];
									if ('image' in res2.data) {
										uni.hideLoading();
										max_times = 0; //采用 then catch 写法后无法 break，故此设置循环最大值为 0 以便退出
										resolve(res2.data, i18n_msg); // 获取到处理结果
									} else {
										if (res2.data['progress'] === 100 
										|| res2.data['progress'] === 0) {
											uni.hideLoading();
											max_times = 0;
											reject(i18n_msg["api_msg_cannot_process"]);
										}
									}
								} else {
									console.log('1 - transmit taskQuery response:', res2);
									uni.hideLoading();
									max_times = 0;
									reject(res2);
								}
							})
							.catch((e) => {
								uni.hideLoading();
								console.log('taskQuery() fail: ' + JSON.stringify(e));
							});
							if (i == max_times - 1) {
								uni.hideLoading();
								max_times = 0;
								reject(i18n_msg["api_process_timeout"]);
							} else {
								await this.sleep(1000);
							}
						}
					} else {
						uni.hideLoading();
						reject(i18n_msg["api_add_task_err"] + ': no task_id, is the server online?');
					}
				} else { //比如接口访问太频繁时
					uni.hideLoading();
					console.log('--> res:' + JSON.stringify(res));
					reject(i18n_msg["api_add_task_err"] + '');
				}
				reject({code: -1, err: 'unkown error'});
			})
			.catch((e) => {
				uni.hideLoading();
				//console.log(JSON.stringify(e));
				reject(JSON.stringify(e));
			});
		});
	},

	//向后端提交图片处理任务
	async taskAdd(m_path, args, data = {}) {
		//根据后端返回的存储方式进行调用不同接口（注：目前只实现了 local 这一种方式）
		//const response = await request.fly.get("/api/v1/media/config");
		return new Promise((resolve, reject) => {
			uni.request({
				url: Vue.prototype.$API_URL + '/media/config',
				success: (res) => {
					if(res.statusCode == 200){
						//resolve(res.data);
						//console.log('--> res:' + JSON.stringify(res));
						//console.log('--> res.data:' + JSON.stringify(res.data));
						const storageType = res.data.data.storage;
						switch (storageType) {
							case "local":
								{
									this.taskAddLocal(m_path, args, data)
										.then(res => {
											//console.log('-->xx res:' + JSON.stringify(res));
											resolve(res);
										})
										.catch((e) => {
											console.log('taskAddLocal(): ' + JSON.stringify(e));
											reject(e);
										});
								}
							case "amz_s3":
								{
									this.uploadAmzs3(m_path, data)
										.then(res => {
											resolve(res);
										})
										.catch((e) => {
											console.log('uploadAmzs3(): ' + JSON.stringify(e));
										});
								}
						}
					} else {
						resolve({"errno": -1, "status":res.statusCode});
					}
				},
				fail: (e) => {
					reject(e);
				}
			});
		});
	},
	
	//查询处理任务执行状态
	async taskQuery(args) {
		return new Promise((resolve, reject) => {
			if (args.indexOf('task_id') >= 0) {
				console.log('request args: ' + args);
				/*
				request.fly.config.headers = this.setAuthHeader({});
				request.fly.get(request.Vue.prototype.$API_URL +
						'/media/task_query' + args)
					.then(response => {
						resolve(response);
					})
				*/
				uni.request({
					url: Vue.prototype.$API_URL + '/media/task_query' + args,
					header: this.setAuthHeader({}),
					success: (res) => {
						if(res.statusCode == 200){
							resolve(res.data);
						} else {
							resolve({"errno": -1, "status":res.statusCode});
						}
					},
					fail: (e) => {
						reject(e);
					}
				});
			} else {
				console.error('no task_id found!');
			}
		});
	},
	
	//保存任务处理后图片
	async taskApplyImageSave(m_id, func_group, func_class, func_name, func_params) {
		let args = "?m_id=" + m_id;
		if (func_group) {args += "&func_group=" + func_group;}
		if (func_class) {args += "&func_class=" + func_class;}
		if (func_name) {args += "&func_name=" + func_name;}
		if (func_params) {args += "&func_params=" + func_params;}
		return new Promise((resolve, reject) => {
			console.log('request args: ' + args);
			/*
			request.fly.config.headers = this.setAuthHeader({});
			request.fly.get(request.Vue.prototype.$API_URL +
					'/media/task_apply_image_save' + args)
				.then(response => {
					resolve(response);
				})
			*/
			uni.request({
				url: Vue.prototype.$API_URL + '/media/task_apply_image_save' + args,
				header: this.setAuthHeader({}),
				success: (res) => {
					if(res.statusCode == 200){
						resolve(res.data);
					} else {
						resolve({"errno": -1, "status":res.statusCode});
					}
				},
				fail: (e) => {
					reject(e);
				}
			});
		});
	},
	
	//恢复任务处理后图片为原图
	async taskRestoreOriginalImage(m_id) {
		let args = "?m_id=" + m_id;
		return new Promise((resolve, reject) => {
			console.log('request args:', args);
			/*
			request.fly.config.headers = this.setAuthHeader({});
			request.fly.get(request.Vue.prototype.$API_URL +
					'/media/task_restore_original_image' + args)
				.then(response => {
					resolve(response);
				})
			*/
			uni.request({
				url: Vue.prototype.$API_URL + '/media/task_restore_original_image' + args,
				header: this.setAuthHeader({}),
				success: (res) => {
					if(res.statusCode == 200){
						resolve(res.data);
					} else {
						resolve({"errno": -1, "status":res.statusCode});
					}
				},
				fail: (e) => {
					reject(e);
				}
			});
		});
	},
	
	//----- 以下为上述接口所调用的子函数 -----

	//请求和上传到自有服务器 -- 使用uniapp方法
	async taskAddLocal(m_path, args, data = {}) {
		let formData = Object.assign({}, data, {
			"storage": "local"
		});
		console.log('taskAddLocal args: ' + args);
		return new Promise((resolve, reject) => {
			//如果参数中指定了 m_id 或者 demo_idx，则不用上传图片
			if (args.indexOf('m_id') >= 0 || args.indexOf('demo_idx') >= 0) {
				//console.log('taskAddLocal() using args with m_id: ' + args);
				console.log('--> formData:' + JSON.stringify(formData));
				//只发送处理请求，不上传文件
				let _headers = {
						"Content-Type": "application/x-www-form-urlencoded"};
				_headers = this.setAuthHeader(_headers);
				//console.log('--> _headers:' + _headers);
				uni.request({
					url: Vue.prototype.$API_URL + '/media/task_add' + args,
					data: formData,
					header: _headers,
					method: 'POST',
					success: (res) => {
						//console.log('--> task_add res.data: ' + JSON.stringify(res.data));
						if(res.statusCode == 200){
							resolve(res.data);
						} else {
							resolve({"errno": -1, "status":res.statusCode});
						}
					},
					fail: (e) => {
						reject(e);
					}
				});
			}
			//否则需读取 m_path 文件做上传
			else if (m_path != null) {
				let _headers = {
						"Content-Type": "application/x-www-form-urlencoded"};
				_headers = this.setAuthHeader(_headers);
				//console.log('--> _headers:' + _headers);
				
				if (m_path.substr(0, 30).indexOf('base64') > 0) {
					// m_path 为 base64 格式的图片内容
					console.log('taskAddLocal() using m_b64');
					formData['m_b64'] = m_path;
					uni.request({
						url: Vue.prototype.$API_URL + '/media/task_add' + args,
						data: formData,
						header: _headers,
						method: 'POST',
						success: (res) => {
							console.log('--> task_add res.data:', res.data);
							if(res.statusCode == 200){
								resolve(res.data);
							} else {
								resolve({"errno": -1, "status":res.statusCode});
							}
						},
						fail: (e) => {
							reject(e);
						}
					});
				} else {
					// m_path 为图片文件路径
					console.log('taskAddLocal() using file path:', m_path);
					uni.uploadFile({
						url: Vue.prototype.$API_URL + '/media/task_add' + args,
						filePath: m_path,
						name: 'image',
						header: _headers,
						formData: formData,
						success: (res) => {
							//reject('upload test fail');
							//console.log('--> task_add res.data:', res.data);
							if (res.statusCode == 200) {
								resolve(JSON.parse(res.data));
							} else {
								resolve({"errno": -1, "status":res.statusCode});
							}
						},
						fail: (e) => {
							console.log('--> task_add e:', e);
							reject(e);
						}
					});
				}
			} else {
				console.error('no m_id or m_path found!');
				resolve(false);
			}
		});
	},

	//上传到云存储服务（TODO: 未实现，勿用）
	uploadAmzs3(m_path, data) {
		return new Promise((resolve, reject) => {
			//
		});
	},
	
	// 保存base64图片
	saveBase64ImageFile(base64, saveToAlbum=false, quality=100) {
		return new Promise((resolve, reject) => {
			// #ifdef APP-PLUS
			const bitmap = new plus.nativeObj.Bitmap("test");
			// 从本地加载Bitmap图片
			bitmap.loadBase64Data(base64, function() {
				//TODO: ios 为_doc，android 为_downloads?
				//let timeStamp = new Date().getTime();
				let timeStamp= "temp_saved_image";
				const url = "_doc/" + timeStamp + ".png";
				bitmap.save(url, {
					overwrite: true,  // 是否覆盖
					quality: quality  // 图片清晰度
				}, (i) => {
					if (saveToAlbum) {
						uni.saveImageToPhotosAlbum({
							filePath: url,
							success: function() {
								resolve({
									code: 0,
									msg: 'save image album success',
									filePath: url
								});
							},
							fail: function() {
								resolve({code: -1});
							}
						});
					} else {
						resolve({
							code: 0,
							msg: 'save image temp success',
							filePath: url
						});
					}
				}, (e) => {
					reject('save image fail: ' + JSON.stringify(e));
				});
			}, (e) => {
				reject('load image fail: ' + JSON.stringify(e));
			});
			// #endif
		});
	},
	
	getStorageValue(key) {
		try {
			const value = uni.getStorageSync(key);
			//console.log('--> value:', value);
			return value;
		} catch (e) {
			return null;
		}
	},
	setStorageValue(key, value) {
		try {
			uni.setStorageSync(key, value);
		} catch (e) {
			console.log('ERROR: save ' + key+ ' failed:' + e);
		}
	},
	
	async requestAndroidPermission(permissionID, authorizedCallback) {
		var result = await permission.requestAndroidPermission(permissionID)
		if (result == 1) {
			let authorized = true;
			authorizedCallback(authorized);
		}
	},
	
	updatePaidCache() {
		return new Promise((resolve, reject) => {
			if (true) { //若为自动续期订阅，则从苹果远程获取和更新已购项
				if (Vue.prototype.apple_user_id) {
					console.log('--> 执行 updatePaidCache()');
					//uni.showLoading({mask: true, title: this.translate('api_processing')});
					payment.plusIAPReady() //支付通道初始化
					.then((res) => {
						//console.log('--> xxx:' + JSON.stringify(res));
						//console.log('支付通道就绪，获取已购项 ...');
						//获取最新已购项
						//payment.plusIAPGetPaid(null)
						payment.plusIAPGetPaid(Vue.prototype.apple_user_id)
						.then((res) => {
							console.log('获取已购项成功!');
							//console.log('--> res：' + JSON.stringify(res));
							if (res) {
								//加密存储
								let x_res =  this.xEncrypt(JSON.stringify(res));
								this.setStorageValue('paid_content', x_res);
								uni.showModal({
									//title: '',
									confirmText: this.translate('confirm'),
									content: this.translate('msg_paid_updated'),
									showCancel: false
								});
								resolve();
							} else {
								console.log('该用户没有购买记录');
								resolve();
							}
						})
						.catch((e) => {
							console.log('获取内购记录失败：' + JSON.stringify(e));
							reject();
						});
					})
					.catch((e) => {
						console.log('支付通道初始化失败：' + JSON.stringify(e));
						reject();
					});
					//uni.hideLoading();
				} else {
					reject('用户没有正常登录，忽略远程获取已购项');
				}
			} else { //其他，从后端远程获取和更新已购项
				console.log('TODO: 从后端远程获取和更新已购项');
				//TODO: 或者改为消耗点数的类型？3 美元 30 次 PRO？ 非 demo
			}
		});
	},
	
	//检查本地缓存已购项的有效性
	checkPaidCache() {
		//检查缓存内容是否有效
		function _paid_content_valid(paid_content) {
			if (! paid_content) return false;
			let paid_content_obj = JSON.parse(paid_content);
			//console.log('--> paid_content_obj: ' + JSON.stringify(paid_content_obj));
			//console.log('--> paid_content_obj.transactionDate: ' + paid_content_obj.transactionDate);
			let paidTimeStr = paid_content_obj.transactionDate; //"2020-04-10 15:02:36"
			//let paidTime = Date.parse(paidTimeStr); //node 下有效，这里无效
			let paidTime = Date.parse(paidTimeStr.replace(' ', 'T')); //改为 ISO 格式，否则无法正常解析
			//console.log('--> paidTime:' + paidTime);
			let _now = Date.parse(new Date());
			//console.log('--> _now:' + _now);
			let delta_seconds = (_now - paidTime) / 1000;
			console.log('缓存的最后内购交易时间：' + paidTimeStr + '；权限期已使用' + delta_seconds + '秒，或' + delta_seconds/(3600) + '小时');
			let max_delta_seconds = (184 + 15 + 0.5) * 24 * 3600; //默认有效期 6 个月 + 15（宽限期） + 0.5 天（最大时区误差）
			if (delta_seconds <= max_delta_seconds) {
				return true;
			}
			return false;
		}
		
		let paid_content = this.getStorageValue('paid_content');
		if (paid_content) {
			//console.log('--> 读取的已购缓存：' + paid_content);
			paid_content = this.xDecrypt(paid_content)
			//console.log('--> 解密后的已购缓存：' + paid_content);
		}
		
		//只在已购项缓存存在且有效时才返回 true
		let result = paid_content && _paid_content_valid(paid_content) ? true: false;
		console.log('检查已购项本地缓存是否有效：' + result);
		
		return result;
	},
	
	execAppleIAP() {
		return new Promise((resolve, reject) => {
			payment.plusIAPReady(Vue.prototype.IAPOrders) //支付通道初始化
			.then((res) => {
				console.log('支付通道就绪，执行应用内购 ...');
				console.log('可购项:' + JSON.stringify(res));
				//执行应用内购
				//TODO: 让用户选择购买项
				let productid = res[0].productid;
				console.log('执行内购 1 份：' + productid);
				//由于苹果沙箱环境在频繁支付时会存在不进入回调的问题（正式环境无此问题）
				// 为便于调试，跳过支付直接使用结果
				if (false) { //跳过支付直接使用结果（！！正式版本必须改为 false）
					let res = {"payment":{"productid":"facemagi.vip.4week","quantity":"1","username":"appuname"},"transactionDate":"2020-04-10 15:02:36","transactionIdentifier":"1000000650346889","transactionReceipt":"ewoJInNpZ25hdHVyZSIgPSAiQTBRR1dlQ0FkNUh3Z......5pbmctc3RhdHVzIiA9ICIwIjsKfQ==","transactionState":"1"};
					let _msg = JSON.stringify(res);
					//let _msg = '{"aaa":"bbb"}';
					console.log('【调试】跳过支付，直接使用结果：' + _msg);
					let x_res = this.xEncrypt(_msg);
					//console.log('加密后的购买项：' + x_res);
					this.setStorageValue('paid_content', x_res);
					resolve();
				} else { //正常流程
					console.log('--> 执行购买', productid, Vue.prototype.apple_user_id);
					//uni.showLoading();
					//payment.plusIAPPay(productid)
					payment.plusIAPPay(productid, Vue.prototype.apple_user_id)
					.then((res) => {
						//console.log('内购成功：' + JSON.stringify(res));
						let x_res = this.xEncrypt(JSON.stringify(res));
						//console.log('加密后的购买项：' + x_res);
						this.setStorageValue('paid_content', x_res);
						resolve();
					})
					.catch((e) => {
						console.log('plusIAPPay() ' + JSON.stringify(e));
						reject('plusIAPPay fail');
					})
					.finally(() => { //貌似并未走到
						uni.hideLoading();
					});
				}
			})
			.catch((e) => {
				console.log('plusIAPReady() ' + JSON.stringify(e));
				uni.showModal({
					//title: '',
					confirmText: that.translate('confirm'),
					content: that.translate('error') + ' - IAPReady',
					showCancel: false
				});
				reject('plusIAPReady fail');
			});
		});
	},
	
	// --- 其他公用小函数
	
	sleep(ms) {
		return new Promise(resolve => setTimeout(resolve, ms))
	},
	/* usage:
	async function test() {
		console.log('Hello')
		await sleep(1000)
		console.log('world!')
	}
	test()
	*/
	
	getDeviceInfo() {
		let deviceInfo = null;
		//console.log('获取设备信息……');
		try {
			const res = uni.getSystemInfoSync();
			/*
			console.log('  brand:' + res.brand); //Apple
			console.log('  model:' + res.model); //iPhoneSimulator
			console.log('  pixelRatio:' + res.pixelRatio); //2
			console.log('  windowWidth:' + res.windowWidth); //375
			console.log('  windowHeight:' + res.windowHeight); //667
			console.log('  language:' + res.language); //en
			console.log('  version:' + res.version); //1.9.9.74105
			console.log('  platform:' + res.platform); //ios
			console.log('  system:' + res.system); //13.4
			*/
			deviceInfo = String(res.brand) + ',' + String(res.model) + ',' + String(res.pixelRatio) + ',' + String(res.windowWidth) + ',' + String(res.windowHeight) + ',' + String(res.language) + ',' + String(res.version) + ',' + String(res.platform) + ',' + String(res.system);
		} catch (e) {
			console.log('获取系统信息失败：', e);
		}
		//console.log('backendUserLogin() deviceInfo:' + deviceInfo);
		return deviceInfo;
	},
	
	//base64，js原生方法btoa()实现
	b64EncodeUnicode(str) {
		return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g, 
			function(match, p1) {
				return String.fromCharCode('0x' + p1);
			}));
	},
	
	zzzHash(input, hashSeed=8087, xxx=6) {
		var I64BIT_TABLE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'.split('');
		
		var hash = hashSeed;
		var i = input.length - 1;
		
		//console.log('--> input:' + input);
		if (typeof input == 'string') {
			for (; i > -1; i--) {
				hash += (hash << 5) + input.charCodeAt(i);
				//console.log('--> hash:' + String(hash) + ', i:' + input[i]);
			}
		}
		else {
			for (; i > -1; i--)
				hash += (hash << 5) + input[i];
		}
		var value = hash & 0x7FFFFFFF;
		//console.log('--> value:' + String(value));
		
		var retValue = '';
		do {
			retValue += I64BIT_TABLE[value & 0x3F];
		}
		while (value >>= xxx);
		
		return retValue;
	},
	
	setAuthHeader(headers) {
		/*
		Authorization: <type> <credentials>
		Authorization: Basic c2NhcjoxMjM0NTY= //为(scar:123456)的base64编码
		*/
		let _timestamp = this.getTimeStamp();
		let _user_id = this.getUserIdLocal();
		//console.log('--> setAuthHeader _timestamp:' + _timestamp);
		//console.log('--> setAuthHeader _user_id:' + _user_id);
		//console.log('--> setAuthHeader zzzHash:' + this.zzzHash(_user_id + String(_timestamp)))
		let credentials = this.b64EncodeUnicode(_user_id + ':' +  this.zzzHash(_user_id + String(_timestamp)));
		headers["Authorization"] = "Basic " + credentials;
		return headers;
	},
	
	getUserIdLocal() {
		return uni.getStorageSync('user_id');
	},
	
	//AES 加解密
	xEncrypt(message) { //加密
		//DES/AES切换只需要修改 CryptoJS.AES <=> CryptoJS.DES
		var aseKey = "11" + "80" + "87" + "01"; //秘钥必须为：8/16/32位
		var encrypt = CryptoJS.AES.encrypt(message, CryptoJS.enc.Utf8.parse(aseKey), {
			mode: CryptoJS.mode.ECB,
			padding: CryptoJS.pad.Pkcs7
		}).toString();
		return encrypt;
	},
	xDecrypt(encrypt) { //解密
		var aseKey = "11" + "80" + "87" + "01"; //秘钥必须为：8/16/32位
		var decrypt = CryptoJS.AES.decrypt(encrypt, CryptoJS.enc.Utf8.parse(aseKey), {
			mode: CryptoJS.mode.ECB,
			padding: CryptoJS.pad.Pkcs7
		}).toString(CryptoJS.enc.Utf8);
		return decrypt;
	},
	
	exitApp() {
		// #ifdef APP-PLUS
		plus.os.name == "Android" ? plus.runtime.quit() : plus.ios.import("UIApplication").sharedApplication().performSelector("exit");
		// #endif
	},
	
	isString(obj) { //判断对象是否是字符串
	  return Object.prototype.toString.call(obj) === "[object String]";
	},
	
	//调用 i18n 翻译，用于 script 中
	translate(e) {
		return Vue.prototype._i18n.messages[Vue.prototype._i18n.locale].index[e];
	}
	
};
