from PyQt5.QtWidgets import QMainWindow
import mainGUI2
from monkey_event import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import *

EVENT_SHOW_LOG = 'event_show_log'


class MyQMainWindow(QMainWindow):
    def __init__(self):
        super(MyQMainWindow, self).__init__()

    def dragEnterEvent(self, event: QDragEnterEvent):
        EventCenter.send_event(EVENT_SHOW_LOG, '拖进来')
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasFormat('text/uri-list'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        pass
        # EventCenter.send_event(EVENT_SHOW_LOG, '拖进来')

    def dropEvent(self, event: QDropEvent):
        mime_data: QMimeData = event.mimeData()
        files: List[QUrl] = mime_data.urls()
        for url in files:
            print(url.url())
        EventCenter.send_event(EVENT_SHOW_LOG, '放下')

    def closeEvent(self, event):
        """
        主界面关闭时候调用，PyQt退出时候不会触发atexit模块退出，需要重写closeEvent事件
        :param event:
        :return:
        """
        EventCenter.stop()  # 程序退出时候停止全局事件管理器的线程


class MainWinGUI(mainGUI2.Ui_MainWindow):
    def setupUi(self, MainWindow: MyQMainWindow):
        super(MainWinGUI, self).setupUi(MainWindow)
        MainWindow.setAcceptDrops(True)
        self.textBrowser.setHtml('程序初始化')

        EventCenter.add_event(EVENT_SHOW_LOG, self.handle_show_log)

        self.textBrowser.textChanged.connect(self.scroll_to_end)
        self.pushButton.clicked.connect(self.btn_click)  # 按钮点击处理

    def handle_show_log(self, event: EventVo):
        self.showLog(event.data)

    def showLog(self, p_str):
        self.textBrowser.append(p_str)

    def btn_click(self):
        print('fuck you')

    def scroll_to_end(self):
        # 滚动到最后的处理
        self.textBrowser.moveCursor(QTextCursor.End)
