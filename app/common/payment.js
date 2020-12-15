//----- 苹果内购相关函数 -----
// 参考官方社区文档：https://ask.dcloud.net.cn/article/497
// 注意：HBuilder 里的调试基座默认不带IAP支付通道，如果需要调试IAP需要使用开发证书生成一个自定义调试基座，用来实现IAP的开发和调试。

import Vue from 'vue';

var iapChannel = null;

/* 购买商品接口使用方法
1、首先调用plus.payment.getChannels获取支付通道，IAP支付通道的ID为“appleiap”；
2、调用ID为“appleiap”的PaymentChannel对象的requestOrder方法，向Appstore请求有效的商品详情。注意：IAP支付必须在调用payment.request方法之前调用requestOrder方法，否则将会报错。
3、调用plus.payment.request方法发起支付请求，传入statement的参数为JSON对象，可以设置如下参数
   productid String（必选）要支付的商品的标识（必须是调用requestOrder返回的有效的商品标识）
   username String（可选）购买商品用户的用户名
   quantity String（可选）购买商品的数量，如果不填写默认为1
*/

// 获取支付通道
function plusIAPReady(IAPOrders) { //uni-app中将此function里的代码放入vue页面的onLoad生命周期中
	return new Promise((resolve, reject) => {
		// #ifdef APP-PLUS
		uni.showLoading();
		plus.payment.getChannels(function(channels) {
			//console.log('获取 IAP 支付通道，IAPOrders：' + IAPOrders);
			for (var i in channels) {
				//console.log('--> channel:' + i + ',' + channels[i].id)
				if (channels[i].id == 'appleiap') {
					iapChannel = channels[i];
					if (IAPOrders) {
						uni.hideLoading();
						uni.showLoading();
						iapChannel.requestOrder(IAPOrders, function(event) {
							console.log("获取 IAPOrders 成功！");
							//for (var index in event) {
							//	var OrderItem = event[index];
							//	console.log("Title:" + OrderItem.title + ", Price:" + OrderItem.price + ", Description:" + OrderItem.description + ", ProductID:" + OrderItem.productid);
							//}
							uni.hideLoading();
							resolve(event);
						}, function(e) {
							console.log("获取 IAPOrders 失败：" + JSON.stringify(e));
							uni.hideLoading();
							reject({code: -2});
						});
					} else {
						console.log('获取 IAP 支付通道成功');
						uni.hideLoading();
						resolve(iapChannel);
					}
				}
			}
		}, function(e) {
			console.log("获取 IAP 支付通道失败：" + JSON.stringify(e));
			uni.hideLoading();
			reject({code: -1});
		});
		// #endif
		
		// #ifndef APP-PLUS
		//console.log('本环境不支持该函数！');
		reject({code: -1, err: "This function is not supported in this environment!"});
		// #endif
	});
}
//document.addEventListener('plusready', plusReady, false); //uni-app不需要此代码

