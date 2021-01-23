from ui import MainView
from Logiclayer import stop_threading

import socket,re,sys,threading,json

class Tcp_server(MainView.Ui_MainWindow):
    def __init__(self):
        super(Tcp_server,self).__init__()

        self.tcp_socket = None
        self.server_threading = None
        self.client_threading = None
        self.client_socket_list = list()

        self.link = False

    def tcp_server_start(self):
        self.pushButton_3.setEnabled(True)

        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 取消主动断开连接四次握手后的TIME_WAIT状态
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 设定套接字为非阻塞式
        self.tcp_socket.setblocking(False)

        try:
            # input_port = (str(self.lineEdit_2.text()),int(self.lineEdit_3.text()))
            port = int(self.lineEdit_3.text())
            self.tcp_socket.bind(('', port))
        except Exception as res:
            self.signal_write_msg.emit('请检查端口号\n')
        else:
            self.tcp_socket.listen()
            self.server_threading = threading.Thread(target=self.tcp_server_threading)
            self.server_threading.start()
            self.signal_write_msg.emit('TCP服务端正在监听端口:%s\n' % port)

    def tcp_server_threading(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                client_socket, client_address = self.tcp_socket.accept()
            except Exception as res:
                pass
                # time.sleep(0.001)
            else:
                # 将创建的客户端套接字存入列表
                self.client_socket_list.append((client_socket, client_address))
                self.signal_write_msg.emit('TCP服务端已连接TCP客户端\n')
                self.plainTextEdit.setReadOnly(False)
            for client, address in self.client_socket_list:
                try:
                    text_msg = client.recv(1024)
                except Exception as ret:
                    msg = "%s,%s,%s,%s,%s" % ret.args
                    dum = msg.split(',')
                    if int(dum[0]) == 10054:
                        client.close()
                        self.pushButton_3.setEnabled(False)
                        self.signal_write_msg.emit('TCP客户端已断开\n')
                        break
                    else:
                        pass
                else:
                    if text_msg:
                        msg = text_msg.decode('utf-8')
                        msg = 'TCP客户端:%s\n' % msg
                        self.signal_write_msg.emit(msg)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))


