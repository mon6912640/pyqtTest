# encoding: UTF-8
# 系统模块
from queue import Queue, Empty
from threading import *

from typing import *

########################################################################
"""事件对象"""


class EventVo:
    # 事件类型
    type = ''
    # 事件附带数据
    data = None

    def __init__(self, p_type=None, p_data=None):
        self.type = p_type  # 事件类型
        self.data = p_data


########################################################################
class EventDispatcher:
    # ----------------------------------------------------------------------
    def __init__(self):
        """初始化事件管理器"""
        # 事件对象列表
        self.__eventQueue = Queue()
        # 事件管理器开关
        self.__active = False
        # 事件处理线程
        self.__thread = Thread(target=self.__run)
        # 事件回调个数
        self.__handler_count = 0

        # 这里的__handlers是一个字典，用来保存对应的事件的响应函数
        # 其中每个键对应的值是一个列表，列表中保存了对该事件监听的响应函数，一对多
        self.__handlers_map = {}

    # ----------------------------------------------------------------------
    def __run(self):
        """引擎运行"""
        while self.__active is True:
            try:
                # 获取事件的阻塞时间设为1秒
                event = self.__eventQueue.get(block=True, timeout=1)
                self.__event_process(event)
            except Empty:
                pass

    # ----------------------------------------------------------------------
    def __event_process(self, p_event: EventVo):
        """处理事件"""
        # 检查是否存在对该事件进行监听的处理函数
        if p_event.type in self.__handlers_map:
            # 若存在，则按顺序将事件传递给处理函数执行
            for handler in self.__handlers_map[p_event.type]:
                handler(p_event)

    # ----------------------------------------------------------------------
    def start(self):
        """启动"""
        # 将事件管理器设为启动
        if self.__active:
            return
        self.__active = True
        # 启动事件处理线程
        self.__thread.start()

    # ----------------------------------------------------------------------
    def stop(self):
        """停止"""
        # 将事件管理器设为停止
        if not self.__active:
            return
        self.__active = False
        # 等待事件处理线程退出
        self.__thread.join()

    # ----------------------------------------------------------------------
    def add_event(self, p_type: str, p_handler):
        """
        添加事件侦听
        :param p_type:
        :param p_handler:
        :return:
        """
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handler_list = self.__handlers_map[p_type]
        except KeyError:
            handler_list = []

        self.__handlers_map[p_type] = handler_list
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if p_handler not in handler_list:
            handler_list.append(p_handler)
            self.__handler_count += 1
            self.start()

    # ----------------------------------------------------------------------
    def remove_event(self, p_type: str, p_handler):
        if p_type not in self.__handlers_map:
            return
        handler_list: List = self.__handlers_map[p_type]
        if p_handler in handler_list:
            handler_list.remove(p_handler)
            self.__handler_count -= 1

    # ----------------------------------------------------------------------
    def send_event(self, p_type: str, p_data=None):
        """发送事件，向事件队列中存入事件"""
        self.__eventQueue.put(EventVo(p_type, p_data))


########################################################################
"""全局对象"""
EventCenter: EventDispatcher = EventDispatcher()
