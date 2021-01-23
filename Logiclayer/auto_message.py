import sys,time,threading,os,psutil,winreg,win32,subprocess,win32gui,re,win32con
from pynput.mouse import Button, Controller as MoveTo
from pynput.keyboard import Key, Controller as Thekeys

from Logiclayer import progress_thread
from ui import createView
from Logiclayer.plugin import spscheduler
class Auto_msg(createView.Ui_MainWindow,spscheduler.spsch_eduler):
    def __init__(self):
        super(Auto_msg, self).__init__()
        self.timing = 0
        self.endface = 0
        self.progeress_thread = None
        self.send_thread = None
        self.progeress_step = 0
        self.Weixinpath = None
        self.dataList = list()
        opsen = threading.Thread(target=self.SeerIE)
        opsen.start()
    def SeerIE(self):
        try:
            pids = psutil.pids()
            for pid in pids:
                try:
                    software = psutil.Process(pid)
                    # re.search(name,software.name())
                    # if bool(re.search(name,'微信weixin')):
                    if software.name() == 'WeChat.exe' and software.status() =='running':
                            #获取路径方法一
                            # cmd = 'wmic process where "name=\'%s\'" get ExecutablePath' % software.name()
                            # proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                            # filePath = proc.stdout.readlines()[1]
                            # key = filePath.strip().decode('utf-8')
                            # 获取方法二
                        #找到就跳出你

                        # print(software.exe())
                        self.Weixinpath = software.exe()

                        break
                        # return software.exe()
                except Exception as k:
                    pass

        except Exception as e:
            pass

        # 获取窗口位置
    def getWindow(self):
        try:
            hwnd_title = {}
            def get_all_hwnd(hwnd, mouse):
                if (win32gui.IsWindow(hwnd)
                        and win32gui.IsWindowEnabled(hwnd)
                        and win32gui.IsWindowVisible(hwnd)):
                    hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
        except Exception as res:
            pass
        else:
            win32gui.EnumWindows(get_all_hwnd, 0)
            for h, t in hwnd_title.items():
                if t:
                    if t == '微信':
                        postion = win32gui.GetWindowRect(h)
                        win32gui.SetForegroundWindow(h)
                        # win32gui.SendMessage(handle, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                        # # 发送还原最小化窗口的信息
                        # win32gui.SetForegroundWindow(handle)
                        return postion
        # 发送消息
    def drawPoniter(self,popele):
        """
        :param popele: 接受人
        :return: null
        """
        content = str(self.msgedit.toPlainText())  # 发送内容
        try:
            m = MoveTo()
            k = Thekeys()
            left, top, right, bottom = self.getWindow() #获取微信在屏幕的坐标
            #微信搜索框  距离最最左边是100左右，距离最上面25左右
            m.position = (left+100,top+25)
            m.click(Button.left,1)
            time.sleep(1)

            #复制微信名称 并回车
            k.type(popele)
            k.touch(Key.enter,True)
            time.sleep(1)

            #点击搜索的微信名称
            m.position = (left+100,top+65)
            m.click(Button.left,1)
            time.sleep(1)

            #复制要发送的内容
            # 复制文字到输入框
            m.position = (left + 345, bottom - 90)
            m.click(Button.left, 1)
            k.type(content)
            k.touch(Key.enter,True)
            time.sleep(1)
            #判定是否是最后一项
            dataleng = len(self.dataList)-1
            if self.endface == dataleng:
                #关闭微信
                m.position = (left+830,top+10)
                m.click(Button.left,1)
                time.sleep(1)
                self.signal_write_msg.emit('发送完毕')
        except Exception as e:
            pass

    def send_start(self):
        self.timing = int(self.lineEdit.text())
        try:
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(self.timing)
        except Exception as e:
            pass
        else:
            self.progeress_thread = progress_thread.Progress_Thread(self.timing)
            self.progeress_thread.start()
            self.progeress_thread.signal.connect(self.callback)

    def callback(self,i):
        t = int(i)
        try:
            self.progressBar.show()
            self.progeress_step +=t
            self.progressBar.setValue(self.progeress_step)
            if self.progeress_step >= self.timing:
                self.progressBar.hide()
                self.progressBar.reset()
                self.progeress_step = 0
                os.startfile(self.Weixinpath)
                self.signal_write_msg.emit('启动程序完毕')
                time.sleep(1)
                self.runDreaw()
        except Exception as e:
            pass

    def runDreaw(self):
        interTime = int(self.lineEdit_2.text())
        try:
            for j, k in enumerate(self.dataList):
                #获取最后发送最后一项下标
                if j == 0:
                    #
                    self.drawPoniter(k[0])
                    self.endface = j
                    self.signal_write_msg.emit('正在向%s发送消息' % k[0])
                else:
                    time.sleep(interTime)
                    self.endface = j
                    #
                    self.drawPoniter(k[0])
                    self.signal_write_msg.emit('正在向%s发送消息' % k[0])
                # print(k[0])
        except Exception as e:
            print(e)
            pass

    #打开微信
    def openWeixin(self,listdata):
        try:
            self.signal_write_msg.emit('正在启动程序')
            self.send_start()
            self.dataList = listdata

        except Exception as e:
            pass


