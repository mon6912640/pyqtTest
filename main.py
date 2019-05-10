import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

import my_view


def init_view():
    print(type(ui.textBrowser))
    ui.textBrowser.setAcceptDrops(True)  # 开启拖动


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = my_view.MyQMainWindow()
    ui = my_view.MainWinGUI()
    ui.setupUi(main_win)
    main_win.setWindowTitle('fuck you')
    main_win.setWindowIcon(QIcon(':/icon/img/icon.png'))

    init_view()

    main_win.show()

    sys.exit(app.exec_())
    # 设置图标打包命令，注意：ico文件要放在与py文件统一层目录中
    # pyinstaller -F -w --icon=icon.ico main.py
