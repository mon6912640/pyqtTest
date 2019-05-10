from PyQt5.QtWidgets import QMainWindow
import mainGUI2
from monkey_event import *

EVENT_SHOW_LOG = 'event_show_log'


class MyQMainWindow(QMainWindow):
    def __init__(self):
        super(MyQMainWindow, self).__init__()

    def dragEnterEvent(self, event):
        EventCenter.send_event(EVENT_SHOW_LOG, '拖进来')

    def dragMoveEvent(self, event):
        pass
        # EventCenter.send_event(EVENT_SHOW_LOG, '拖进来')

    def dropEvent(self, event):
        EventCenter.send_event(EVENT_SHOW_LOG, '放下')

    def closeEvent(self, event):
        """
        主界面关闭时候调用，PyQt退出时候不会触发atexit模块退出，需要重写closeEvent事件
        :param event:
        :return:
        """
        EventCenter.stop()


class MainWinGUI(mainGUI2.Ui_MainWindow):
    def setupUi(self, MainWindow: MyQMainWindow):
        super(MainWinGUI, self).setupUi(MainWindow)
        MainWindow.setAcceptDrops(True)
        self.textBrowser.setHtml('程序初始化')
        EventCenter.add_event(EVENT_SHOW_LOG, self.handle_show_log)

    def handle_show_log(self, event: EventVo):
        self.showLog(event.data)

    def showLog(self, p_str):
        self.textBrowser.append(p_str)
        self.textBrowser