//  发起IAP应用内自购
function plusIAPPay(productid, username='appuname') {
	return new Promise((resolve, reject) => {
		// #ifdef APP-PLUS
		uni.showLoading();
		//plus.nativeUI.showWaiting('', {style:"black",background:"rgba(0,0,0,0)"});
		//setTimeout(() => { //如果用户在支付时选择取消，则不走下述两个回调，所以定时关闭
		//	uni.hideLoading();
		//}, 5000);
		plus.payment.request(iapChannel, {
			"productid": productid,
			"username": username,
			"quantity": 1
		}, function(res) {
			console.log('用户 ' + username + ' 购买 ' + productid + ' 成功！');
			let productId = res.payment.productid; //商品id  
			let transactionId = res.transactionIdentifier; //订单号  
			let receiptData = res.transactionReceipt; //苹果返回唯一凭证
			//console.log('返回信息：' + JSON.stringify(res));
			//返回信息：{"payment":{"productid":"facemagi.pro.subscription.1month","quantity":"1","username":"001141.e2e2372eaa554136b3de658485d31d5a.1027"},"transactionDate":"2020-05-05 23:29:51","transactionIdentifier":"1000000660442220","transactionReceipt":"ewoJInNpZ25hdHVyZSIgPSAiQTFsbFFLcVpLWEIrcUJhL1pBak5idXFiTFloczgwa043dGE0ODlRMllkR2tQNTNVL2dTYmdJckFGMk1KTUZDMXdOazgrUFdTbGlNYkpRTlowQXpHM0sybmpneHptWGR3QVl3cTJqMEJNR2tyZUhQdi9wUndSaDAxanZmbGNRWjRsS0F6cit6ZEMrN2k0ZDV6WHk5RkRFT0J5eXYxQytGN2RZUzJiMEVYK0VTeFRLQXFMV2NFMEtDN0VkSGxrcWV2dmtyVjdONUx5RWk2ZHRBVDRsZUx2bWhIV3ZVUDVxRHpDNlhscXdDeTcyMVFxYVAwU2FTVmNXNVNadStJUWFJVzJjQk1zQUlyV2hma0QwaGc4VFNBN3dDdnhkTlRaVDBXUURxRGljTjF1dzVpaFRMNTdKSzVBZ3hqaUNackZ5SEdrQ2g5ekgrM1VTaThnd0tEOVJ5QjNjd0FBQVdBTUlJRmZEQ0NCR1NnQXdJQkFnSUlEdXRYaCtlZUNZMHdEUVlKS29aSWh2Y05BUUVGQlFBd2daWXhDekFKQmdOVkJBWVRBbFZUTVJNd0VRWURWUVFLREFwQmNIQnNaU0JKYm1NdU1Td3dLZ1lEVlFRTERDTkJjSEJzWlNCWGIzSnNaSGRwWkdVZ1JHVjJaV3h2Y0dWeUlGSmxiR0YwYVc5dWN6RkVNRUlHQTFVRUF3dzdRWEJ3YkdVZ1YyOXliR1IzYVdSbElFUmxkbVZzYjNCbGNpQlNaV3hoZEdsdmJuTWdRMlZ5ZEdsbWFXTmhkR2x2YmlCQmRYUm9iM0pwZEhrd0hoY05NVFV4TVRFek1ESXhOVEE1V2hjTk1qTXdNakEzTWpFME9EUTNXakNCaVRFM01EVUdBMVVFQXd3dVRXRmpJRUZ3Y0NCVGRHOXlaU0JoYm1RZ2FWUjFibVZ6SUZOMGIzSmxJRkpsWTJWcGNIUWdVMmxuYm1sdVp6RXNNQ29HQTFVRUN3d2pRWEJ3YkdVZ1YyOXliR1IzYVdSbElFUmxkbVZzYjNCbGNpQlNaV3hoZEdsdmJuTXhFekFSQmdOVkJBb01Da0Z3Y0d4bElFbHVZeTR4Q3pBSkJnTlZCQVlUQWxWVE1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBcGMrQi9TV2lnVnZXaCswajJqTWNqdUlqd0tYRUpzczl4cC9zU2cxVmh2K2tBdGVYeWpsVWJYMS9zbFFZbmNRc1VuR09aSHVDem9tNlNkWUk1YlNJY2M4L1cwWXV4c1FkdUFPcFdLSUVQaUY0MWR1MzBJNFNqWU5NV3lwb041UEM4cjBleE5LaERFcFlVcXNTNCszZEg1Z1ZrRFV0d3N3U3lvMUlnZmRZZUZScjZJd3hOaDlLQmd4SFZQTTNrTGl5a29sOVg2U0ZTdUhBbk9DNnBMdUNsMlAwSzVQQi9UNXZ5c0gxUEttUFVockFKUXAyRHQ3K21mNy93bXYxVzE2c2MxRkpDRmFKekVPUXpJNkJBdENnbDdaY3NhRnBhWWVRRUdnbUpqbTRIUkJ6c0FwZHhYUFEzM1k3MkMzWmlCN2o3QWZQNG83UTAvb21WWUh2NGdOSkl3SURBUUFCbzRJQjF6Q0NBZE13UHdZSUt3WUJCUVVIQVFFRU16QXhNQzhHQ0NzR0FRVUZCekFCaGlOb2RIUndPaTh2YjJOemNDNWhjSEJzWlM1amIyMHZiMk56Y0RBekxYZDNaSEl3TkRBZEJnTlZIUTRFRmdRVWthU2MvTVIydDUrZ2l2Uk45WTgyWGUwckJJVXdEQVlEVlIwVEFRSC9CQUl3QURBZkJnTlZIU01FR0RBV2dCU0lKeGNKcWJZWVlJdnM2N3IyUjFuRlVsU2p0ekNDQVI0R0ExVWRJQVNDQVJVd2dnRVJNSUlCRFFZS0tvWklodmRqWkFVR0FUQ0IvakNCd3dZSUt3WUJCUVVIQWdJd2diWU1nYk5TWld4cFlXNWpaU0J2YmlCMGFHbHpJR05sY25ScFptbGpZWFJsSUdKNUlHRnVlU0J3WVhKMGVTQmhjM04xYldWeklHRmpZMlZ3ZEdGdVkyVWdiMllnZEdobElIUm9aVzRnWVhCd2JHbGpZV0pzWlNCemRHRnVaR0Z5WkNCMFpYSnRjeUJoYm1RZ1kyOXVaR2wwYVc5dWN5QnZaaUIxYzJVc0lHTmxjblJwWm1sallYUmxJSEJ2YkdsamVTQmhibVFnWTJWeWRHbG1hV05oZEdsdmJpQndjbUZqZEdsalpTQnpkR0YwWlcxbGJuUnpMakEyQmdnckJnRUZCUWNDQVJZcWFIUjBjRG92TDNkM2R5NWhjSEJzWlM1amIyMHZZMlZ5ZEdsbWFXTmhkR1ZoZFhSb2IzSnBkSGt2TUE0R0ExVWREd0VCL3dRRUF3SUhnREFRQmdvcWhraUc5Mk5rQmdzQkJBSUZBREFOQmdrcWhraUc5dzBCQVFVRkFBT0NBUUVBRGFZYjB5NDk0MXNyQjI1Q2xtelQ2SXhETUlKZjRGelJqYjY5RDcwYS9DV1MyNHlGdzRCWjMrUGkxeTRGRkt3TjI3YTQvdncxTG56THJSZHJqbjhmNUhlNXNXZVZ0Qk5lcGhtR2R2aGFJSlhuWTR3UGMvem83Y1lmcnBuNFpVaGNvT0FvT3NBUU55MjVvQVE1SDNPNXlBWDk4dDUvR2lvcWJpc0IvS0FnWE5ucmZTZW1NL2oxbU9DK1JOdXhUR2Y4YmdwUHllSUdxTktYODZlT2ExR2lXb1IxWmRFV0JHTGp3Vi8xQ0tuUGFObVNBTW5CakxQNGpRQmt1bGhnd0h5dmozWEthYmxiS3RZZGFHNllRdlZNcHpjWm04dzdISG9aUS9PamJiOUlZQVlNTnBJcjdONFl0UkhhTFNQUWp2eWdhWndYRzU2QWV6bEhSVEJoTDhjVHFBPT0iOwoJInB1cmNoYXNlLWluZm8iID0gImV3b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ESXdMVEExTFRBMUlEQTRPakk1T2pVeUlFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW5GMVlXNTBhWFI1SWlBOUlDSXhJanNLQ1NKemRXSnpZM0pwY0hScGIyNHRaM0p2ZFhBdGFXUmxiblJwWm1sbGNpSWdQU0FpTWpBMk16SXdPVFlpT3dvSkluVnVhWEYxWlMxMlpXNWtiM0l0YVdSbGJuUnBabWxsY2lJZ1BTQWlOakpGUVVZM01FSXRPRGczUWkwME5UY3dMVUV4TXpFdFJqTXpOamt3TkVKR09UUTVJanNLQ1NKdmNtbG5hVzVoYkMxd2RYSmphR0Z6WlMxa1lYUmxMVzF6SWlBOUlDSXhOVGc0TmpreU5Ua3lOVE01SWpzS0NTSmxlSEJwY21WekxXUmhkR1V0Wm05eWJXRjBkR1ZrSWlBOUlDSXlNREl3TFRBMUxUQTFJREUxT2pNME9qVXhJRVYwWXk5SFRWUWlPd29KSW1sekxXbHVMV2x1ZEhKdkxXOW1abVZ5TFhCbGNtbHZaQ0lnUFNBaVptRnNjMlVpT3dvSkluQjFjbU5vWVhObExXUmhkR1V0YlhNaUlEMGdJakUxT0RnMk9USTFPVEUyTWpBaU93b0pJbVY0Y0dseVpYTXRaR0YwWlMxbWIzSnRZWFIwWldRdGNITjBJaUE5SUNJeU1ESXdMVEExTFRBMUlEQTRPak0wT2pVeElFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW1sekxYUnlhV0ZzTFhCbGNtbHZaQ0lnUFNBaVptRnNjMlVpT3dvSkltbDBaVzB0YVdRaUlEMGdJakUxTVRFM05UZ3pNVGNpT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0pqWmpoa1lUTTRPVGt3Tnprd056Tm1aVFEwTlRZMFpHWTFZemRqTkRGak5EazRZbUprWlRVeUlqc0tDU0p2Y21sbmFXNWhiQzEwY21GdWMyRmpkR2x2YmkxcFpDSWdQU0FpTVRBd01EQXdNRFkyTURRME1qSXlNQ0k3Q2draVpYaHdhWEpsY3kxa1lYUmxJaUE5SUNJeE5UZzROamt5T0RreE5qSXdJanNLQ1NKMGNtRnVjMkZqZEdsdmJpMXBaQ0lnUFNBaU1UQXdNREF3TURZMk1EUTBNakl5TUNJN0Nna2lZblp5Y3lJZ1BTQWlNakF3TlRBME1Ua2lPd29KSW5kbFlpMXZjbVJsY2kxc2FXNWxMV2wwWlcwdGFXUWlJRDBnSWpFd01EQXdNREF3TlRJeU5EazFOek1pT3dvSkluWmxjbk5wYjI0dFpYaDBaWEp1WVd3dGFXUmxiblJwWm1sbGNpSWdQU0FpTUNJN0Nna2lZbWxrSWlBOUlDSjFibWt1VlU1Sk1UQTFNRFE0UkNJN0Nna2ljSEp2WkhWamRDMXBaQ0lnUFNBaVptRmpaVzFoWjJrdWNISnZMbk4xWW5OamNtbHdkR2x2Ymk0eGJXOXVkR2dpT3dvSkluQjFjbU5vWVhObExXUmhkR1VpSUQwZ0lqSXdNakF0TURVdE1EVWdNVFU2TWprNk5URWdSWFJqTDBkTlZDSTdDZ2tpY0hWeVkyaGhjMlV0WkdGMFpTMXdjM1FpSUQwZ0lqSXdNakF0TURVdE1EVWdNRGc2TWprNk5URWdRVzFsY21sallTOU1iM05mUVc1blpXeGxjeUk3Q2draWIzSnBaMmx1WVd3dGNIVnlZMmhoYzJVdFpHRjBaU0lnUFNBaU1qQXlNQzB3TlMwd05TQXhOVG95T1RvMU1pQkZkR012UjAxVUlqc0tmUT09IjsKCSJlbnZpcm9ubWVudCIgPSAiU2FuZGJveCI7CgkicG9kIiA9ICIxMDAiOwoJInNpZ25pbmctc3RhdHVzIiA9ICIwIjsKfQ==","transactionState":"1"}
			uni.hideLoading();
			//plus.nativeUI.closeWaiting();
			resolve(res);
		}, function(e) {
			//plus.nativeUI.alert("更多错误信息请参考支付(Payment)规范文档：http://www.html5plus.org/#specification#/specification/Payment.html", null, "支付失败：" + e.code);
			console.log("IAP 支付失败：" + JSON.stringify(e));
			uni.hideLoading();
			//plus.nativeUI.closeWaiting();
			reject({code: -1});
		});
		/*
		//无效，无支付界面调出来（另外，据说只返回是否成功，无购买凭证）
		uni.requestPayment({
			provider: 'appleiap',
			orderInfo: {
				productid: productid,
				username: username,
				quantity: 1
			},
			success: (res) => {
				resolve(res);
			},
			fail: (e) => {
				reject({code: -1, err: e});
			},
			complete: () => {
				console.log("payment结束");
				uni.hideLoading();
			}
		});
		*/
		// #endif
		
		// #ifndef APP-PLUS
		//console.log('本环境不支持该函数！');
		reject({code: -1, err: "This function is not supported in this environment!"});
		// #endif
	});
}

