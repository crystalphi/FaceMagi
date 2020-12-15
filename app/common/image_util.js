
async function compressImage(src, platform) {
	const imageInfo = await getImageInfo(src);
	const orientation = imageInfo.orientation;
	let rotate = 0;
	let quality = 90;
	
	if (platform === 'ios') {
		rotate = 0;
		//quality = 25;
	} else {
		switch (orientation) {
			case 'up': //exif:1 不旋转
				rotate = 0;
				break;
			case 'down': //exif:3 旋转180度
				rotate = 180;
				break;
			case 'right': //exif:6 旋转90度
				rotate = 90;
				break;
			case 'left': //exif:8 旋转270度
				rotate = 270;
				break;
			default:
				rotate = 0;
				break;
		}
	}
	
	console.log('orientation: ' + orientation + '; rotate: ' + rotate);
	console.log('imageInfo.width:' + imageInfo.width);
	let _width = 'auto';
	if (imageInfo.width > 800) {
		_width = String(parseInt((800 / imageInfo.width) * 100)) + '%';
	}
	console.log('_width:' + _width);
	
	return new Promise(function(resolve, reject) {
		plus.zip.compressImage({
			src: src,
			dst: "_doc/uniapp_temp" + '/compressed/' + Math.round(new Date()) + '.jpg',
			format: 'jpg',
			quality: quality,
			width: _width, //'auto', 'xx%'
			//width: '800px', //这里指定宽度
			overwrite: true,
			//height: 'auto',
			rotate: rotate
		},
		function(event) {
			let tempPath = event.target;
			//console.log('--> tempPath: ' + tempPath);
			plus.io.resolveLocalFileSystemURL(tempPath, function(entry) {
				// 获取文件大小
				entry.getMetadata(function(metadata){
					console.log("文件大小：" + metadata.size);
				}, function(e) {
					console.log("获取文件信息失败：" + e.message);
				}, false);
			}, function(e) {
				console.log("读取文件错误：" + e.message);
			});
			resolve(tempPath);
		},
		function(error) {
			reject(error);
		});
	});
}

function getImageInfo(path) {
	return new Promise(function(resolve, reject) {
		// #ifdef APP-PLUS
		plus.io.getImageInfo({
			src: path,
			success: function(image) {
				// console.log(image.width);
				// console.log(image.height);
				// console.log('orientation=' + image.orientation);
				// console.log('path=' + image.path);
				resolve(image)
			},
			fail: function(err) {
				console.log("getImageInfoErr: " + JSON.stringify(err));
				reject(err)
			}
		});
		// #endif
		// #ifdef H5 || MP-WEIXIN	
		uni.getImageInfo({
			src: path,
			success: function(image) {
				// console.log(image.width);
				// console.log(image.height);
				// console.log('orientation=' + image.orientation);
				// console.log('path=' + image.path);
				resolve(image)
			},
			fail: function(err) {
				console.log("getImageInfoErr: " + JSON.stringify(err));
				reject(err)
			}
		});
		// #endif
	});
}

export default compressImage