/**
 * @description 输出日期到控制台,如果是字符串、数值类型直接输出，
 * 如果是数组和对象类型，则递归输出对象的属性或者数组的成员
 * @param {Object} obj
 */

/**
 * Function : dump()
 * Arguments: The data - array,hash(associative array),object
 *    The level - OPTIONAL
 * Returns  : The textual representation of the array.
 * This function was inspired by the print_r function of PHP.
 * This will accept some data as the argument and return a
 * text that will be a more readable version of the
 * array/hash/object that is given.
 * Docs: http://www.openjs.com/scripts/others/dump_function_php_print_r.php
 * USAGE:
 *       console.log(qs.core.dump({name:'qs', value:[1,2,3,4,5]}));
 */
import helper from './helper'

//	var MAX_DUMP_DEPTH = 10;
const var_dump = function(arr, level = 0) {
	level = level ? level : 0;

	let dumped_text = "\n";
	if (!level) level = 0;

	if (level > 10) { //MAX_DUMP_DEPTH=10
		return dumped_text + ": <Maximum Depth Reached>\n";
	}

	//The padding given at the beginning of the line.
	let level_padding = "";
	for (let j = 0; j < level + 1; j++) level_padding += "\t";

	if (typeof(arr) == 'object') { //Array/Hashes/Objects
		for (let item in arr) {
			let value = arr[item];
			if (helper.isNullOrUndefined(value)) {
				dumped_text += level_padding + "'" + item + "' => null\n";
			} else if (helper.isArray(value)) { // If it is an array		
				if (helper.isEmpty(value)) {
					dumped_text += level_padding + "'" + item + "' =>(Empty Array)\n";
				} else {
					dumped_text += level_padding + "'" + item + "' =>(Array)\n";
					dumped_text += var_dump(value, level + 1);
				}
				dumped_text += var_dump(value, level + 1);
			} else if (helper.isObject(value)) { //If it is an Object
				dumped_text += level_padding + "'" + item + "' =>(Object)\n";
				dumped_text += var_dump(value, level + 1);
			} else { //其它类型
				dumped_text += level_padding + "'" + item + "' => " + JSON.stringify(value) + "\n";
			}
		}
	} else { //Strings/Chars/Numbers etc.
		dumped_text = "===>" + arr + "<===(" + typeof(arr) + ")";
	}
	return dumped_text;
}

const dump = function(arr) {
	return var_dump(arr, 0);
};

// const Console = class {
// 	log(obj) {
// 		let message = var_dump(obj, 0);
// 		console.log(message);
// 	}
// 
// 	info(obj) {
// 		let message = var_dump(obj, 0);
// 		console.info(message);
// 	}
// 
// 	warn(obj) {
// 		let message = var_dump(obj, 0);
// 		console.warn(message);
// 	}
// 
// 	debug(obj) {
// 		let message = var_dump(obj, 0);
// 		console.debug(message);
// 	}
// 
// 	error(obj) {
// 		let message = var_dump(obj, 0);
// 		console.error(message);
// 	}
// }

let logger;

// #ifndef H5
// logger = require('tracer').console();
logger = console;
// #endif

// #ifdef H5
// logger = new Console(); //没法跟踪出错的文件和行号
logger = console;
// #endif

logger.dump = dump;

export {
	logger,
	dump
};

export default logger;
