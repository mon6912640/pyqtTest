import argparse
import sys
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QFrame

import TinyPngTool
import mainGUI2
import cleanGUI
from common import *


class MyQMainWindow(QMainWindow):
    __thread: Thread = None
    __queue: Queue = None
    __active = False

    def __init__(self):
        QMainWindow.__init__(self)

        self.__queue = Queue()
        self.__thread = Thread(target=self.__run)

        self.view = mainGUI2.Ui_MainWindow()
        self.view.setupUi(self)
        self.setAcceptDrops(True)

        EventCenterSync.add_event(EVENT_SHOW_LOG, self.handle_show_log)
        EventCenterSync.add_event(EVENT_MAIN_INIT, self.handle_init)

        self.view.cbOverride.setChecked(TinyPngTool.override)

        self.view.textBrowser.textChanged.connect(self.scroll_to_end)
        self.view.pushButton.clicked.connect(self.on_btn_click)  # 按钮点击处理
        self.view.cbOverride.stateChanged.connect(self.__on_overide_state_change)

        self.view.textBrowser.setHtml('程序初始化完成')
        show_log('请拖动文件/文件夹到此程序界面中进行压缩')

    def __run(self):
        while self.__active is True:
            try:
                list_path = self.__queue.get(block=True, timeout=1)
                TinyPngTool.run_by_list(list_path, './compress')
            except Empty:
                pass

    def thread_start(self, p_flag: bool):
        if not self.__thread:
            return
        if p_flag:
            if self.__active:
                return
            self.__active = True
            self.__thread.start()
        else:
            if not self.__active:
                return
            self.__active = False
            self.__thread.join()

    def handle_init(self, event: EventVo):
        pass

    def handle_show_log(self, event: EventVo):
        if event.data['type'] == LOG_TYPE_MAIN:
            self.show_log(event.data['str'])

    def show_log(self, p_str: str):
        self.view.textBrowser.append(p_str.encode('utf-8').decode('utf-8'))

    def on_btn_click(self):
        ins_app = QApplication.instance()
        ins_app.quit()

    def __on_overide_state_change(self, p_state):
        t_isChecked = self.view.cbOverride.isChecked()
        TinyPngTool.override = t_isChecked
        show_log('复选框点击 {0}'.format(t_isChecked))

    def scroll_to_end(self):
        # 滚动到最后的处理
        self.view.textBrowser.moveCursor(QTextCursor.End)

    def dragEnterEvent(self, event: QDragEnterEvent):
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
        # EventCenterSync.send_event(EVENT_SHOW_LOG, '放下')
        list_source = []
        for url in files:
            path_source = Path(url.toLocalFile())
            # print(path_source)
            # print(path_source.absolute())
            # print(path_source.exists())
            if not path_source.exists():
                continue
            if path_source.is_file():
                if path_source.suffix == '.jpg' or path_source.suffix == '.png':
                    list_source.append(path_source.absolute())
            elif path_source.is_dir():
                list_source.append(path_source.absolute())
        if len(list_source) > 0:
            self.__queue.put(list_source)
            self.thread_start(True)

    def closeEvent(self, event):
        """
        主界面关闭时候调用，PyQt退出时候不会触发atexit模块退出，需要重写closeEvent事件
        :param event:
        :return:
        """
        print('程序退出')
        # EventCenterAsync.stop()  # 程序退出时候停止全局事件管理器的线程
        self.thread_start(False)


class CleanView(QFrame):
    def __init__(self):
        QFrame.__init__(self)

        self.view = cleanGUI.Ui_Frame()
        self.view.setupUi(self)
        self.setAcceptDrops(True)

        self.view.textBrowser.textChanged.connect(self.scroll_to_end)
        self.view.textBrowser.setHtml('请拖动根目录文件夹进行批量删除带@source后缀的文件')

        EventCenterSync.add_event(EVENT_SHOW_LOG, self.handle_show_log)

    def handle_show_log(self, event: EventVo):
        if event.data['type'] == LOG_TYPE_CLEAN:
            self.show_log(event.data['str'])

    def scroll_to_end(self):
        # 滚动到最后的处理
        self.view.textBrowser.moveCursor(QTextCursor.End)

    def dragEnterEvent(self, event: QDragEnterEvent):
        mime_data: QMimeData = event.mimeData()
        if mime_data.hasFormat('text/uri-list'):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        mime_data: QMimeData = event.mimeData()
        files: List[QUrl] = mime_data.urls()
        list_source = []
        for url in files:
            path_source = Path(url.toLocalFile())
            if not path_source.exists():
                continue
            t_path = path_source.absolute()
            list_source.append(t_path)
        for t_path in list_source:
            TinyPngTool.clean(t_path)

    def show_log(self, p_str: str):
        self.view.textBrowser.append(p_str.encode('utf-8').decode('utf-8'))


# PyQt官方API文档
# https://www.riverbankcomputing.com/static/Docs/PyQt5/module_index.html

# pyqt进度条范例
# https://zhuanlan.zhihu.com/p/31109561

if __name__ == '__main__':
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='', help='需要压缩的源目录')
    parser.add_argument('--output', type=str, default='', help='输出的目录')
    args = parser.parse_args()

    print('source_path = ' + args.source)
    print('output_path = ' + args.output)

    main_win = MyQMainWindow()
    main_win.setWindowTitle('fuck you')
    main_win.setWindowIcon(QIcon(':/icon/img/icon.png'))
    main_win.show()

    clean_view = CleanView()


    def open_clean_view():
        clean_view.show()


    main_win.view.btnClean.clicked.connect(open_clean_view)

    clean_view.setWindowTitle('清理工具')

    # 广播初始化事件
    EventCenterSync.send_event(EVENT_MAIN_INIT)
    show_log('source_path = ' + args.source)
    show_log('output_path = ' + args.output)
    # if args.source or args.output:
    #     app.quit()

    sys.exit(app.exec_())
    # 设置图标打包命令，注意：ico文件要放在与py文件统一层目录中
    # pyinstaller -F -w --icon=icon.ico main.py
