/*
对选中的图片进行压缩旋转处理
*/

//import Exif from '@/common/exif.min.js'
import Exif from '@/common/exif.js'


const imageCompress = async (opt) => {
	let maxWidth = 800; //压缩图片最大宽度  
	opt = opt || {};
	opt.url = opt.url || '';
	opt.success = opt.success || function() {};
	//console.log(opt.url)
	let Orientation = 1;
	//获取图片META信息
	await getImageTag(opt.url, 'Orientation', function(e) {
		if (e != undefined) Orientation = e;
	})
	var img = null;
	var canvas = null;
	await compressImage(opt.url, maxWidth, function(e) {
		img = e.img;
		canvas = e.canvas;
	})

	console.log('image orientation:', Orientation)
	let baseStr = '';
	//如果方向角不为1，都需要进行旋转  
	switch (Orientation) {
		case 6: //需要顺时针（向右）90度旋转  
			console.log('rotate 90. right');
			baseStr = rotateImg(img, 'right', canvas);
			break;
		case 8: //需要逆时针（向左）90度旋转  
			console.log('rotate 90. left');
			baseStr = rotateImg(img, 'left', canvas);
			break;
		case 3: //需要180度旋转 转两次  
			console.log('rotate 180.');
			baseStr = rotateImg(img, 'right', canvas, 2);
			break;
		default:
			baseStr = rotateImg(img, '', canvas);
			break;
	}
	opt.success(baseStr); //公共方法的回调函数  
}

const compressImage = async (imgSrc, maxWidth, func) => {
	if (!imgSrc) return 0;
	return new Promise((resolve, reject) => {
		uni.getImageInfo({
			src: imgSrc,
			success(res) {
				let img = new Image();
				//let img = document.createElement("img")
				img.src = res.path;
				//console.log(img)
				let canvas = document.createElement('canvas');
				let obj = new Object();
				obj.img = img;
				obj.canvas = canvas;
				resolve(func(obj));
			}
		});
	})
}

/**  
 * @desc 获取图片信息，使用exif.js库，具体用法请在github中搜索  
 * @param {Object} file 上传的图片文件  
 * @param {String} tag 需要获取的信息 例如：'Orientation'旋转信息  
 * @return {Promise<Any>} 读取是个异步操作，返回指定的图片信息  
 */
const getImageTag = (file, tag, suc) => {
	if (!file) return 0;
	return new Promise((resolve, reject) => {
		/* eslint-disable func-names */
		// 箭头函数会修改this，所以这里不能用箭头函数  
		let imgObj = new Image()
		//let imgObj = document.createElement("img")
		imgObj.src = file
		//console.log(imgObj)
		uni.getImageInfo({
			src: file,
			success(res) {
				Exif.getData(imgObj, function() {
					Exif.getAllTags(this);
					let or = Exif.getTag(this, 'Orientation'); //这个Orientation 就是我们判断需不需要旋转的值了，有1、3、6、8  
					resolve(suc(or));
				});
			},
			fail(e) {
				reject(e);
			}
		})
	});
};

//网上提供的旋转function  
const rotateImg = (img, direction, canvas, times = 1) => {
	//console.log('开始旋转')
	//最小与最大旋转方向，图片旋转4次后回到原方向    
	var min_step = 0;
	var max_step = 3;
	if (img == null) return;

	//img的高度和宽度不能在img元素隐藏后获取，否则会出错    
	var height = img.height;
	var width = img.width;
	let maxWidth = 800;
	let canvasWidth = width; //图片原始长宽  
	let canvasHeight = height;
	let base = canvasWidth / canvasHeight;
	//console.log(maxWidth);
	if (canvasWidth > maxWidth) {
		canvasWidth = maxWidth;
		canvasHeight = Math.floor(canvasWidth / base);
	}
	width = canvasWidth;
	height = canvasHeight;
	var step = 0;

	if (step == null) {
		step = min_step;
	}

	if (direction == 'right') {
		step += times;
		//旋转到原位置，即超过最大值    
		step > max_step && (step = min_step);
	} else if (direction == 'left') {
		step -= times;
		step < min_step && (step = max_step);
	} else { //不旋转  
		step = 0;
	}

	//旋转角度以弧度值为参数    
	var degree = step * 90 * Math.PI / 180;
	var ctx = canvas.getContext('2d');
	//console.log(degree)
	//console.log(step)
	switch (step) {
		case 1:
			console.log('右旋转 90度')
			canvas.width = height;
			canvas.height = width;
			ctx.rotate(degree);
			ctx.drawImage(img, 0, -height, width, height);
			break;
		case 2:
			//console.log('旋转 180度')  
			canvas.width = width;
			canvas.height = height;
			ctx.rotate(degree);
			ctx.drawImage(img, -width, -height, width, height);
			break;
		case 3:
			console.log('左旋转 90度')
			canvas.width = height;
			canvas.height = width;
			ctx.rotate(degree);
			ctx.drawImage(img, -width, 0, width, height);
			break;
		default: //不旋转  
			canvas.width = width;
			canvas.height = height;
			ctx.drawImage(img, 0, 0, width, height);
			break;
	}

	let baseStr = canvas.toDataURL("image/png", 1);
	return baseStr;
}

/* 另一种图片旋转方式：
plus.zip.compressImage({
		src:url,  
		dst:"../_temp/temp.jpg",  
		quality:90,  
		overwrite:true,  
		rotate:90,  
		format:"jpg"  
	},  
	function(e) {
		imgBox.src = e.target;// 旋转后的图片路径  
		alert("Compress success!");  
	},function(error) {  
		alert("Compress error!"+JSON.stringify(error));  
});
*/

//let type = "image/png"; // 定义图片类型（canvas转的图片一般都是png，也可以指定其他类型）
//let conversions = base64ToBlob(m_b64, type); // 调用base64转图片方法
function base64ToBlob(urlData, type) {
	let arr = urlData.split(',');
	let mime = arr[0].match(/:(.*?);/)[1] || type;
	// 去掉url的头，并转化为byte
	let bytes = window.atob(arr[1]);
	// 处理异常,将ascii码小于0的转换为大于0
	let ab = new ArrayBuffer(bytes.length);
	// 生成视图（直接针对内存）：8位无符号整数，长度1个字节
	let ia = new Uint8Array(ab);
	for (let i = 0; i < bytes.length; i++) {
		ia[i] = bytes.charCodeAt(i);
	}
	return new Blob([ab], {
		type: mime
	});
}

function dataURLtoFile(dataurl, filename='dataurl_image_temp.png') {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while(n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, {type:mime});
}


module.exports = {
	imageCompress: imageCompress,
	base64ToBlob: base64ToBlob,
	dataURLtoFile: dataURLtoFile
}
