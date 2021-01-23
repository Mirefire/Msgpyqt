from ui import MainView
import socket,re,sys,threading

class Tcp_client(MainView.Ui_MainWindow):
    def __init__(self):
        super(Tcp_client, self).__init__()
        self.tcp_socket = None
        self.server_threading = None
        self.client_threading = None
        self.client_socket_list = list()

        self.link = False

    def tcp_client_start(self):
        """
        功能函数，TCP客户端连接其他服务端的方法
        :return:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            input_address = (str(self.lineEdit_4.text()), int(self.lineEdit_3.text()))
        except Exception as res:
            self.signal_write_msg.emit('请检查目标IP，目标端口\n')
        else:
            try:
                self.signal_write_msg.emit('正在连接目标服务器\n')
                self.tcp_socket.connect(input_address)
            except Exception as re:
                self.signal_write_msg.emit('无法连接目标服务器\n')
            else:
                self.client_threading = threading.Thread(target=self.tcp_client_threading, args=(input_address,))
                self.client_threading.start()
                self.signal_write_msg.emit('TCP客户端已连接TCP服务端\n')
                self.plainTextEdit.setReadOnly(False)

    def tcp_client_threading(self, address):
        """
        功能函数，用于TCP客户端创建子线程的方法，阻塞式接收
        :return:
        """
        while True:
            text_msg = self.tcp_socket.recv(1024)
            if text_msg:
                msg = text_msg.decode('utf-8')
                msg = 'TCP服务端:%s\n' % msg
                self.signal_write_msg.emit(msg)
            else:
                self.tcp_socket.close()
                self.reset()
                self.signal_write_msg.emit('从服务器断开连接\n')
                break
