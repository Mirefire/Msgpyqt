from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

class mylineEdit(QLineEdit):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()  # 发送clicked信号

    # def  __init__(self):
    # self.lineEdit_3.installEventFilter(self)  # 方法2(1)
    # self.clicked.connect(self.showData)


    # def eventFilter(self, widget, QEvent):
    #     try:
    #         if widget == self.lineEdit_3:
    #             if QEvent.type() == QEvent.FocusOut:
    #                 pass
    #             elif QEvent.type() == QEvent.FocusIn:
    #                 self.clicked.emit()  # 当焦点再次落到edit输入框时，发送clicked信号出去
    #             else:
    #                 pass
    #         return False
    #     except Exception as e:
    #         pass

    # def showData(self):
    #     print('ok')
    #     try:
    #         self.lineEdit_3.setFocus()
    #         font, isok = QFontDialog.getFont()
    #         print(font)
    #         print(isok)
    #     except Exception as e:
    #         pass