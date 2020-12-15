# -*- coding: utf-8 -*-
""" 任务管理：
建立任务管理队列，支持添加、删除、查询；周期统计任务总状态、周期清理过期任务。
"""

import os
import time
import datetime
import enum
import inspect
from collections import OrderedDict
#from multiprocessing import Process, Queue

from app.engine_v1 import app_config, logger
from app.util import load_task_obj_data


# 任务状态（5种）：新任务：new、待处理：pending、处理中：running、处理成功：success、处理失败：fail
TaskStat = enum.Enum('TaskStat', ('NEW', 'PENDING', 'RUNNING', 'SUCCESS', 'FAIL'))

# 任务队列类型（3 种）：
# 1、新任务队列（NEW）：保存客户端所提交的请求处理任务；该队列定时处理，如果图片没有经过预处理（标准化、面部检测和特征识别）则处理之，已经预处理过的则直接迁移到待处理任务队列。
# 2、处理任务队列（PROCESS）：保存已经预处理过的任务，有 3 种状态（等待处理、处理中、或处理完尚未超过指定时间）。
# 3、过期任务队列（EXPIRED）：保存处理超过指定时间（比如5分钟）的任务队列。
TaskQueue = enum.Enum('TaskQueue', ('NEW', 'PROCESS', 'EXPIRED'))


class Task:
    """图片处理任务"""

    INVALID_VALUE = -9999
    
    def __init__(self, task_id=None, task_stat=None,
                 user_id=None, user_type=None, m_id=None,
                 func_group=None, func_class=None, func_name=None,
                 func_params=None, msg=None):
        # 1. 任务编号：任务查询主键。任务添加时根据时间自动生成，后续客户端可据此查询任务状态。
        self.task_id = task_id
        # 2. 任务状态：4种
        self.task_stat = task_stat
        # 3. 用户id：完成登录认证后的用户id
        self.user_id = user_id
        # 4. 用户类型：2种（normal、vip，由后端根据购买记录等决定）
        self.user_type = user_type
        # 5. 图片id：由客户端传入或图片存储模块返回
        self.m_id = m_id
        # 6. 功能类别：所需进行的处理类别（内部表达），如 hair_color
        self.func_group = func_group
        # 7. 功能类型：所需进行的处理类型（内部表达），当前取值有两种：
        # 'fc_editor' - 编辑类，全尺寸，无水印
        # 'fc_fun' - 娱乐类，半尺寸，有水印
        self.func_class = func_class
        # 8. 功能名称：所需进行的处理名称（内部表达），如 hair_color_blond
        self.func_name = func_name
        # 9. 功能参数：所需进行的处理参数，如处理强度 strength = 5 等
        self.func_params = func_params
        # 10. 附加信息：一般作为任务状态的补充说明
        self.msg = msg
        # 前面等待处理的任务数量（TODO: 在状态初次转为 PENDING 时开始真实计数）
        self.pending_tasks = 2**31

    def update(self, key, value=INVALID_VALUE):
        """更新节点字段内容（不包含只读字段如 task_id）"""

        ## 获取函数输入参数信息
        #frame = inspect.currentframe()
        #args, _, _, values = inspect.getargvalues(frame)
        
        # 首先检查字段合法性
        if key not in self.__dict__:
            return False, 'unknown task item: {}'.format(key)
        
        # 更新指定的属性值
        if value != self.INVALID_VALUE:
            self.__dict__[key] = value


