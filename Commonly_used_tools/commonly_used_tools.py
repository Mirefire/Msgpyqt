from numpy import unicode
from Commonly_used_tools import Word_get_pictures
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pygame,datetime,sys,os,io
from PIL import Image, ImageFont, ImageDraw
import numpy as np
from Logiclayer.plugin import createClick
pygame.init()
from PyQt5.QtGui import *
import time
class Com_use_tool(QDialog,Word_get_pictures.Ui_dialog):
    com_use_tool_signal = pyqtSignal(object)
    # clicked = pyqtSignal()
    def __init__(self):
        super(Com_use_tool, self).__init__()
        self.setupUi(self)
        self.savepathimg = None
        self._translate = QCoreApplication.translate
        self.lineEdit_4.setText('255,255,255')
        self.lineEdit_2.setText('0,0,0')
        self.connect()
    def connect(self):
        self.pushButton.clicked.connect(self.changesimg)
        self.pushButton_2.clicked.connect(self.savepath)
        self.pushButton_3.clicked.connect(self.upimg)
    #上传图片
    def upimg(self):
        try:
            openfile_name, _ = QFileDialog.getOpenFileName(self, '选择图片', '', 'Excel files(*.png , *.jpg)')
            # self.openGLWidget.
            print(openfile_name)
        except Exception as e:
            pass


    def changesimg(self):
        try:
            text = str(self.textEdit.toPlainText())
            fontsize = int(self.lineEdit.text())
            bgcolor = str(self.lineEdit_4.text())
            fontcolor = str(self.lineEdit_2.text())
            bgcolor = bgcolor.split(',')
            bgcolor = (int(bgcolor[0]),int(bgcolor[1]),int(bgcolor[2]))
            fontcolor = fontcolor.split(',')
            fontcolor = (int(fontcolor[0]), int(fontcolor[1]), int(fontcolor[2]))

            text = u"%s"%text
        # #     # 设置字体和字号

            # im = Image.new("RGB", (300, 50), (255, 255, 255))
            font = pygame.font.Font(os.path.join("Logiclayer/plugin/fontFamily/", "msyh.ttf"), fontsize)

        # #     # 渲染图片，设置背景颜色和字体样式,前面的颜色是字体颜色
            fontimg = font.render(text.replace(" ",""), True, fontcolor, bgcolor)
            timestr = str(datetime.datetime.now()).replace(':', '_')
            fn = self.savepathimg + timestr + ".png"
        #     print(fn)
        #     sio = io.StringIO()
            pygame.image.save(fontimg, fn)  # 图片保存地址
            # sio.seek(0)
            QMessageBox.information(self,"消息提示","已成功，请查看！")
            # line = Image.open(sio)
            # im.paste(line, (10, 5))
            # im.save("t.png")
        #     # 保存图片

        except Exception as e:
            print(e)
            pass

    def savepath(self):
        try:
            # file_path = QFileDialog.getSaveFileName(self, "选择保存路径", "",
            #                                         "all files(*.*)")
            dir_path = QFileDialog.getExistingDirectory(self, "选择保存路径", "")

            self.savepathimg = str(dir_path).replace("/","\\")+'\\'
            # self.savepathimg = unicode(dir_path.toUtf8(), 'utf-8', 'ignore')
            self.lineEdit_5.setText(self._translate("",self.savepathimg))

        except Exception as e:
            pass