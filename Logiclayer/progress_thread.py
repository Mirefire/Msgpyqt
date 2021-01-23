import time,ctypes,win32con
from PyQt5.QtCore import QThread,pyqtSignal,QTimer
from tqdm import tqdm
class Progress_Thread(QThread):
        signal = pyqtSignal(int)
        def __init__(self,num=True):
            super(Progress_Thread,self).__init__()
            self.num = num
            self.handle = -1
        def run(self):
            '''任务进度条'''
            try:
                self.handle =ctypes.windll.kernel32.OpenThread(
                win32con.PROCESS_ALL_ACCESS, False, int(QThread.currentThreadId()))
            except Exception as e:
                pass
            else:
                with tqdm(total=self.num) as bar:
                    for i in range(self.num):
                        # print(i)
                        bar.update(1)
                        self.signal.emit(1)
                        time.sleep(1)



