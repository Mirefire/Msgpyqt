from ui import MainView
from Logiclayer import progress_thread
import pyperclip as p
import psutil,os,subprocess,win32gui,time,threading,win32con
import winreg
from tqdm import tqdm
from pynput.mouse import Button, Controller as c1
from pynput.keyboard import Key, Controller as c2
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import *


class Auto_resp(MainView.Ui_MainWindow):
    def __init__(self):
        super(Auto_resp,self).__init__()
        self.Progesstime = QBasicTimer()
        self.step = 0
        self.progress_th = None
        self.t=None
        self.send_thread = None
        self.openWeixin_th = None
        self.ishow = False
        self.path = None

    def progress_start(self):
        try:
            self.t = int(self.lineEdit_3.text())
            self.progressBar.setMinimum(0)
            self.progressBar.setMaximum(self.t)
        except Exception as re:
            self.signal_write_msg.emit('请输入时间\n')
        else:
            self.progress_th = progress_thread.Progress_Thread(self.t)
            self.progress_th.start()
            self.progress_th.signal.connect(self.callback)


    def callback(self,i):
        self.progressBar.show()
        self.step +=i
        if self.step>=self.t:
            self.rpss()
            self.progressBar.hide()
            self.progressBar.reset()
            self.step=0
        else:
            self.progressBar.setValue(self.step)
    #移动鼠标
    def send(self):
            m = c1()
            k = c2()

            left, top, right, bottom = self.getWindow()
            name = str(self.lineEdit_2.text())
            content = str(self.plainTextEdit.toPlainText())
            m.position = (left + 100, top + 25)
            m.click(Button.left, 1)
            time.sleep(1)
            k.type(name)
            # time.sleep(2)
            # k.type([Key.enter])
            k.touch(Key.enter, True)
            time.sleep(1)
            # 打开聊天窗口
            # 1034.369   1247.425
            m.position = (left + 100, top + 65)
            m.click(Button.left, 1)
            time.sleep(1)
            # 复制文字到输入框
            m.position = (left + 345, bottom - 90)
            m.click(Button.left, 1)
            # time.sleep(0.5)
            k.type(content)
            # p.copy(content)
            time.sleep(1)
        # 粘贴发送文本
        #     with k.pressed(Key.ctrl_l):
        #         k.touch('v', True)
            k.touch(Key.enter, True)
            # 关闭微信窗口
            time.sleep(1)

            m.position = (left + 830, top + 10)
            m.click(Button.left, 1)

        # 反馈状态  可以用easygui写一个窗口展示

        # now = time.strftime('%Y.%m.%d %H:%M:%S')
        # print('Completed at {}'.format(now))
        # msg = '消息已发送'
        # g.msgbox(msg, title=now)
        #打开微信
    # def copy_file(self,i):
    #     self.progressBar.show()

    def rpss(self):
        if self.ishow:
            os.startfile(self.path)
            time.sleep(1)
            self.send_thread = threading.Thread(target=self.send)
            self.send_thread.start()
        else:
            os.startfile(self.path)

    # self.SearchWeChat()
    def seachfill(self):
        try:
            self.openWeixin_th = threading.Thread(target=self.SearchWeChat)
        except Exception as res:
            pass

    def SearchWeChat(self):
        self.prinstPids()
        if not self.ishow:
            self.RegistryKey()

    def RegistryKey(self):
        sub_key = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall',
                   r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
        software_name = []
        for i in sub_key:
            listKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i, 0, winreg.KEY_ALL_ACCESS)
            for j in range(winreg.QueryInfoKey(listKey)[0] - 1):
                try:
                    key_name = winreg.EnumKey(listKey, j)

                    key_path = i + '\\' + key_name
                    if str(key_name) == 'WeChat':
                        print('还没打开微信')
                        self.ishow = False
                        each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
                        key_path, regtype = winreg.QueryValueEx(each_key, 'InstallLocation')
                        path = key_path + '\\' + key_name + '.exe'
                        self.path = path
                        break
                except Exception as e:
                    pass
    def prinstPids(self):
        pids = psutil.pids()
        for pid in pids:
            try:
                p = psutil.Process(pid)
                if p.name() == 'WeChat.exe':
                    # print('已打开微信了')
                    # self.ishow = True #判定是否已经打开微信
                    # cmd = 'wmic process where "name=\'%s\'" get ExecutablePath' % p.name()
                    # proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    # filePath = proc.stdout.readlines()[1]
                    # key = filePath.strip().decode('utf-8')
                    os.startfile(p.exe())
                    # self.path = key
                    break
            except Exception as e:
                pass

    #获取窗口位置
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
                        # win32gui.SendMessage(h, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)
                        # # 发送还原最小化窗口的信息
                        win32gui.SetForegroundWindow(h)
                        return postion

    def sendtime(self):
        '''任务进度条'''
        t = int(self.lineEdit_3.text())
        with tqdm(total=t) as bar:
            for i in range(t):
                bar.update(1)
                time.sleep(1)