import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import cv2 as cv,ctypes,win32con,Levenshtein
from cnocr import CnOcr
from cnstd import CnStd
import mxnet as mx
from cnocr.line_split import line_split
from PIL import Image, ImageGrab
from Qdialog import dialog
from Logiclayer import progress_thread,auto_response,open_flie
from win32process import SuspendThread,ResumeThread
from pynput.mouse import Button, Controller as MoveTo
from pynput.keyboard import Key, Controller as Thekeys
import os,time,pytesseract,datetime
class Dialog_Menu(QDialog,dialog.Ui_Dialog,auto_response.Auto_resp):
    dialogsing_msg = pyqtSignal(object)
    def __init__(self):
        super(Dialog_Menu, self).__init__()
        self.setupUi(self)
        self.hour = 0
        self.mints = 0
        self.ss = 0
        self.timer = None
        self.fnPath = None
        self.timetotal = 0
        self.step = 0
        pointSize = self.label_7.fontInfo().pointSize()
        self.horizontalSlider.setValue(pointSize)
        self.label_8.setText('%s'%pointSize)
        self.lcdNumber.display('00:00:00')
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShadow(QFrame.Sunken)
        self.frame.setPalette(QPalette(Qt.green))
        self.pen = QPen(Qt.green, 2, Qt.SolidLine)
        self.frame_2.setAutoFillBackground(True)
        self.frame_2.setPalette(QPalette(Qt.red))
        self.pen1 = QPen(Qt.red, 2, Qt.SolidLine)
        self.frame_3.setAutoFillBackground(True)
        self.frame_3.setPalette(QPalette(Qt.black))
        self.pen2 = QPen(Qt.black, 2, Qt.SolidLine)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
        self.pushButton_7.setEnabled(False)
        self.connect()
    def connect(self):
        self.pushButton.clicked.connect(lambda:self.changColor(1))
        self.pushButton_2.clicked.connect(lambda:self.changColor(2))
        self.pushButton_3.clicked.connect(lambda:self.changColor(3))
        self.pushButton_4.clicked.connect(self.start)
        self.pushButton_5.clicked.connect(self.stopTime)
        self.pushButton_7.clicked.connect(self.restore)
        self.pushButton_6.clicked.connect(self.suspended)
        self.pushButton_8.clicked.connect(self.csrenWind)
        self.horizontalSlider.valueChanged.connect(self.valuechange)
        self.dialogsing_msg.connect(self.dialog_msg)

    def valuechange(self):
        try:
            val = self.horizontalSlider.value()
            self.label_7.setFont(QFont('Arial',val))
            self.label_8.setText('%s'%val)
        except Exception as e:
            pass
    #开始
    def start(self):
        txt = self.lineEdit.text()
        try:
            if isinstance(float(txt), float):
                if float(txt) > 24 or float(txt) < 0.1:
                    QMessageBox.about(self, '输入错误', '输入值不能大于24小时,不能小于0.1小时')
                    return
                txt = float(txt)
                self.pushButton_5.show()
                self.timetotal = txt*60*60
                mis = txt*60
                # print(int(mis))
                if txt >= 1:
                    self.hour = int(txt)
                    self.mints = 0
                    self.ss = 0
                    if int(txt)>=10:
                        hour = '%s' % (int(txt))
                    else:
                        hour = '0%s' % (int(txt))
                    mint = '00'
                    ss = '00'
                if txt <1:
                    if mis >=1:
                        self.hour = 0
                        self.mints = int(mis)
                        self.ss = 0
                        hour = '00'
                        if int(mis) >= 10:
                            mint = '%s' % (int(mis))
                        else:
                            mint = '0%s' % (int(mis))
                        ss = '00'
                    else:
                        self.hour = 0
                        self.mints = 0
                        self.ss = mis*60
                        hour = '00'
                        mint = '00'
                        if int(mis * 60) >= 10:
                            ss = '%s' % (int(mis * 60))
                        else:
                            ss = '0%s' % (int(mis * 60))

                str = hour +':' + mint +':'+ ss
                self.lcdNumber.display(str)
                self.timer = progress_thread.Progress_Thread(int(self.timetotal))
                self.timer.signal.connect(self.handle_time)  # 计时结束调用operate()方法
                self.timer.start()
                self.pushButton_4.setEnabled(False)
                self.pushButton_5.setEnabled(True)
                self.pushButton_6.setEnabled(True)
        except Exception as e:
            print(e)
            pass
    #停止，取消
    def stopTime(self):
        try:
            ctypes.windll.kernel32.TerminateThread(self.timer.handle, 0)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)
            os.system('shutdown -a')
        except Exception as e:
            pass
     #暂停
    def suspended(self):
        try:
            if self.timer.handle == -1:
                return print('handle is wrong')
            SuspendThread(self.timer.handle)
            os.system('shutdown -a')
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(True)
        except Exception as e:
            print(e)
            pass
    #恢复
    def restore(self):
        try:
            if self.timer.handle == -1:
                return print('handle is wrong')
            ResumeThread(self.timer.handle)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(False)
        except Exception as e:
            print(e)
            pass
    #强制关闭
    # def closeEvent(self, event):
    #     if self.timer.isRunning():
    #         self.timer.quit()
    #         # self._thread.terminate()# 强制
    #     self.timer = None
    #     super(Dialog_Menu, self).closeEvent(event)

    #


    def closeshutdow(self):
        try:
            os.system('gpedit.msc')

            IP = ''
            content ='我要关闭你的电脑'
            os.system('shutdown -s -t 1 -m \\%s -c "%s" -f' %(IP,content))
        except Exception as e:
            pass
    def handle_time(self,i):
        try:
            self.step +=i
            if self.step >=self.timetotal:
                os.system('shutdown -s -t 1')
                # print('关机')
            if self.ss>0:
                self.ss -= i
            if self.ss <=0:
                if self.mints > 0:
                    self.mints -= i
                    self.ss = 60-i
                if self.mints <=0:
                    if self.hour >0:
                        self.hour -=i
                        self.mints = 60-i

            if self.hour>=10:
                hour = '%s'%self.hour
            else:
                hour = '0%s' % self.hour
            if self.mints >= 10:
                mm = '%s' % self.mints
            else:
                mm = '0%s' % self.mints
            if self.ss >= 10:
                ss = '%s' % self.ss
            else:
                ss = '0%s' % self.ss

            str = hour + ':'+mm+':'+ss

            self.lcdNumber.display(str)

        except Exception as e:
            pass

    def dialog_msg(self,msg):
        try:
            text = (msg[0],msg[0], msg[1])  # 任意颜色
            if self.radioButton.isChecked():
                word = '<span style=\" color:rgb%s;\">颜色代码:rgb%s;%s\n</span>' % text
            if self.radioButton_2.isChecked():
                word = '<span style=\" color:%s;\">颜色代码:%s;%s\n</span>' % text
            self.textBrowser.append(word)
            self.textBrowser.moveCursor(self.textBrowser.textCursor().End)
        except Exception as e:
            pass
    def changColor(self,num):
        try:
            if num == 1:
                color = QColorDialog.getColor(Qt.green)  # 参数Qt.blue：调色盘选取颜色默认停在蓝色
                if color.isValid():
                    self.frame.setPalette(QPalette(color))
                    self.pen.setColor(color)  # 设置笔颜色
                    if self.radioButton.isChecked():
                        self.dialogsing_msg.emit([color.getRgb(),'成功提示'])
                    if self.radioButton_2.isChecked():
                        self.dialogsing_msg.emit([color.name(), '成功提示'])

                else: #如果点击取消,设置原来的颜色
                    self.frame.setPalette(QPalette(Qt.green))

            if num == 2:
                color = QColorDialog.getColor(Qt.red)
                if color.isValid():
                    self.frame_2.setPalette(QPalette(color))  # 设置控件背景颜色
                    self.pen1.setColor(color)  # 设置笔颜色
                    if self.radioButton.isChecked():
                        self.dialogsing_msg.emit([color.getRgb(), '错误提示'])
                    if self.radioButton_2.isChecked():
                        self.dialogsing_msg.emit([color.name(), '错误提示'])

                else:
                    self.frame_2.setPalette(QPalette(Qt.red))
            if num == 3:
                color = QColorDialog.getColor(Qt.black)
                if color.isValid():
                    self.frame_3.setPalette(QPalette(color))  # 设置控件背景颜色
                    self.pen2.setColor(color)  # 设置笔颜色
                    if self.radioButton.isChecked():
                        self.dialogsing_msg.emit([color.getRgb(), '默认字体'])
                    if self.radioButton_2.isChecked():
                        self.dialogsing_msg.emit([color.name(), '默认字体'])

                else:
                    self.frame_3.setPalette(QPalette(Qt.black))
        except Exception as e:
            pass

    def csrenWind(self):
        try:
            # open_flie.spoton() #获取鼠标坐标
            # self.prinstPids()
            # self.screenshots()
            # time.sleep(1)
            self.imgs()
            # self.drwa()
        except Exception as e:
            pass

    def drwa(self):
        try:
            m = MoveTo()
            k = Thekeys()
            left, top, right, bottom = self.getWindow()  # 获取微信在屏幕的坐标

            m.position = (left+31,top+144)
            m.click(Button.left)
            time.sleep(1)

            m.position = (left+62,top+100)
            m.scroll(0,-50)
            time.sleep(1)
            self.screenshots()
        except Exception as e:
            pass
    # 255 - 310 = 45
    # 256 -367 = -111
    # 250-318 = -78
    # 595 - 533 = 62
    # 533 - 845 = -312
    # 256  - 400 = 144
    # 530 - 561 = 31
    def screenshots(self):
        try:
            # top:161
            # 行高 60
            # 225 416 475
            # BASE_DIR = os.path.dirname(__file__)
            left, top, right, bottom = self.getWindow()  # 获取微信在屏幕的坐标
            #pic = ImageGrab.grab((left+62, top+61, left+312, bottom)) 截取整列
            pic = ImageGrab.grab((left+62, top+161, left+312, top+221)) #截取某个联系人
            timestr = str(datetime.datetime.now()).replace(':', '_')
            fn = "D:\\Pictures\\Camera Roll\\" + timestr + ".png"
            # print(BASE_DIR)
            # print(fn)
            pic.save(fn)
            # print(img_ready)
            self.fnPath = fn
            time.sleep(0.5)

            self.imgs()
            # print(pytesseract.image_to_string(img))
            # img.show()
            # print(fn)
            # zh = pytesseract.image_to_string(img,lang="chi_sim") # 中文识别有时不是特别准确，识别结果中间有空格

            # 也只有识别规矩的英文和数字了，可以用来破解低级验证码

            # img_ready.show()
        except Exception as e:

            pass

    def print_preds(pred):
        pred = [''.join(line_p) for line_p in pred]
        print("Predicted Chars:", pred)

    def cal_score(preds, expected):
        if len(preds) != len(expected):
            return 0
        total_cnt = 0
        total_dist = 0
        for real, pred in zip(expected, preds):
            pred = ''.join(pred)
            distance = Levenshtein.distance(real, pred)
            total_dist += distance
            total_cnt += len(real)

        return 1.0 - float(total_dist) / total_cnt

    def simpleocr(self):
        try:
            ocr = CnOcr()
            img_fp = os.path.join("Qdialog/", "2021-01-03 20_08_07.398045.png")
            pred = ocr.ocr(img_fp)
            print('\n')
            self.print_preds(pred)
            # assert cal_score(pred, expected) >= 0.9

            img = mx.image.imread(img_fp, 1)
            pred = ocr.ocr(img)
            self.print_preds(pred)
            # assert cal_score(pred, expected) >= 0.9

            img = mx.image.imread(img_fp, 1).asnumpy()
            pred = ocr.ocr(img)
            self.print_preds(pred)
            # assert cal_score(pred, expected) >= 0.9
        except Exception as e:
            pass
    def single_line(self):
        try:
            ocr = CnOcr()
            img_fp = os.path.join("Qdialog/", "2021-01-03 20_08_07.398045.png")
            pred = ocr.ocr_for_single_line(img_fp)
            print('\n')
            self.print_preds(pred)
            # assert cal_score([pred], expected) >= 0.9

            img = mx.image.imread(img_fp, 1)
            pred = ocr.ocr_for_single_line(img)
            self.print_preds(pred)
            # assert cal_score([pred], expected) >= 0.9

            img = mx.image.imread(img_fp, 1).asnumpy()
            pred = ocr.ocr_for_single_line(img)
            self.print_preds(pred)
            # assert cal_score([pred], expected) >= 0.9

            img = np.array(Image.fromarray(img).convert('L'))
            assert len(img.shape) == 2
            pred = ocr.ocr_for_single_line(img)
            self.print_preds(pred)
            # assert cal_score([pred], expected) >= 0.9

            img = np.expand_dims(img, axis=2)
            assert len(img.shape) == 3 and img.shape[2] == 1
            pred = ocr.ocr_for_single_line(img)
            self.print_preds(pred)
            # assert cal_score([pred], expected) >= 0.9
        except Exception as e:
            pass

    def imgs(self):
        try:

            # path = os.path.join("Qdialog/", "1609857213.png")
            path = os.path.join("Qdialog/", "2021-01-03 20_08_07.398045.png")
            # imgss = Image.open(path)
            ocr = CnOcr()
            # img_fp = 'examples/multi-line_cn1.png'
            img = mx.image.imread(path,1).asnumpy()
            print(ocr.ocr_for_single_line(img))

            line_imgs = line_split(img, blank=True)
            line_img_list = [line_img for line_img, _ in line_imgs]
            res = ocr.ocr_for_single_lines(line_img_list)
            print("Predicted Chars:", res)

        except Exception as e:
            print(e)
            pass