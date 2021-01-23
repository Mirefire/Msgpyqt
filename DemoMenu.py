import sys,ctypes,inspect,time,socket,threading,os,re
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from ui import MainView
from Logiclayer import tcp_server,tcp_client,web_server,auto_response
from Logiclayer import stop_threading
from pynput.keyboard import Key,Controller

class Tcp_nhs(QMainWindow,tcp_server.Tcp_server,tcp_client.Tcp_client,web_server.Web_server,auto_response.Auto_resp):
    signal_write_msg = QtCore.pyqtSignal(str)
    _translate = QtCore.QCoreApplication.translate
    def __init__(self,parent = None):
        super(Tcp_nhs,self).__init__(parent)

        self.tcp_socket = None
        self.udp_socket = None
        self.setupUi(self)
        self.defaultInit()
        self.connect()
        self.Setsocket()


    def Setsocket(self):
        # 创建TCP/UDP套接字
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 将TCP套接字四次挥手后的TIME_WAIT状态取消
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 使用socket模块获取本机ip
        MY_IP = socket.gethostbyname(socket.gethostname())
        if self.comboBox.currentIndex() == 5:
            self.lineEdit_2.setText('')
        else:
            self.lineEdit_2.setText(str(MY_IP))

    def defaultInit(self):
        self.pushButton_3.setEnabled(False)
        self.pushButton_8.hide()
        self.plainTextEdit.setReadOnly(False)
        self.label_3.hide()
        self.lineEdit_4.hide()
        self.progressBar.hide()


    #绑定触发事件
    def connect(self):
        self.signal_write_msg.connect(self.write_msg)
        self.pushButton.clicked.connect(self.click_btn1)
        self.pushButton_2.clicked.connect(self.click_btn2)
        self.actioncs.triggered.connect(self.click_actioncs)
        self.actionout.triggered['bool'].connect(self.close)
        # self.actionxinjian.triggered.connect(self.createView)
        self.pushButton_3.clicked.connect(self.click_btn3)
        self.pushButton_4.clicked.connect(self.click_btn4)
        # self.pushButton5.clicked.connect(self.click_btn5)
        # self.pushButton_4.grabKeyboard(self.keycente)
        self.pushButton_6.clicked.connect(self.click_btn6)
        self.pushButton_8.clicked.connect(self.click_btn8)
        self.comboBox.currentIndexChanged.connect(self.click_box)

    def write_msg(self,msg):
        """
        功能函数，向接收区写入数据的方法
        信号-槽触发
        tip：PyQt程序的子线程中，使用非规定的语句向主线程的界面传输字符是不允许的
        :return: None
        """
        self.textBrowser_2.insertPlainText(msg)
        self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)
    #重新获取ip
    def click_btn1(self):
        self.lineEdit_2.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            MY_IP = s.getsockname()[0]
            self.lineEdit_2.setText(str(MY_IP))
        except Exception as error:
            try:
                MY_IP = socket.gethostbyname(socket.gethostname())
                self.lineEdit_2.setText(str(MY_IP))
            except Exception as err:
                self.signal_write_msg.emit("无法获取ip，请连接网络！\n")
        finally:
            s.close()
    #连接网络
    def click_btn2(self):

        if self.comboBox.currentIndex() == 0:
            self.tcp_server_start()
        if self.comboBox.currentIndex() == 1:
            self.tcp_client_start()
        if self.comboBox.currentIndex() == 4:
            self.web_server_start()
        self.link = True
        self.pushButton_3.setEnabled(True)

    # 断开网络
    def click_btn3(self):
        self.close_socket()
        self.link = False
    # 重置数据
    def reset(self):
        """
        功能函数，将按钮重置为初始状态
        :return:None
        """
        self.link = False
        self.client_socket_list = list()
        self.pushButton_3.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.plainTextEdit.setReadOnly(False)

    def close_socket(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox.currentIndex() == 0 or self.comboBox.currentIndex() == 1:
            self.tcp_close()
        if self.comboBox.currentIndex() == 2 or self.comboBox.currentIndex() == 3:
            self.udp_close()
        if self.comboBox.currentIndex() == 4:
            self.web_close()
        self.reset()

    def tcp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox.currentIndex() == 0:
            try:
                for client, address in self.client_socket_list:
                    client.close()
                self.tcp_socket.close()
                if self.link is True:
                    self.signal_write_msg.emit('已断开网络\n')
            except Exception as ret:
                pass
        if self.comboBox.currentIndex() == 1:
            try:
                self.tcp_socket.close()
                if self.link is True:
                    self.signal_write_msg.emit('已断开网络\n')
            except Exception as ret:
                pass
        try:
            stop_threading.stop_thread(self.server_threading)
        except Exception:
            pass
        try:
            stop_threading.stop_thread(self.client_threading)
        except Exception:
            pass

    def udp_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        if self.comboBox.currentIndex() == 2:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        if self.comboBox.currentIndex() == 3:
            try:
                self.udp_socket.close()
                if self.link is True:
                    msg = '已断开网络\n'
                    self.signal_write_msg.emit(msg)
            except Exception as ret:
                pass
        try:
            stop_threading.stop_thread(self.server_threading)
        except Exception:
            pass
        try:
            stop_threading.stop_thread(self.client_threading)
        except Exception:
            pass

    def web_close(self):
        """
        功能函数，关闭网络连接的方法
        :return:
        """
        try:
            for client, address in self.client_socket_list:
                client.send('WEB服务端已断开网络\n')
                client.close()
            self.tcp_socket.close()
            if self.link is True:
                msg = '已断开网络\n'
                self.signal_write_msg.emit(msg)
        except Exception as ret:
            pass
        try:
            stop_threading.stop_thread(self.server_threading)
        except Exception:
            pass
        try:
            stop_threading.stop_thread(self.client_threading)
        except Exception:
            pass
    #发送消息
    def click_btn4(self):
        if self.comboBox.currentIndex() == 5:
           self.SearchWeChat()
           self.progress_start()
        elif self.link is False:
            self.signal_write_msg.emit( '请选择服务，并点击连接网络\n')
            self.plainTextEdit.setPlainText('')
        else:
            try:
                msg = (str(self.plainTextEdit.toPlainText())).encode('utf-8')
                txt = str(self.plainTextEdit.toPlainText())
                if self.comboBox.currentIndex() == 0:
                    for client,address in self.client_socket_list:
                        client.send(msg)
                    self.signal_write_msg.emit('TCP服务端:%s\n' % txt)
                    self.plainTextEdit.setPlainText('')
                if self.comboBox.currentIndex() == 1:
                    self.tcp_socket.send(msg)
                    self.signal_write_msg.emit('TCP客户端:%s\n' % txt)
                    self.plainTextEdit.setPlainText('')
                if self.comboBox.currentIndex() == 4:
                    self.web_send()

            except Exception as res:
                self.signal_write_msg.emit("发送失败,请查看网络\n")
                self.plainTextEdit.setPlainText('')


    # 清除信息
    def click_btn6(self):
        self.textBrowser_2.clear()
    # 选择服务端
    def click_box(self):
        self.pushButton_8.hide()
        self.lineEdit_3.setText('')
        self.plainTextEdit.setReadOnly(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton.setEnabled(True)
        if self.comboBox.currentIndex() == 0 or self.comboBox.currentIndex() == 2:
            self.label_3.hide()
            self.lineEdit_4.hide()
            self.label.setText(self._translate("TCP-UDP", "本地IP地址:"))
            self.label_2.setText(self._translate("TCP-UDP", "端口号:"))
        if self.comboBox.currentIndex() == 1 or self.comboBox.currentIndex() == 3:
            self.label_3.show()
            self.lineEdit_4.show()

            self.label.setText(self._translate("TCP-UDP", "本地IP地址:"))
            self.label_2.setText(self._translate("TCP-UDP", "目标端口:"))
        if self.comboBox.currentIndex() == 4:
            self.pushButton_8.show()
            self.plainTextEdit.setReadOnly(True)
            self.label_3.hide()
            self.lineEdit_4.hide()
            self.label.setText(self._translate("TCP-UDP", "本地IP地址:"))
            self.label_2.setText(self._translate("TCP-UDP", "端口号:"))
        if self.comboBox.currentIndex() == 5:
            self.pushButton.setEnabled(False)
            self.label.setText(self._translate("TCP-UDP", "微信名称:"))
            self.label_2.setText(self._translate("TCP-UDP", "倒计时（秒）:"))
            # self.plainTextEdit.setReadOnly(True)
            self.link = True
            self.lineEdit_2.setText('')
            self.label_3.hide()
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.lineEdit_4.hide()

    def textBrowser2(self):
        # self.textBrowser_2.insertPlainText(self.msg)
        print('ssssssss')
    # 查询端口
    def click_actioncs(self):
        self.Makeport()
    # def createView(self):
        # self.newView =Ui_MainWindow()
        # self.newView.setupUi()

    def Makeport(self):
        # port_list = []
        # port_dict = {"data": None}
        cmd = 'netstat -ano'
        local_ports = os.popen(cmd).readlines()
        for port in local_ports:
            self.signal_write_msg.emit(port.replace("\n", ""))

        local_ports.close()
            # pdict["TCP_PORT"] = port.replace("\n", "")
            # port_list.append(pdict)
        # port_dict["data"] = port_list
        # jsonStr = json.dumps(port_dict, sort_keys=True, indent=4)
        #
        # print(jsonStr)

        # 选择文件

    def click_btn8(self):
        self.choseFile()

    def keyPressEvent(self, event):
        # print(Qt.Key_Enter)
        # print(event.key())
        if event.key() == 16777220:
            print('sss')


# 线程
class StopThreading:
    """强制关闭线程的方法"""
    @staticmethod
    def _async_raise(tid, exc_type):
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exc_type):
            exc_type = type(exc_type)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exc_type))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Tcp_nhs()
    demo.show()
    sys.exit(app.exec_())