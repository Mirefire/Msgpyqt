from ui import MainView
from Logiclayer import stop_threading
import sys,re,threading,socket
from PyQt5.QtWidgets import *

class Web_server(MainView.Ui_MainWindow):
    def __init__(self):
        super(Web_server, self).__init__()
        self.tcp_socket = None
        self.sever_th = None
        self.web_dir = None
        self.web_dir_type = None
        self.client_socket_list = list()

        # web_tcp **************************************************

    def web_server_start(self):
            """
            功能函数，WEB服务端开启的方法
            :return: None
            """
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 取消主动断开连接四次握手后的TIME_WAIT状态
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # 设置套接字为非阻塞式
            self.tcp_socket.setblocking(False)
            try:
                input_port = int(self.lineEdit_3.text())
                self.tcp_socket.bind(('', input_port))
            except Exception as ret:
                self.signal_write_msg.emit('请检查端口号\n')
            else:
                self.tcp_socket.listen()
                self.server_threading = threading.Thread(target=self.web_server_threading)
                self.server_threading.start()
                self.signal_write_msg.emit('WEB服务端正在监听端口:%s\n' % input_port)

    def web_server_threading(self):
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
                    # time.sleep(0.01)
                    pass
                else:
                    client_socket.setblocking(False)
                    self.client_socket_list.append((client_socket, client_address))
                    msg = 'WEB服务端已连接TCP客户端\n'
                    self.signal_write_msg.emit(msg)
                for client, address in self.client_socket_list:
                    try:
                        recy_msg = client.recv(1024)
                    except Exception as ret:

                        pass
                    else:
                        if recy_msg:
                            if self.comboBox == 4:
                                txt = recy_msg.decode('utf-8')
                                txt_lines = txt.splitlines()
                                file = re.match(r"[^/]+(/[^ ]*)", txt_lines[0])
                            else:
                                file = recy_msg.decode('utf-8')
                            msg = 'TCP客服端:%s\n' % file
                            self.signal_write_msg.emit(msg)
                        else:
                            client.close()
                            self.client_socket_list.remove((client, address))
    def web_send(self):
        """
        WEB服务器发送消息的方法
        :return: None
        """

        try:
            flie_name = re.match(r'[^.]+\.(.*)$', self.web_dir).group(0)
            header,boby = self.web_send_file(flie_name)
            print(boby)
            for client, address in self.client_socket_list:
                client.send(header)
                client.send(boby)
            self.signal_write_msg.emit('WEB服务端发送:%s\n'% flie_name)
            self.plainTextEdit.setPlainText('')
        except Exception as ret:
            print(ret)
            self.signal_write_msg.emit("发送失败")
            self.plainTextEdit.setPlainText('')
    def choseFile(self):
        # 选择文件
        self.web_dir, self.web_dir_type = QFileDialog.getOpenFileName(self, '选择文件', '', "All Files (*)")
        flie = re.match(r'[^.]+\.(.*)$', self.web_dir).group(0)
        # print(self.web_dir_type)
        if self.web_dir:
            self.plainTextEdit.setPlainText('已选择文件:%s\n' % str(flie))

        # 发送文件

    def web_send_file(self, file_dir):
        # dir = file_dir
        # 根据返回文件的类型，制作相应的Content-Type数据
        file_header = self.web_header_file(file_dir)

        try:
            with open(file_dir, 'rb') as flie:
                file = flie.read()
                # print(dir)
        except Exception as ret:
            file = '你要的东西不见了'.encode('utf-8')
            response_header = ('HTTP/1.1 404 NOT FOUND\r\n' +
                               'Connection: Keep-Alive\r\n' +
                               'Content-Length: %d\r\n' % len(file) +
                               file_header +
                               '\r\n')
        else:
            response_header = ('HTTP/1.1 200 OK\r\n' +
                               'Connection: Keep-Alive\r\n' +
                               'Content-Length: %d\r\n' % len(file) +
                               file_header +
                               '\r\n')
        response_body = file_dir.encode('utf-8')
        return response_header.encode('utf-8'), response_body

        # 设置头部

    @staticmethod
    def web_header_file(file):
        """
        根据返回文件的类型，制作相应的Content-Type数据
        :param file: 历览器请求的路径
        :return: Content-Type数据
        """
        try:
            file_type = re.match(r'[^.]+\.(.*)$', file)
            file_type = file_type.group(1)
            if file_type == 'png' or file_type == 'jpg' or file_type == 'gif' or file_type == 'jpeg':
                file_header = 'Content-Type: image/%s; charset=utf-8\r\n' % file_type
            elif file_type == 'html':
                file_header = 'Content-Type: text/html; charset=utf-8\r\n'
            else:
                file_header = 'Content-Type: text/%s; charset=utf-8\r\n' % file_type
        except Exception as ret:
            file_header = 'Content-Type: text/%s; charset=utf-8\r\n' % file_type
            return file_header
        else:
            return file_header