import argparse
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

import mainGUI2
from common import *


class MyQMainWindow(QMainWindow):
    def __init__(self):
        super(MyQMainWindow, self).__init__()

    def dragEnterEvent(self, event: QDragEnterEvent):
        EventCenterSync.send_event(EVENT_SHOW_LOG, '拖进来')
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
        EventCenterSync.send_event(EVENT_SHOW_LOG, '放下')

    def closeEvent(self, event):
        """
        主界面关闭时候调用，PyQt退出时候不会触发atexit模块退出，需要重写closeEvent事件
        :param event:
        :return:
        """
        print('程序退出')
        # EventCenterAsync.stop()  # 程序退出时候停止全局事件管理器的线程


class MainWinGUI(mainGUI2.Ui_MainWindow):
    def setupUi(self, MainWindow: MyQMainWindow):
        super(MainWinGUI, self).setupUi(MainWindow)
        MainWindow.setAcceptDrops(True)
        self.textBrowser.setHtml('程序初始化')

        EventCenterSync.add_event(EVENT_SHOW_LOG, self.handle_show_log)
        EventCenterSync.add_event(EVENT_MAIN_INIT, self.handle_init)

        self.textBrowser.textChanged.connect(self.scroll_to_end)
        self.pushButton.clicked.connect(self.btn_click)  # 按钮点击处理

    def handle_init(self, event: EventVo):
        pass

    def handle_show_log(self, event: EventVo):
        self.show_log(event.data)

    def show_log(self, p_str):
        self.textBrowser.append(p_str)

    def btn_click(self):
        print('fuck you')
        ins_app = QApplication.instance()
        ins_app.quit()

    def scroll_to_end(self):
        # 滚动到最后的处理
        self.textBrowser.moveCursor(QTextCursor.End)


def init_view():
    print(type(ui.textBrowser))
    # ui.textBrowser.setAcceptDrops(True)  # 开启拖动


# PyQt官方API文档
# https://www.riverbankcomputing.com/static/Docs/PyQt5/module_index.html

if __name__ == '__main__':
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='', help='需要压缩的源目录')
    parser.add_argument('--output', type=str, default='', help='输出的目录')
    args = parser.parse_args()

    print('source_path = ' + args.source)
    print('output_path = ' + args.output)

    main_win = MyQMainWindow()
    ui = MainWinGUI()
    ui.setupUi(main_win)
    main_win.setWindowTitle('fuck you')
    main_win.setWindowIcon(QIcon(':/icon/img/icon.png'))

    init_view()

    main_win.show()

    # 广播初始化事件
    EventCenterSync.send_event(EVENT_MAIN_INIT)
    show_log('source_path = ' + args.source)
    show_log('output_path = ' + args.output)
    # if args.source or args.output:
    #     app.quit()

    sys.exit(app.exec_())
    # 设置图标打包命令，注意：ico文件要放在与py文件统一层目录中
    # pyinstaller -F -w --icon=icon.ico main.py
