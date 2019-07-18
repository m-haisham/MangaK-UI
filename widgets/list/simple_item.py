# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_item.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(323, 35)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.mangaLabel = QtWidgets.QLabel(Form)
        self.mangaLabel.setSizeIncrement(QtCore.QSize(5, 5))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.mangaLabel.setFont(font)
        self.mangaLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.mangaLabel.setLineWidth(0)
        self.mangaLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mangaLabel.setWordWrap(True)
        self.mangaLabel.setObjectName("mangaLabel")
        self.gridLayout_3.addWidget(self.mangaLabel, 1, 0, 1, 1)
        self.chapterLabel = QtWidgets.QLabel(Form)
        self.chapterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.chapterLabel.setObjectName("chapterLabel")
        self.gridLayout_3.addWidget(self.chapterLabel, 2, 0, 1, 1)
        self.line = QtWidgets.QFrame(Form)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.mangaLabel.setText(_translate("Form", "TextLabel"))
        self.chapterLabel.setText(_translate("Form", "TextLabel"))


