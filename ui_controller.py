import shelve
import re
import sys
import threading
import time

import socket_temperature_connect
import socket_oscilloscope_connect
# import usb_connect
import serial_connect
from main_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QTimer, QThread, pyqtSignal


class MainUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        self.setupUi(self)

        # 测试变量
        self.test_info = False
        self.test_text = ''

        # 日志名字
        self.log_name = ''

        # 打开配置文件
        self.init_scope = shelve.open('init/init_scope')
        self.init_temp = shelve.open('init/init_temp')
        self.init_power = shelve.open('init/init_power')
        self.init_debug = shelve.open('init/init_debug')

        # Oscilloscope标签页数据
        self.scope_ip = ''
        self.scope_setup = ''

        # Temperature标签页数据
        self.temp_ip = ''
        self.temp_channel1_temp = ''
        self.temp_channel2_temp = ''
        self.temp_channel3_temp = ''
        self.temp_channel4_temp = ''

        self.temp_is_channel1_temp = False
        self.temp_is_channel2_temp = False
        self.temp_is_channel3_temp = False
        self.temp_is_channel4_temp = False

        # Power标签页数据
        self.power_high_voltage = ''
        self.power_mid_voltage = ''
        self.power_low_voltage = ''
        self.power_vid = ''
        self.power_pid = ''

        # Debug标签页数据
        self.debug_port = ''
        self.debug_mode = []

        # 读取初始化文件并显示在软件上
        self.init_setting()

        self.pushbutton_signal_manage()
        self.lineedit_signal_manage()

    def pushbutton_signal_manage(self):
        self.pushButton_info_start.clicked.connect(
            lambda: self.pushbutton_slot_manage(self.pushButton_info_start)
        )

    def pushbutton_slot_manage(self, button):
        if button == self.pushButton_info_start:
            self.start()

    def lineedit_signal_manage(self):
        pass
        # self.lineEdit_scope_ip.textChanged.connect(
        #     lambda: self.lineedit_slot_manage(self.lineEdit_scope_ip)
        # )

    def lineedit_slot_manage(self, lineedit):
        pass
        # regex_ip = re.compile(r'^(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
        # if lineedit == self.lineEdit_scope_ip:
        #     if not regex_ip.search(self.lineEdit_scope_ip.text()):
        #         QMessageBox.critical(self, 'Wrong', 'IP address format error')
        #
        # if lineedit == self.lineEdit_temp_ip:
        #     if not regex_ip.search(self.lineEdit_temp_ip.text()):
        #         QMessageBox.critical(self, 'Wrong', 'IP address format error')

    # 关闭软件自动保存
    def closeEvent(self, QCloseEvent):
        self.data_save()
        print('save success!')

    # 开启软件时，将上一次关闭时保存的配置配置到软件上
    def init_setting(self):
        # Oscilloscope数据显示
        try:
            self.scope_ip = self.init_scope['scope_ip']
            self.lineEdit_scope_ip.setText(self.scope_ip)
        except KeyError:
            pass
        try:
            self.scope_setup = self.init_scope['scope_setup']
            self.lineEdit_scope_setup.setText(self.scope_setup)
        except KeyError:
            pass

        # Temperature数据显示
        try:
            self.temp_ip = self.init_temp['temp_ip']
            self.lineEdit_temp_ip.setText(self.temp_ip)
        except KeyError:
            pass
        try:
            self.temp_channel1_temp = self.init_temp['temp_channel1_temp']
            self.lineEdit_temp_channl1.setText(self.temp_channel1_temp)
        except KeyError:
            pass
        try:
            self.temp_channel2_temp = self.init_temp['temp_channel2_temp']
            self.lineEdit_temp_channl2.setText(self.temp_channel2_temp)
        except KeyError:
            pass
        try:
            self.temp_channel3_temp = self.init_temp['temp_channel3_temp']
            self.lineEdit_temp_channl3.setText(self.temp_channel3_temp)
        except KeyError:
            pass
        try:
            self.temp_channel4_temp = self.init_temp['temp_channel4_temp']
            self.lineEdit_temp_channl4.setText(self.temp_channel4_temp)
        except KeyError:
            pass
        try:
            self.temp_is_channel1_temp = self.init_temp['temp_is_channel1_temp']
            self.checkBox_temp_channel1.setCheckState(self.temp_is_channel1_temp)
        except KeyError:
            pass
        try:
            self.temp_is_channel2_temp = self.init_temp['temp_is_channel2_temp']
            self.checkBox_temp_channel2.setCheckState(self.temp_is_channel2_temp)
        except KeyError:
            pass
        try:
            self.temp_is_channel3_temp = self.init_temp['temp_is_channel3_temp']
            self.checkBox_temp_channel3.setCheckState(self.temp_is_channel3_temp)
        except KeyError:
            pass
        try:
            self.temp_is_channel4_temp = self.init_temp['temp_is_channel4_temp']
            self.checkBox_temp_channel4.setCheckState(self.temp_is_channel4_temp)
        except KeyError:
            pass

        # Power数据显示
        try:
            self.power_high_voltage = self.init_power['power_high_voltage']
            self.lineEdit_power_high_voltage.setText(self.power_high_voltage)
        except KeyError:
            pass
        try:
            self.power_mid_voltage = self.init_power['power_mid_voltage']
            self.lineEdit_power_mid_voltage.setText(self.power_mid_voltage)
        except KeyError:
            pass
        try:
            self.power_low_voltage = self.init_power['power_low_voltage']
            self.lineEdit_power_low_voltage.setText(self.power_low_voltage)
        except KeyError:
            pass
        try:
            self.power_vid = self.init_power['power_vid']
            self.lineEdit_power_vid.setText(self.power_vid)
        except KeyError:
            pass
        try:
            self.power_pid = self.init_power['power_pid']
            self.lineEdit_power_pid.setText(self.power_pid)
        except KeyError:
            pass

        # Debug数据显示
        try:
            self.debug_port = self.init_debug['debug_port']
            self.lineEdit_debug_port.setText(self.debug_port)
        except KeyError:
            pass
        try:
            self.debug_mode = self.init_debug['debug_mode']
            for i in range(len(self.debug_mode)):
                for j in range(len(self.debug_mode[0])):
                    self.tableWidget_debug_mode.setItem(i, j, QTableWidgetItem(self.debug_mode[i][j]))
        except KeyError:
            pass

    # 界面数据保存到变量中，再保存到配置文件中
    def data_save(self):
        # 打开配置文件
        self.init_scope = shelve.open('init/init_scope')
        self.init_temp = shelve.open('init/init_temp')
        self.init_power = shelve.open('init/init_power')
        self.init_debug = shelve.open('init/init_debug')

        # Oscilloscope标签页数据保存
        self.scope_ip = self.lineEdit_scope_ip.text()
        self.scope_setup = self.lineEdit_scope_setup.text()

        self.init_scope['scope_ip'] = self.scope_ip
        self.init_scope['scope_setup'] = self.scope_setup

        # Temperature标签页数据保存
        self.temp_ip = self.lineEdit_temp_ip.text()
        self.temp_channel1_temp = self.lineEdit_temp_channl1.text()
        self.temp_channel2_temp = self.lineEdit_temp_channl2.text()
        self.temp_channel3_temp = self.lineEdit_temp_channl3.text()
        self.temp_channel4_temp = self.lineEdit_temp_channl4.text()

        self.temp_is_channel1_temp = self.checkBox_temp_channel1.checkState()
        self.temp_is_channel2_temp = self.checkBox_temp_channel2.checkState()
        self.temp_is_channel3_temp = self.checkBox_temp_channel3.checkState()
        self.temp_is_channel4_temp = self.checkBox_temp_channel4.checkState()

        self.init_temp['temp_ip'] = self.temp_ip
        self.init_temp['temp_channel1_temp'] = self.temp_channel1_temp
        self.init_temp['temp_channel2_temp'] = self.temp_channel2_temp
        self.init_temp['temp_channel3_temp'] = self.temp_channel3_temp
        self.init_temp['temp_channel4_temp'] = self.temp_channel4_temp

        self.init_temp['temp_is_channel1_temp'] = self.temp_is_channel1_temp
        self.init_temp['temp_is_channel2_temp'] = self.temp_is_channel2_temp
        self.init_temp['temp_is_channel3_temp'] = self.temp_is_channel3_temp
        self.init_temp['temp_is_channel4_temp'] = self.temp_is_channel4_temp

        # Power标签页数据保存
        self.power_high_voltage = self.lineEdit_power_high_voltage.text()
        self.power_mid_voltage = self.lineEdit_power_mid_voltage.text()
        self.power_low_voltage = self.lineEdit_power_low_voltage.text()
        self.power_vid = self.lineEdit_power_vid.text()
        self.power_pid = self.lineEdit_power_pid.text()

        self.init_power['power_high_voltage'] = self.power_high_voltage
        self.init_power['power_mid_voltage'] = self.power_mid_voltage
        self.init_power['power_low_voltage'] = self.power_low_voltage
        self.init_power['power_vid'] = self.power_vid
        self.init_power['power_pid'] = self.power_pid

        # Debug标签页数据保存
        self.debug_port = self.lineEdit_debug_port.text()
        debug_mode = []
        try:
            for i in range(self.tableWidget_debug_mode.rowCount()):
                list_ = []
                for j in range(self.tableWidget_debug_mode.columnCount()):
                    text = self.tableWidget_debug_mode.item(i, j).text()
                    if text == '':
                        break
                    list_.append(text)
                if list_ == []:
                    break
                debug_mode.append(list_)
        except:
            pass

        self.init_debug['debug_port'] = self.debug_port
        self.debug_mode = debug_mode
        self.init_debug['debug_mode'] = debug_mode

        # 关闭配置文件
        self.init_scope.close()
        self.init_temp.close()
        self.init_power.close()
        self.init_debug.close()

    def start(self):
        self.log_name = 'log/' + time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()) + '_' + 'log.txt'
        self.data_save()
        threading.Thread(target=self.run).start()

    def run(self):
        self.temp = socket_temperature_connect.Temperature()
        threading.Thread(target=self.temp_info).start()
        self.scope = socket_oscilloscope_connect.Oscilloscope()
        threading.Thread(target=self.scope_info).start()
        self.power = usb_connect.Power()
        threading.Thread(target=self.power_info).start()
        self.debug = serial_connect.Debug()
        threading.Thread(target=self.debug_info).start()

        self.temp.task_generate()
        self.power.task_generate()
        self.debug.task_generate()

        self.temp.start()

        for i in self.temp.task:
            self.temp.run(i)
            for j in self.power.task:
                self.power.run(j)
                for k in self.debug.task:
                    self.debug.run(k)

                    name = 'temp_'+str(i[0])+'-'+'power_'+str(j[1])+'-'+'debug_'+str(k[1])
                    self.scope.run(name)

        self.temp.stop()

    # 将信息打印到窗口
    def temp_info(self):
        while True:
            if self.temp.is_info:
                text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' -> ' + self.temp.info
                f = open(self.log_name, 'a')
                f.write(text + '\n')
                f.close()
                self.textBrowser_info_text.append(text)
                self.textBrowser_info_text.moveCursor(self.textBrowser_info_text.textCursor().End)
                self.temp.is_info = False

    def scope_info(self):
        while True:
            if self.scope.is_info:
                text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' -> ' + self.scope.info
                f = open(self.log_name, 'a')
                f.write(text + '\n')
                f.close()
                self.textBrowser_info_text.append(text)
                self.textBrowser_info_text.moveCursor(self.textBrowser_info_text.textCursor().End)
                self.scope.is_info = False

    def power_info(self):
        while True:
            if self.power.is_info:
                text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' -> ' + self.power.info
                f = open(self.log_name, 'a')
                f.write(text + '\n')
                f.close()
                self.textBrowser_info_text.append(text)
                self.textBrowser_info_text.moveCursor(self.textBrowser_info_text.textCursor().End)
                self.power.is_info = False

    def debug_info(self):
        while True:
            if self.debug.is_info:
                text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' -> ' + self.debug.info
                f = open(self.log_name, 'a')
                f.write(text + '\n')
                f.close()
                self.textBrowser_info_text.append(text)
                self.textBrowser_info_text.moveCursor(self.textBrowser_info_text.textCursor().End)
                self.debug.is_info = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainUI = MainUI()
    MainUI.show()
    sys.exit(app.exec_())