/* 恢复已购项目接口使用方法
1、首先调用plus.payment.getChannels获取支付通道，IAP支付通道的ID为“appleiap”
2、调用ID为“appleiap”的PaymentChannel对象的restoreComplateRequest方法
*/

function plusIAPGetPaid(username='appuname') {
	//注意：有些文章说，只有 Auto-renewable subscriptions（续期订阅）和 Non-consumable products（非消耗性）可以做恢复
	//应用中如果使用的是消耗性购买项，则只能在完成内购时保存本地，无法使用这里的恢复购买项功能
	return new Promise((resolve, reject) => {
		function getLastTransaction(trancs) {
			console.log("trancs.length:" + trancs.length);
			if (trancs.length == 0) {
				return null;
			}
			let _trancDate = "2020-01-01 00:00:00";
			let _trancIndex = -1;
			for(let i = 0; i < trancs.length; i++) {
				let transactionState = trancs[i].transactionState;
				let payment = trancs[i].payment; //商品信息
				let transactionIdentifier = trancs[i].transactionIdentifier; //购买商品的交易订单标识
				let transactionDate = trancs[i].transactionDate; //购买商品的交易日期
				console.log("i:" + i + " 商品信息：" + JSON.stringify(payment) + "，状态：" + transactionState + "，订单标识：" + transactionIdentifier + "，交易日期：" + transactionDate); // 交易状态可取值："1"为支付成功；"2"为支付失败；"3"为支付已恢复。多为1/3。
				if (trancs[i].transactionDate > _trancDate) {
					_trancDate = trancs[i].transactionDate;
					_trancIndex = i;
				}
			}
			//uni.hideLoading();
			//只返回交易日期最近的一笔
			let ret_tranc = trancs[trancs.length-1];
			if (_trancIndex >= 0) {
				ret_tranc = trancs[_trancIndex];
			}
			console.log("返回最近的一笔交易：" + JSON.stringify(ret_tranc.payment) + "，状态：" + ret_tranc.transactionState + "，交易日期：" + ret_tranc.transactionDate);
			return ret_tranc;
		}
		
		// #ifdef APP-PLUS
		uni.showLoading({mask: false, title: translate("msg_paid_updating")});
		console.log("获取已购项... iapChannel:" + JSON.stringify(iapChannel) + ", username:" + JSON.stringify(username));
		iapChannel.restoreComplateRequest({
			"username": username // 这个 username 可以随意内部指定，无需为苹果账号信息？
		}, function(trancs) {
			//console.log("获取已购项目成功：" + JSON.stringify(trancs));
			uni.hideLoading();
			resolve(getLastTransaction(trancs));
		}, function(e) {
			console.log("获取已购项目失败：" + JSON.stringify(e));
			uni.hideLoading();
			reject({code: -1});
		});
		//【示例数据】获取已购项目成功：
		//let trancs = [{"payment":{"productid":"facemagi.pro.subscription.6months","quantity":"1"},"transactionDate":"2020-05-06 15:50:09","transactionIdentifier":"1000000661405836","transactionReceipt":"ewoJInNpZ25hdHVyZSIgPSAiQXl1c0xjSTFGZ3hOTGZkWmdTajFOcXNBSURyZGlXZVNHZGRGMUlKUXpZbnRscXcwUklGbUFiNlRMaGs2RnFRR3VkcGE3R2haR1FTcXlyRUhUS1oxQ1ZEL0FBeWl0UWhmWWdLTVAvRGJGODFhMGlWVzMwc0taSEZlV0NRVFZjRTRwaUY3dEVYamRFVjRFSUg1RG9UM3hBZzJJcDVOMkQrZHh0Z1dTdjBmWktWNVJYYjB2ZHErUTFQNnJKT2FmclJDS3IrVXRoWmtTbnhYRnNsTTJCNzhPUHpBSmM5ZEt2TDNqdHdiUEhtTVA3T2FKS2tndThNUEtKL1BvWDdONitQWFZMcHJNczNVcCtFcnE3OFcvRGp6RGRITVhsR0ZvOG9zNXA5NUltbDFQWnhRTUNHMlZYRFBHVDNtTjk0b1RoT2ZzcStKSmtoa3g5a29Ja0NTZEY0YXg2QUFBQVdBTUlJRmZEQ0NCR1NnQXdJQkFnSUlEdXRYaCtlZUNZMHdEUVlKS29aSWh2Y05BUUVGQlFBd2daWXhDekFKQmdOVkJBWVRBbFZUTVJNd0VRWURWUVFLREFwQmNIQnNaU0JKYm1NdU1Td3dLZ1lEVlFRTERDTkJjSEJzWlNCWGIzSnNaSGRwWkdVZ1JHVjJaV3h2Y0dWeUlGSmxiR0YwYVc5dWN6RkVNRUlHQTFVRUF3dzdRWEJ3YkdVZ1YyOXliR1IzYVdSbElFUmxkbVZzYjNCbGNpQlNaV3hoZEdsdmJuTWdRMlZ5ZEdsbWFXTmhkR2x2YmlCQmRYUm9iM0pwZEhrd0hoY05NVFV4TVRFek1ESXhOVEE1V2hjTk1qTXdNakEzTWpFME9EUTNXakNCaVRFM01EVUdBMVVFQXd3dVRXRmpJRUZ3Y0NCVGRHOXlaU0JoYm1RZ2FWUjFibVZ6SUZOMGIzSmxJRkpsWTJWcGNIUWdVMmxuYm1sdVp6RXNNQ29HQTFVRUN3d2pRWEJ3YkdVZ1YyOXliR1IzYVdSbElFUmxkbVZzYjNCbGNpQlNaV3hoZEdsdmJuTXhFekFSQmdOVkJBb01Da0Z3Y0d4bElFbHVZeTR4Q3pBSkJnTlZCQVlUQWxWVE1JSUJJakFOQmdrcWhraUc5dzBCQVFFRkFBT0NBUThBTUlJQkNnS0NBUUVBcGMrQi9TV2lnVnZXaCswajJqTWNqdUlqd0tYRUpzczl4cC9zU2cxVmh2K2tBdGVYeWpsVWJYMS9zbFFZbmNRc1VuR09aSHVDem9tNlNkWUk1YlNJY2M4L1cwWXV4c1FkdUFPcFdLSUVQaUY0MWR1MzBJNFNqWU5NV3lwb041UEM4cjBleE5LaERFcFlVcXNTNCszZEg1Z1ZrRFV0d3N3U3lvMUlnZmRZZUZScjZJd3hOaDlLQmd4SFZQTTNrTGl5a29sOVg2U0ZTdUhBbk9DNnBMdUNsMlAwSzVQQi9UNXZ5c0gxUEttUFVockFKUXAyRHQ3K21mNy93bXYxVzE2c2MxRkpDRmFKekVPUXpJNkJBdENnbDdaY3NhRnBhWWVRRUdnbUpqbTRIUkJ6c0FwZHhYUFEzM1k3MkMzWmlCN2o3QWZQNG83UTAvb21WWUh2NGdOSkl3SURBUUFCbzRJQjF6Q0NBZE13UHdZSUt3WUJCUVVIQVFFRU16QXhNQzhHQ0NzR0FRVUZCekFCaGlOb2RIUndPaTh2YjJOemNDNWhjSEJzWlM1amIyMHZiMk56Y0RBekxYZDNaSEl3TkRBZEJnTlZIUTRFRmdRVWthU2MvTVIydDUrZ2l2Uk45WTgyWGUwckJJVXdEQVlEVlIwVEFRSC9CQUl3QURBZkJnTlZIU01FR0RBV2dCU0lKeGNKcWJZWVlJdnM2N3IyUjFuRlVsU2p0ekNDQVI0R0ExVWRJQVNDQVJVd2dnRVJNSUlCRFFZS0tvWklodmRqWkFVR0FUQ0IvakNCd3dZSUt3WUJCUVVIQWdJd2diWU1nYk5TWld4cFlXNWpaU0J2YmlCMGFHbHpJR05sY25ScFptbGpZWFJsSUdKNUlHRnVlU0J3WVhKMGVTQmhjM04xYldWeklHRmpZMlZ3ZEdGdVkyVWdiMllnZEdobElIUm9aVzRnWVhCd2JHbGpZV0pzWlNCemRHRnVaR0Z5WkNCMFpYSnRjeUJoYm1RZ1kyOXVaR2wwYVc5dWN5QnZaaUIxYzJVc0lHTmxjblJwWm1sallYUmxJSEJ2YkdsamVTQmhibVFnWTJWeWRHbG1hV05oZEdsdmJpQndjbUZqZEdsalpTQnpkR0YwWlcxbGJuUnpMakEyQmdnckJnRUZCUWNDQVJZcWFIUjBjRG92TDNkM2R5NWhjSEJzWlM1amIyMHZZMlZ5ZEdsbWFXTmhkR1ZoZFhSb2IzSnBkSGt2TUE0R0ExVWREd0VCL3dRRUF3SUhnREFRQmdvcWhraUc5Mk5rQmdzQkJBSUZBREFOQmdrcWhraUc5dzBCQVFVRkFBT0NBUUVBRGFZYjB5NDk0MXNyQjI1Q2xtelQ2SXhETUlKZjRGelJqYjY5RDcwYS9DV1MyNHlGdzRCWjMrUGkxeTRGRkt3TjI3YTQvdncxTG56THJSZHJqbjhmNUhlNXNXZVZ0Qk5lcGhtR2R2aGFJSlhuWTR3UGMvem83Y1lmcnBuNFpVaGNvT0FvT3NBUU55MjVvQVE1SDNPNXlBWDk4dDUvR2lvcWJpc0IvS0FnWE5ucmZTZW1NL2oxbU9DK1JOdXhUR2Y4YmdwUHllSUdxTktYODZlT2ExR2lXb1IxWmRFV0JHTGp3Vi8xQ0tuUGFObVNBTW5CakxQNGpRQmt1bGhnd0h5dmozWEthYmxiS3RZZGFHNllRdlZNcHpjWm04dzdISG9aUS9PamJiOUlZQVlNTnBJcjdONFl0UkhhTFNQUWp2eWdhWndYRzU2QWV6bEhSVEJoTDhjVHFBPT0iOwoJInB1cmNoYXNlLWluZm8iID0gImV3b0pJbTl5YVdkcGJtRnNMWEIxY21Ob1lYTmxMV1JoZEdVdGNITjBJaUE5SUNJeU1ESXdMVEExTFRBMUlEQTRPakk1T2pVeUlFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW5GMVlXNTBhWFI1SWlBOUlDSXhJanNLQ1NKemRXSnpZM0pwY0hScGIyNHRaM0p2ZFhBdGFXUmxiblJwWm1sbGNpSWdQU0FpTWpBMk16SXdPVFlpT3dvSkluVnVhWEYxWlMxMlpXNWtiM0l0YVdSbGJuUnBabWxsY2lJZ1BTQWlPVUU1TmtGRlJFUXRNa1l3T0MwME1EUXpMVGd6UVRBdFJEWkdSa1JHUkROQ01EVkdJanNLQ1NKdmNtbG5hVzVoYkMxd2RYSmphR0Z6WlMxa1lYUmxMVzF6SWlBOUlDSXhOVGc0TmpreU5Ua3lNREF3SWpzS0NTSmxlSEJwY21WekxXUmhkR1V0Wm05eWJXRjBkR1ZrSWlBOUlDSXlNREl3TFRBMUxUQTJJREE0T2pJd09qQTVJRVYwWXk5SFRWUWlPd29KSW1sekxXbHVMV2x1ZEhKdkxXOW1abVZ5TFhCbGNtbHZaQ0lnUFNBaVptRnNjMlVpT3dvSkluQjFjbU5vWVhObExXUmhkR1V0YlhNaUlEMGdJakUxT0RnM05URTBNRGt3TURBaU93b0pJbVY0Y0dseVpYTXRaR0YwWlMxbWIzSnRZWFIwWldRdGNITjBJaUE5SUNJeU1ESXdMVEExTFRBMklEQXhPakl3T2pBNUlFRnRaWEpwWTJFdlRHOXpYMEZ1WjJWc1pYTWlPd29KSW1sekxYUnlhV0ZzTFhCbGNtbHZaQ0lnUFNBaVptRnNjMlVpT3dvSkltbDBaVzB0YVdRaUlEMGdJakUxTVRFNE9EZzROVGdpT3dvSkluVnVhWEYxWlMxcFpHVnVkR2xtYVdWeUlpQTlJQ0pqWmpoa1lUTTRPVGt3Tnprd056Tm1aVFEwTlRZMFpHWTFZemRqTkRGak5EazRZbUprWlRVeUlqc0tDU0p2Y21sbmFXNWhiQzEwY21GdWMyRmpkR2x2YmkxcFpDSWdQU0FpTVRBd01EQXdNRFkyTURRME1qSXlNQ0k3Q2draVpYaHdhWEpsY3kxa1lYUmxJaUE5SUNJeE5UZzROelV6TWpBNU1EQXdJanNLQ1NKMGNtRnVjMkZqZEdsdmJpMXBaQ0lnUFNBaU1UQXdNREF3TURZMk1UUXdOVGd6TmlJN0Nna2lZblp5Y3lJZ1BTQWlNakF3TlRBME1Ua2lPd29KSW5kbFlpMXZjbVJsY2kxc2FXNWxMV2wwWlcwdGFXUWlJRDBnSWpFd01EQXdNREF3TlRJeU5qUTNOemtpT3dvSkluWmxjbk5wYjI0dFpYaDBaWEp1WVd3dGFXUmxiblJwWm1sbGNpSWdQU0FpTUNJN0Nna2lZbWxrSWlBOUlDSjFibWt1VlU1Sk1UQTFNRFE0UkNJN0Nna2ljSEp2WkhWamRDMXBaQ0lnUFNBaVptRmpaVzFoWjJrdWNISnZMbk4xWW5OamNtbHdkR2x2Ymk0MmJXOXVkR2h6SWpzS0NTSndkWEpqYUdGelpTMWtZWFJsSWlBOUlDSXlNREl3TFRBMUxUQTJJREEzT2pVd09qQTVJRVYwWXk5SFRWUWlPd29KSW5CMWNtTm9ZWE5sTFdSaGRHVXRjSE4wSWlBOUlDSXlNREl3TFRBMUxUQTJJREF3T2pVd09qQTVJRUZ0WlhKcFkyRXZURzl6WDBGdVoyVnNaWE1pT3dvSkltOXlhV2RwYm1Gc0xYQjFjbU5vWVhObExXUmhkR1VpSUQwZ0lqSXdNakF0TURVdE1EVWdNVFU2TWprNk5USWdSWFJqTDBkTlZDSTdDbjA9IjsKCSJlbnZpcm9ubWVudCIgPSAiU2FuZGJveCI7CgkicG9kIiA9ICIxMDAiOwoJInNpZ25pbmctc3RhdHVzIiA9ICIwIjsKfQ==","transactionState":"3"}];
		//resolve(getLastTransaction(trancs));
		// #endif
		
		// #ifndef APP-PLUS
		//console.log('本环境不支持该函数！');
		reject({code: -1, err: "This function is not supported in this environment!"});
		// #endif
	});
}

//调用 i18n 翻译，用于 script 中
function translate(e) {
	return Vue.prototype._i18n.messages[Vue.prototype._i18n.locale].index[e];
}

module.exports = {
	plusIAPReady: plusIAPReady,
	plusIAPPay: plusIAPPay,
	plusIAPGetPaid: plusIAPGetPaid,
}
