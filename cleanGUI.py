# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cleanGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(400, 300)
        self.textBrowser = QtWidgets.QTextBrowser(Frame)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))

