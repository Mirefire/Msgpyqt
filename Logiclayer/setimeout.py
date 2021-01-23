import time
import pyperclip as p
import easygui as g
from tqdm import tqdm
from pynput.mouse import Button, Controller as c1
from pynput.keyboard import Key, Controller as c2
from Logiclayer import open_flie

m = c1()
k = c2()


# time.sleep(3)
# print('鼠标的位置:{}'.format(m.position))

def send(obj, ms):
    # # 单击微信图标
    # m.position = (273, 751)  # print(m.position)获取图标位置
    #
    # m.click(Button.left, 1)
    # time.sleep(1.5)
    # 单击搜索框
    #648.302,798.302   886 187
    # if                    503
    # 100,25,58             887   682 92
    # 60,175.237 58 25 140  384.590.  870.193
    #914 1256
    left, top, right, bottom = open_flie.getWindow()
    # print(postion)

    m.position = (left+100, top+25)
    m.click(Button.left, 1)
    time.sleep(1)
    # 搜索对象
    k.type(obj)
    # p.copy(obj)
    # with k.pressed(Key.ctrl_l):
    #     k.touch('v', True)
    time.sleep(1.5)
    k.touch(Key.enter, True)
    time.sleep(1)
    # 打开聊天窗口
    #1034.369   1247.425
    m.position = (left+100, top+65)
    m.click(Button.left, 1)
    # time.sleep()
    # 复制文字到输入框
    m.position = (left+345, bottom-90)
    m.click(Button.left, 1)
    # time.sleep(0.5)
    k.type(ms)
    time.sleep(1)
    # 粘贴发送文本
    # with k.pressed(Key.ctrl_l):
    #     k.touch('v', True)
    k.touch(Key.enter, True)
    # 关闭微信窗口
    time.sleep(.1)

    m.position = (left+830, top+10)
    m.click(Button.left, 1)
    # 反馈状态  可以用easygui写一个窗口展示

    # now = time.strftime('%Y.%m.%d %H:%M:%S')
    # print('Completed at {}'.format(now))
    # msg = '消息已发送'
    # g.msgbox(msg, title=now)


def sendtime(t):
    '''任务进度条'''
    with tqdm(total=t) as bar:
        for i in range(t):
            bar.update(1)
            time.sleep(1)

22

def main():
    obj = input('Object：')
    ms = input('content：')
    t = int(input('Scheduled(Example:30):'))  # 多少秒之后发送
    open_flie.prinstPids()
    sendtime(t)
    send(obj, ms)


if __name__ == '__main__':
    main()