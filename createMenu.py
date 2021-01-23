
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from xlrd import *
import pandas as pd
import numpy as np
from Logiclayer import auto_message
from Logiclayer.plugin import spscheduler,createTif
from Qdialog import dialogMenu
from Commonly_used_tools import commonly_used_tools
class Create_mian(QMainWindow,auto_message.Auto_msg,spscheduler.spsch_eduler,createTif.Tif):
    signal_write_msg = pyqtSignal(object) #可以传输任何类型
    _translate = QCoreApplication.translate

    def __init__(self):
        super(Create_mian, self).__init__()
        self.setFixedSize(800,500)
        self.filepath = list()
        self.setupUi(self)
        self.setTaleWidget()
        self.connect()
        # self.SeerIE()
    #设置tableWidget 初始化
    def setTaleWidget(self):
        # self.setFrameShape(QFrame.NoFrame)  ##设置无表格的外框
        self.tableWidget.resizeColumnsToContents()  # 设置列宽高按照内容自适应
        self.tableWidget.resizeRowsToContents()  # 设置行宽和高按照内容自适应
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置只可以单选，可以使用ExtendedSelection进行多选
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置 不可选择单个单元格，只可选择一行。
        self.tableWidget.horizontalHeader().setSectionsClickable(False)  # 可以禁止点击表头的列
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置表格不可更改
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setStyleSheet(
            'QHeaderView::section{background:#ddd;border:none}')  # 设置表头的背景色为绿色
    # 绑定触发事件
    def connect(self):
        #搜索
        self.searchbtn.clicked.connect(self.searchBtn)
        #点击事件 添加个选中组件check 方法一
        self.tableWidget.clicked.connect(self.checkchange)
        # 全选
        self.radioAll.toggled.connect(self.allBtn)
        #清除
        self.clearbtn.clicked.connect(self.clear)
        #发送
        self.sendbtn.clicked.connect(self.send)
        #导入
        self.actiondao.triggered.connect(self.IntoBtn)
        #图片转tif
        self.actiontif.triggered.connect(self.Intotif)
        #设置
        self.setting.triggered.connect(self.set_Btn)
        # 文字转图片
        self.usetool.triggered.connect(self.userd_tool)
        #退出系统
        self.action_logu.triggered.connect(self.logout)
        #搜索框
        self.lineEdit_3.textChanged.connect(self.handleChanged)
        #发送消息
        self.signal_write_msg.connect(self.send_msg)

        self.textBrowser_2.setEnabled(True)
        self.progressBar.setValue(0)
        self.progressBar.hide()
    #截图
    def scremWindow(self):
        screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
        rect = QRect(self.startPoint, self.endPoint)
        outputRegion = screenshot.copy(rect)
        outputRegion.save('d:/sho54t.jpg', format='JPG', quality=100)
        self.close()


    def send_msg(self,msg):
        try:
            color = dialog.pen.color().name()
            if isinstance(msg,str) or isinstance(msg,int):
                text = (color, msg)
                word = '<span style=\" color:%s;\">%s\n</span>' % text
                self.textBrowser_2.append(word)
                self.textBrowser_2.moveCursor(self.textBrowser_2.textCursor().End)
        except Exception as e:
            pass
    def send(self):
        try:
           if self.radioAll.isChecked():  # 全选
               # 获取有多少行(左到右)
                table_rows = self.filepath.shape[0]
                table_rows_values = self.filepath
                table_rows_values_array = np.array(table_rows_values)
                # print(table_rows_values_array)
                table_rows_values_list = table_rows_values_array.tolist()
                # print(table_rows_values_list)
                self.openWeixin(table_rows_values_list)

           else:
               # 获取有多少行(左到右)
                table_rows = self.filepath.shape[0]
               # 获取有多少列（上到下）+1多加个操作列
                table_colunms = self.filepath.shape[1]
                table_list = []
                for i in range(table_rows):
                    state = self.tableWidget.item(i,table_colunms).checkState()
                    if state == 2:
                        table_rows_values = self.filepath.iloc[[i]]
                        table_rows_values_array = np.array(table_rows_values)
                        table_rows_values_list = table_rows_values_array.tolist()[0]
                        # print(table_rows_values_list)
                        table_list.append(table_rows_values_list)
                    # self.openWeixin(table_rows_values_list)

                self.openWeixin(table_list)
        except Exception as e:
            pass

    def clear(self):
        try:
            self.tableWidget.clear()
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels([''])
            self.filepath = list()
            self.radioAll.setChecked(False)
        except Exception as e:
            pass

    def allBtn(self):
        try:
            # 获取有多少行(左到右)
            table_rows = self.filepath.shape[0]
            # 获取有多少列（上到下）+1多加个操作列
            table_colunms = self.filepath.shape[1]
            if self.radioAll.isChecked(): #选中
                self.radioAll.setText(self._translate('','取消'))
                for i in range(table_rows):
                    self.tableWidget.item(i,table_colunms).setCheckState(Qt.Checked)
            else:
                self.radioAll.setText(self._translate('','全选'))
                for i in range(table_rows):
                    self.tableWidget.item(i, table_colunms).setCheckState(Qt.Unchecked)
        except Exception as e:
            pass
    #监听搜索框值变化
    def handleChanged(self,text):
        try:
            if text == '' and len(self.filepath)>0:
                table_rows = self.filepath.shape[0]
                # # 获取有多少列（上到下）+1多加个操作列
                table_colunms = self.filepath.shape[1] + 1
                # print(np.array(self.filepath))
                table_rows_values_array = np.array(self.filepath)
                self.tableWidget.clear()
                self.tableWidget.setHorizontalHeaderLabels(['微信名称', '备注', '操作'])
                self.tableWidget.setColumnCount(table_colunms)
                self.tableWidget.setRowCount(table_rows)
                for i,k in enumerate(table_rows_values_array):
                    for j,ds in enumerate(table_rows_values_array[i]):
                        name = QTableWidgetItem(str(ds))
                        name.setTextAlignment(Qt.AlignCenter)
                        name.setFlags(Qt.ItemIsEnabled)
                        self.tableWidget.setItem(i, j, name)
                        # 添加个选中组件check 方法一
                        check = QTableWidgetItem()
                        check.setFlags(Qt.ItemIsEnabled)
                        check.setTextAlignment(Qt.AlignCenter)
                        check.setCheckState(Qt.Unchecked)  # 把checkBox设为未选中状态
                        self.tableWidget.setItem(i, table_colunms - 1, check)  # 在(x,y)
        except Exception as e:
            pass


        #搜索
    def searchBtn(self):
        txt = str(self.lineEdit_3.text())
        try:
            # 获取有多少行(左到右)
            table_rows = self.filepath.shape[0]
            # # 获取有多少列（上到下）+1多加个操作列
            table_colunms = self.filepath.shape[1]+1
            # print(np.array(self.filepath))
            table_rows_values_array = np.array(self.filepath)
            for i,j in enumerate(table_rows_values_array):
                if j[0] == txt:
                    for k in range(table_colunms):
                        self.tableWidget.item(i, k).setBackground(QBrush(QColor(255, 0, 0)))

                        # 字体颜色（红色）
                        # self.tableWidget_Software.item(1, 0).setForeground(QBrush(QColor(255, 0, 0)))
                        # 背景颜色（红色）
                        # self.tableWidget_Software.item(1, 0).setBackground(QBrush(QColor(255, 0, 0)))
                    # self.tableWidget.clear()
                    # self.tableWidget.setColumnCount(table_colunms)
                    # self.tableWidget.setRowCount(1)
                    # self.tableWidget.setHorizontalHeaderLabels(['微信名称', '备注', '操作'])
                    # for e, k in enumerate(table_rows_values_array[i]):
                    #
                    #     name = QTableWidgetItem(str(k))
                    #     name.setTextAlignment(Qt.AlignCenter)
                    #     name.setFlags(Qt.ItemIsEnabled)
                    #     self.tableWidget.setItem(0, e, name)
                    #         # 添加个选中组件check 方法一
                    #     check = QTableWidgetItem()
                    #     check.setFlags(Qt.ItemIsEnabled)
                    #     check.setTextAlignment(Qt.AlignCenter)
                    #     check.setCheckState(Qt.Unchecked)  # 把checkBox设为未选中状态
                    #     self.tableWidget.setItem(0, table_colunms-1, check)  # 在(x,y)

        except Exception as e:
            pass
    #设置
    def set_Btn(self):
        try:
            dialog.dialogsing_msg.connect(self.get_dialog_msg)
            dialog.show()

        except Exception as e:
            pass

    def userd_tool(self):
        try:
            print(11)
            user_tool.show()
        except Exception as e:
            print(e)
            pass
    #获取子窗口的传参
    def get_dialog_msg(self,e):
        try:
            data = (e[0],e[1])
            # print(data)
        except Exception as ret:
            # print(ret)
            pass
        # print('data:%s' %data)

    #退出系统
    def logout(self):
        app = QApplication.instance()
        app.quit()

    #导入
    def IntoBtn(self):
        openfile_name, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Excel files(*.xlsx , *.xls)')
        # print(openfile_name[0])
        try:
            self.radioAll.setText(self._translate('','全选'))
            self.radioAll.setChecked(Qt.Unchecked)
            self.tableWidget.clear()
            self.filepath = pd.read_excel(openfile_name)
            # 获取有多少行(左到右)
            table_rows = self.filepath.shape[0]
            # 获取有多少列（上到下）+1多加个操作列
            table_colunms = self.filepath.shape[1] + 1
            # 获取头部
            # table_headers = filepath.columns.values.tolist()
            self.tableWidget.setColumnCount(table_colunms)
            self.tableWidget.setRowCount(table_rows)
            self.tableWidget.setHorizontalHeaderLabels(['微信名称', '备注', '操作'])
            # self.tableWidget.setHorizontalHeaderLabels(table_headers)
            for i in range(table_rows):
                self.tableWidget.setRowHeight(i,40)
                # 获取每一行数据
                table_rows_values = self.filepath.iloc[[i]]
                # 转成数组形式
                table_rows_values_array = np.array(table_rows_values)
                table_rows_values_list = table_rows_values_array.tolist()[0]
                # print(table_rows_values_list)
                for e, k in enumerate(table_rows_values_list):
                    name = QTableWidgetItem(str(k))
                    name.setTextAlignment(Qt.AlignCenter)
                    name.setFlags(Qt.ItemIsEnabled)
                    self.tableWidget.setItem(i, e, name)
                    # 添加个选中组件check 方法一
                    check = QTableWidgetItem()
                    check.setFlags(Qt.ItemIsEnabled)
                    check.setTextAlignment(Qt.AlignCenter)
                    check.setCheckState(Qt.Unchecked)  # 把checkBox设为未选中状态
                    self.tableWidget.setItem(i, table_colunms-1, check)  # 在(x,y)

                    # 添加个选中组件check 方法二（不好用）
                    # ck = QCheckBox(self.centralwidget)
                    # ck.stateChanged.connect(lambda: self.checkchange(ck))
                    # h = QHBoxLayout()
                    # h.setAlignment(Qt.AlignCenter)
                    # h.addWidget(ck)
                    # w = QWidget()
                    # w.setLayout(h)
                    #self.tableWidget.setCellWidget(i, 2, w)
            self.signal_write_msg.emit('上传完成')
            color = dialog.pen.color().name()
            self.signal_write_msg.emit('上传%s数据'%table_rows)
        except Exception as e:
            print(e)
            QMessageBox.about(self,'打开失败','打开文件失败,请检查文件')

    def Intotif(self):
        filepath = QFileDialog.getOpenFileName(self, '选择图片', '', 'Excel files(*.png , *.jpg)')
        try:
            self.tiffs(filepath)
        except Exception as e:
            pass

    def checkchange(self, e):
        try:
            # 获取行
            row = e.row()
            # 获取列
            colum = e.column()
            if colum == 2:
                checkState = self.tableWidget.item(row, colum).checkState()
                if checkState:
                    self.tableWidget.item(row, colum).setCheckState(Qt.Unchecked)
                else:
                    self.tableWidget.item(row, colum).setCheckState(Qt.Checked)
        except Exception as es:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_mian = Create_mian()

    #弹框
    dialog = dialogMenu.Dialog_Menu()

    #user_tool
    user_tool = commonly_used_tools.Com_use_tool()

    app_mian.show()
    sys.exit(app.exec_())
