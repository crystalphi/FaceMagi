function formatMoney(volume) {
  //输入单位为分
  let flag = 1
  if (volume < 0) {
    flag = -1;
    volume = -volume;
  }
  volume = volume / 100; //转为元
  if (volume > 1e6) {
    return flag * (volume / 1e6).toFixed(2) + '百万'
  } else if (volume > 1e4) {
    return flag * (volume / 1e4).toFixed(2) + '万'
  } else {
    return flag * volume.toFixed(2)
  }
}

function formatTime(time) {
  if (typeof time !== 'number' || time < 0) {
    return time
  }
  var hour = parseInt(time / 3600)
  time = time % 3600
  var minute = parseInt(time / 60)
  time = time % 60
  var second = time
  return ([hour, minute, second]).map(function(n) {
    n = n.toString()
    return n[1] ? n : '0' + n
  }).join(':')
}

function formatLocation(longitude, latitude) {
  if (typeof longitude === 'string' && typeof latitude === 'string') {
    longitude = parseFloat(longitude)
    latitude = parseFloat(latitude)
  }
  longitude = longitude.toFixed(2)
  latitude = latitude.toFixed(2)
  return {
    longitude: longitude.toString().split('.'),
    latitude: latitude.toString().split('.')
  }
}
var dateUtils = {
  UNITS: {
    '年': 31557600000,
    '月': 2629800000,
    '天': 86400000,
    '小时': 3600000,
    '分钟': 60000,
    '秒': 1000
  },
  humanize: function(milliseconds) {
    var humanize = '';
    for (var key in this.UNITS) {
      if (milliseconds >= this.UNITS[key]) {
        humanize = Math.floor(milliseconds / this.UNITS[key]) + key + '前';
        break;
      }
    }
    return humanize || '刚刚';
  },
  format: function(dateStr) {
    var date = this.parse(dateStr)
    var diff = Date.now() - date.getTime();
    if (diff < this.UNITS['天']) {
      return this.humanize(diff);
    }
    var _format = function(number) {
      return (number < 10 ? ('0' + number) : number);
    };
    return date.getFullYear() + '/' + _format(date.getMonth() + 1) + '/' + _format(date.getDay()) + '-' + _format(
      date.getHours()) + ':' + _format(date.getMinutes());
  },
  parse: function(str) { //将"yyyy-mm-dd HH:MM:ss"格式的字符串，转化为一个Date对象
    var a = str.split(/[^0-9]/);
    return new Date(a[0], a[1] - 1, a[2], a[3], a[4], a[5]);
  }
};
var mapUtils = {
  toRad: function(d) {
    return d * Math.PI / 180;
  },
  //计算地球上两个点之间的测地距离
  getDistance: function(lat1, lng1, lat2, lng2) {
    // lat为纬度,
    // lng为经度,
    let radLat1 = this.toRad(lat1);
    let radLat2 = this.toRad(lat2);
    let deltaLat = radLat1 - radLat2;
    let deltaLng = this.toRad(lng1) - this.toRad(lng2);
    let dist = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(deltaLat / 2), 2) + Math.cos(radLat1) * Math.cos(radLat2) *
      Math.pow(Math.sin(deltaLng / 2), 2)));
    return dist * 6378137;
    //alert(  getDistance(39.91917,116.3896,39.91726,116.3940) );
  },
  formatedDistance: function(distance) {
    if (distance > 1000) {
      return (distance / 1000).toFixed(2) + '公里'
    } else {
      return Math.round(distance) + '米'
    }
  }
}
var uniUtils = {
  upx2px: function(upx) {
    return uni.getSystemInfoSync().windowWidth / 750 * upx
  }
}
module.exports = {
  formatMoney: formatMoney,
  formatTime: formatTime,
  formatLocation: formatLocation,
  dateUtils: dateUtils,
  mapUtils: mapUtils,
  uniUtils: uniUtils,
}