class TaskController(object):
    """任务管理器。通过多进程代理提供给客户端进行访问。主要接口有：
    任务添加、删除、查询；统计任务总状态；清理过期任务。
    """

    tasks_processed = 0
    __start_time = datetime.datetime.now()

    # 任务队列：分为 3 个，都需定时调用相关类方法处理或清理
    __task_queue = {}
    for i in TaskQueue:
        __task_queue[i] = OrderedDict()

    def __init__(self):
        """初始化"""
        pass

    def __make_response(self, if_success, data=None):
        if if_success:
            return({'return': 'success', 'data': data})
        else:
            return({'return': 'fail', 'data': data})

    # @classmethod
    def new_task_add(self, task={}):
        """添加新任务节点到队列中
        任务信息主要包括：图片ID、人脸位置及特征数据、处理方式名称和参数，任务初始状态等"""

        # 参数合法性检查
        params_invalid = False
        msg = None
        if not task:
            params_invalid = True
            msg = 'task is none'
        else:
            for i in ('user_id', 'm_id', 'func_group',
                      'func_name', 'func_params', 'task_stat'):
                if i not in task:
                    params_invalid = True
                    msg = 'invalid param, {} needed'.format(i)
                    break
        if params_invalid:
            return self.__make_response(False, msg)

        # 根据客户端传入的 task 信息生成任务对象
        task_id = str(time.time())
        new_task = Task(
            task_id = task_id,
            user_id = task['user_id'],
            user_type = 'normal', # FIXME: 查找数据库根据判断用户类型
            m_id = task['m_id'],
            func_group = task['func_group'],
            func_class = task['func_class'],
            func_name = task['func_name'],
            func_params = task['func_params'],
            task_stat = task['task_stat']
        )
        if new_task.task_stat == TaskStat.NEW:
            self.__task_queue[TaskQueue.NEW][task_id] = new_task
        elif new_task.task_stat == TaskStat.PENDING:
            self.__task_queue[TaskQueue.PROCESS][task_id] = new_task

        return self.__make_response(True, {'task_id':task_id})

    def new_task_get(self):
        """从新任务队列中按顺序获取1个任务节点（只读信息，不摘取）"""

        # 获取一个 NEW 任务
        __task = None
        for i in self.__task_queue[TaskQueue.NEW]:
            task = self.__task_queue[TaskQueue.NEW][i]
            if task.task_stat == TaskStat.NEW:
                task.task_stat = TaskStat.PENDING # 更改状态，防止其他预处理进程再获取
                __task = task
                break
        if not __task:
            return self.__make_response(False, 'no new task found')
        
        return self.__make_response(True, __task)

    def pending_tasks_get(self, task_filters):
        """获取分类待处理任务（该函数被工作引擎用于获取指定待处理任务）
        为便于多进程并行处理，这里从 process 任务队列中，按功能组及优先级获取 1 个没有被处理的任务"""

        __task = None
        # 优先获取 VIP 用户待处理任务
        for func_group, func_name_list in task_filters:
            for i in self.__task_queue[TaskQueue.PROCESS]:
                task = self.__task_queue[TaskQueue.PROCESS][i]
                if task.task_stat == TaskStat.PENDING \
                              and task.func_group == func_group \
                              and task.func_name in func_name_list \
                              and task.user_type == 'vip':
                    __task = task
                    __task.task_stat = TaskStat.RUNNING
                    break
        if not __task:
            # 再获取普通用户待处理任务
            for func_group, func_name_list in task_filters:
                for i in self.__task_queue[TaskQueue.PROCESS]:
                    task = self.__task_queue[TaskQueue.PROCESS][i]
                    #print('--> task:', task.task_id, task.task_stat, task.user_type, task.func_group)
                    if task.task_stat == TaskStat.PENDING \
                                  and task.func_group == func_group \
                                  and task.func_name in func_name_list \
                                  and task.user_type == 'normal':
                        __task = task
                        __task.task_stat = TaskStat.RUNNING
                        break
        if not __task:
            return self.__make_response(False, 'no pending task found')
        
        return self.__make_response(True, __task)

    def task_update(self, task_id, queue, task_items={}):
        """更新任务节点属性取值"""

        if queue not in self.__task_queue:
            return self.__make_response(False, 'no such task queue: {}'.format(queue))
        if task_id not in self.__task_queue[queue]:
            return self.__make_response(False, 'no such task: {}'.format(task_id))
        
        task = self.__task_queue[queue][task_id]
        for i in task_items:
            if i not in dir(task):
                return self.__make_response(False, 'no such task item: {}'.format(i))
        
        for i in task_items:
            task.update(i, task_items[i])
        
        return self.__make_response(True, task)
    
    def task_move(self, task_id, from_queue=TaskQueue.NEW, to_queue=TaskQueue.PROCESS):
        """将任务节点从一个队列迁移到另外一个队列"""

        if from_queue == TaskQueue.NEW and to_queue == TaskQueue.PROCESS:
            if task_id not in self.__task_queue[TaskQueue.NEW]:
                return self.__make_response(False, 'no new task found: {}'.format(task_id))
            task = self.__task_queue[TaskQueue.NEW].pop(task_id)
            self.__task_queue[TaskQueue.PROCESS][task_id] = task
        elif from_queue == TaskQueue.PROCESS and to_queue == TaskQueue.EXPIRED:
            if task_id not in self.__task_queue[TaskQueue.PROCESS]:
                return self.__make_response(False, 'no process task found: {}'.format(task_id))
            task = self.__task_queue[TaskQueue.PROCESS].pop(task_id)
            self.__task_queue[TaskQueue.EXPIRED][task_id] = task
        else:
            return self.__make_response(False, 'unknown queues pair: {}->{}'
                                        .format(from_queue, to_queue))
        
        return self.__make_response(True, task)

    # @classmethod
    def task_query(self, task_id):
        """查询任务状态
        返回任务执行状态，主要有：任务进度、等待时间、处理时间、和处理结果。
        任务进度 = (前面待处理任务数量 - 添加时待处理任务数量) / 添加时待处理任务数量 * 100
        等待时间 = 当前时间 - 任务添加时间
        处理时间 = 任务完成时间 - 任务开始处理时间
        处理结果 = (输出图片内容，或补充信息)
        """

        task_info = None
        
        # 先查处理队列，若没找到则查新队列，不查已过期队列。根据 task_id 返回查询任务运行状态
        task = self.__task_queue[TaskQueue.PROCESS].get(task_id)
        __task_queue = TaskQueue.PROCESS
        if not task:
            task = self.__task_queue[TaskQueue.NEW].get(task_id)
            __task_queue = TaskQueue.PROCESS
        
        if task:
            task_info = {}
            
            # 任务进度 #FIXME: 考虑更贴合实际的计算方法
            if task.task_stat == TaskStat.NEW:
                task_info['progress'] = 10 # 任务执行进度，取值范围 0~100
            elif task.task_stat == TaskStat.PENDING:
                pendings = self.count_pending_tasks(task_id, __task_queue)
                task_info['progress'] = int(70 - 60*(float(pendings)/task.pending_tasks))
            elif task.task_stat == TaskStat.RUNNING:
                task_info['progress'] = 70
            elif task.task_stat == TaskStat.SUCCESS:
                task_info['progress'] = 100
                task_info['image'] = load_task_obj_data(
                                                app_config.SAVE_FILE_NAME['image_temp'],
                                                task.m_id, app_config, logger)
            else: # TaskStat.FAIL
                task_info['progress'] = 0
            
            task_info['m_id'] = task.m_id
            task_info['func_class'] = task.func_class
            task_info['msg'] = task.msg
            #TODO: 等待时间
            #TODO: 处理时间

        return self.__make_response(True, task_info)

    # @classmethod
    def task_delete(self, task_id, from_queue):
        """从指定任务队列中删除节点（不包括图片等任务文件，这些另外清理）"""

        if from_queue not in TaskQueue:
            return self.__make_response(False, 'unknown queue: {}'.format(from_queue))

        if task_id not in self.__task_queue[from_queue]:
            return self.__make_response(False, 'no task found: {}'.format(task_id))
        else:
            return self.__make_response(True, self.__task_queue[from_queue].pop(task_id))

    def tasks_clean(self):
        """从指定任务队列中删除节点（不包括图片等任务文件，这些另外清理）"""

        # 1、检查”新任务队列“，将超过指定时间的任务迁移到”过期任务队列“
        count = 0
        tasks_list = [i for i in self.__task_queue[TaskQueue.NEW].keys()]
        for i in tasks_list:
            task_id = i
            if time.time() - float(task_id) > app_config.TERM_TASK_EXPIRED: # 默认5分钟
                task2 = self.__task_queue[TaskQueue.NEW].pop(task_id)
                self.__task_queue[TaskQueue.EXPIRED][task_id] = task2
                count += 1
        if count > 0:
            logger.warn('moved {} tasks from queue NEW to EXPIRED'.format(count))

        # 2、检查”处理任务队列“，将超过指定时间的任务（非处理中的）迁移到”过期任务队列“
        count = 0
        tasks_list = [i for i in self.__task_queue[TaskQueue.PROCESS].keys()]
        for i in tasks_list:
            #task_id = self.__task_queue[TaskQueue.PROCESS][i].task_id
            task_id = i
            if time.time() - float(task_id) > app_config.TERM_TASK_EXPIRED: # 默认5分钟
                task2 = self.__task_queue[TaskQueue.PROCESS].pop(task_id)
                self.__task_queue[TaskQueue.EXPIRED][task_id] = task2
                count += 1
        if count > 0:
            logger.warn('moved {} tasks from queue PROCESS to EXPIRED'.format(count))

        # 3、检查”过期任务队列“，将超过最大保留时间的任务删除
        count = 0
        tasks_list = [i for i in self.__task_queue[TaskQueue.EXPIRED].keys()]
        for i in tasks_list:
            #task_id = self.__task_queue[TaskQueue.EXPIRED][i].task_id
            task_id = i
            if time.time() - float(task_id) > app_config.TERM_TASK_CLEANED: # 默认24小时
                task2 = self.__task_queue[TaskQueue.EXPIRED].pop(task_id)
                # 删除任务资源文件
                file_dir =  os.path.join(app_config.UPLOAD_FOLDER, task2.m_id.replace('-', '/'))
                import shutil
                shutil.rmtree(file_dir, ignore_errors=True)
                count += 1
        if count > 0:
            logger.warn('cleaned {} tasks from queue EXPIRED'.format(count))

        return self.__make_response(True)
    
    # @property
    def status(self):
        """查询服务状态
        返回引擎的运行统计信息"""
        uptime = datetime.datetime.now() - self.__start_time

        stat = OrderedDict()
        stat["total tasks processed"] = self.tasks_processed
        stat["new tasks length"] = len(self.__task_queue[TaskQueue.NEW])
        stat["process tasks length"] = len(self.__task_queue[TaskQueue.PROCESS])
        stat["expired tasks length"] = len(self.__task_queue[TaskQueue.EXPIRED])
        stat["uptime"] = uptime

        return self.__make_response(True, stat)

    def count_pending_tasks(self, task_id, task_queue):
        """统计指定任务节点前面的待处理任务数"""

        count = 0
        for i in self.__task_queue[task_queue]:
            task = self.__task_queue[task_queue][i]
            if (task.task_stat == TaskStat.PENDING or task.task_stat == TaskStat.PENDING) and task.task_id < task_id:
                count += 1
        
        return count
