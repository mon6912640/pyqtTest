# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUI2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(636, 313)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 611, 201))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(520, 220, 75, 23))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/img/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName("pushButton")
        self.cbOverride = QtWidgets.QCheckBox(self.centralwidget)
        self.cbOverride.setGeometry(QtCore.QRect(10, 220, 101, 16))
        self.cbOverride.setObjectName("cbOverride")
        self.btnClean = QtWidgets.QPushButton(self.centralwidget)
        self.btnClean.setGeometry(QtCore.QRect(10, 240, 75, 23))
        self.btnClean.setObjectName("btnClean")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 636, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "ok"))
        self.cbOverride.setText(_translate("MainWindow", "覆盖原文件"))
        self.btnClean.setText(_translate("MainWindow", "清理工具"))

import res_rc
