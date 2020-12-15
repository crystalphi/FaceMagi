# -*- coding: utf-8 -*-
""" 多进程通讯支持：本模块为客户端，封装提供给 Flask 和各工作引擎进行调用。
"""

import sys
import logging
import traceback
import multiprocessing
from multiprocessing.managers import BaseManager

from app.engine_v1 import app_config, logger


class ManagerClient(object):
    """管理器客户端"""

    def __init__(self):
        self.logger = logger
        self.__em_address = app_config.EM_ADDRESS
        self.__em_port = app_config.EM_PORT
        self.__em_authkey = app_config.EM_AUTHKEY
        self.__client = self.__get_client()

    def __get_client(self):
        try:
            from multiprocessing.managers import BaseManager
            client = BaseManager(
                address=(self.__em_address, self.__em_port), authkey=self.__em_authkey)
            client.register('task_controller')
            client.register('engine_controller')
            client.register('shared_data_controller')
            client.connect()
            self.logger.info('connected to manager %s:%d ...' %
                  (self.__em_address, self.__em_port))
        except Exception as e:
            client = None
            self.logger.warn('client connect fail! {}'.format(e))
            #traceback.print_exc(file=sys.stderr)
        return client

    def __get_shared_obj(self, registered_name):
        """根据注册名称获取进程间共享对象
        如果失败则重新连接并再次获取，如果仍然失败则返回空
        """

        try:
            tc = getattr(self.__client, registered_name)()
        except:
            try:
                self.__client = self.__get_client()
                tc = getattr(self.__client, registered_name)()
            except Exception as e:
                tc = None
                traceback.print_exc(file=sys.stderr)
                self.logger.error('manager client get registered obj failed! {}'.format(e))
        return tc
    
    def shared_obj_func_list(self, registered_name):
        """根据注册名称获取进程间共享对象所支持的方法列表"""
        
        tc = self.__get_shared_obj(registered_name)
        if tc:
            result = []
            for attr in dir(tc):
                if attr[0] != '_':
                    class_attr_obj = getattr(tc, attr)
                    if hasattr(class_attr_obj, '__call__'):
                        result.append(attr)
            return result
        else:
            return None
    
    def shared_obj_func_call(self, registered_name, func_name, func_args=None):
        """调用指定进程间共享对象的方法"""
        
        tc = self.__get_shared_obj(registered_name)
        if tc:
            result = None
            for attr in dir(tc):
                if attr[0] != '_':
                    class_attr_obj = getattr(tc, attr)
                    if hasattr(class_attr_obj, '__call__') and func_name == attr:
                        try:
                            if func_args:
                                result = class_attr_obj(*func_args)
                            else:
                                result = class_attr_obj()
                        except Exception as e:
                            self.logger.error('call {} with args {} fail: {}'
                                    .format(func_name, func_args, str(e)))
                            traceback.print_exc(file=sys.stderr)
                        break
            else:
                self.logger.warn('unsupported function: {}'.format(func_name))
            return result
        else:
            return None

    def is_alive(self):
        stat = self.shared_obj_func_call('task_controller', 'status')
        if stat:
            self.logger.info('manager client connected. task controller status: %s' % stat)
            return True
        else:
            self.logger.warn('manager client disconnected.')
            return False
