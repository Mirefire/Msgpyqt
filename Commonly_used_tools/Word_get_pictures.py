# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Word_get_pictures.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(480, 500)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setGeometry(QtCore.QRect(180, 10, 121, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(dialog)
        self.textEdit.setGeometry(QtCore.QRect(10, 40, 461, 61))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(dialog)
        self.pushButton.setGeometry(QtCore.QRect(170, 240, 100, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 120, 54, 12))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(dialog)
        self.lineEdit.setGeometry(QtCore.QRect(80, 116, 91, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(dialog)
        self.label_3.setGeometry(QtCore.QRect(190, 120, 75, 12))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(270, 116, 111, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_5 = QtWidgets.QLabel(dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 150, 75, 20))
        self.label_5.setObjectName("label_5")
        self.lineEdit_4 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(90, 150, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(10, 190, 351, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_2 = QtWidgets.QPushButton(dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 190, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 150, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.openGLWidget = QtWidgets.QOpenGLWidget(dialog)
        self.openGLWidget.setGeometry(QtCore.QRect(10, 280, 461, 200))
        self.openGLWidget.setObjectName("openGLWidget")

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "文字变图片"))
        self.label.setText(_translate("dialog", "字体变图片"))
        self.pushButton.setText(_translate("dialog", "生成图片"))
        self.label_2.setText(_translate("dialog", "字体大小"))
        self.label_3.setText(_translate("dialog", "字体颜色rbg"))
        self.label_5.setText(_translate("dialog", "背景颜色rbg"))
        self.pushButton_2.setText(_translate("dialog", "保存路径"))
        self.pushButton_3.setText(_translate("dialog", "背景图片"))