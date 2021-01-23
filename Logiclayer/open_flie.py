import psutil,os,subprocess,pyautogui,win32gui,win32con,time,winreg

def prinstPids():
    pids = psutil.pids()
    # print(pids)
    for pid in pids:
        try:
            p = psutil.Process(pid)
            if p.name() == 'WeChat.exe':
                # cmds = 'wmic process where "name like \'%s\'" get processid,commandline' % p.name()
                # cmd = 'wmic process where "name=\'%s\'" get ExecutablePath'% p.name()
                cmd = 'wmic process where "name=\'%s\'" get ExecutablePath' % p.name()
                # print(cmd)
                proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                filePath = proc.stdout.readlines()[1]
                key = filePath.strip().decode('utf-8')

                os.startfile(key)
                time.sleep(1)
            else:
                print('121212')
                break
                # getWindow()
                # print(filePath)
                # print(key)
        except Exception as e:
            print(e)
            pass
def getWindow():
    hwnd_title = {}
    def get_all_hwnd(hwnd, mouse):
        if (win32gui.IsWindow(hwnd)
                and win32gui.IsWindowEnabled(hwnd)
                and win32gui.IsWindowVisible(hwnd)):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t:
            if h == 132200:
                postion =  win32gui.GetWindowRect(h)
                return postion


def setWindow(bid):
    x = 1021
    y = 640
    # 根据横纵坐标定位光标
    # win32api.SetCursorPos([x, y])
    # # 给光标定位的位置进行单击操作（若想进行双击操作，可以延时几毫秒再点击一次）
    # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP | win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # # 给光标定位的位置进行右击操作
    # win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP | win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    #
    # 获取标题
    title = win32gui.GetWindowText(bid)  # jbid为句柄id
    # 获取类名
    clsname = win32gui.GetClassName(bid)

    #根据句柄获取窗口位置
    postion = win32gui.GetWindowRect(bid)
    #根据句柄将窗口放在最前
    win32gui.SetForegroundWindow(bid)


def spoton():
    try:
        while 1:
            x, y = pyautogui.position()
            print(x, y)
    except:
        pass
if __name__ == '__main__':
    # RegistryKey()
    prinstPids()