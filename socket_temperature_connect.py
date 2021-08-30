import socket
import time
import shelve

preset_command = {
    1: ['MB0023,1', 'MI0695,'],
    2: ['MB0024,1', 'MI0696,'],
    3: ['MB0076,1', 'MI0697,'],
    4: ['MB0026,1', 'MI0698,'],
}
force_command = 'MB0336,1'
start_command = 'MB0020,0'
stop_command = 'MB0020,1'


class Temperature:
    def __init__(self):
        # 是否打印log信息
        self.is_info = False
        # 打印log信息
        self.info = ''
        # temp测试任务
        self.task = []

        # 打开配置文件
        self.init_temp = shelve.open('init/init_temp')

        self.ip = self.init_temp['temp_ip']
        self.channel1_temp = self.init_temp['temp_channel1_temp']
        self.channel2_temp = self.init_temp['temp_channel2_temp']
        self.channel3_temp = self.init_temp['temp_channel3_temp']
        self.channel4_temp = self.init_temp['temp_channel4_temp']
        self.is_channel1_temp = self.init_temp['temp_is_channel1_temp']
        self.is_channel2_temp = self.init_temp['temp_is_channel2_temp']
        self.is_channel3_temp = self.init_temp['temp_is_channel3_temp']
        self.is_channel4_temp = self.init_temp['temp_is_channel4_temp']

        # 关闭配置文件
        self.init_temp.close()

        self.channel1 = (self.channel1_temp, 1)
        self.channel2 = (self.channel2_temp, 2)
        self.channel3 = (self.channel3_temp, 3)
        self.channel4 = (self.channel4_temp, 4)

        # 创造套接字
        self.server = socket.socket()
        # self.ip = '192.168.0.14'
        self.port = 5000
        try:
            self.server.connect((self.ip, self.port))
            # print('[INFO-TEMP]connect successfully')
            self.send_info('[INFO-TEMP]connect successfully')
            time.sleep(1)
        except:
            # print('[FAIL-TEMP]connect fail')
            self.send_info('[FAIL-TEMP]connect fail')

    # 向设备发送数据
    def send(self, data):
        try:
            self.server.send(bytes(data, encoding='ASCII'))
        except ConnectionError:
            # print('[FAIL-TEMP]send data fail')
            self.send_info('[FAIL-TEMP]send data fail')

    # 向设备接受数据
    def recv(self):
        try:
            text = str(self.server.recv(1024), encoding='UTF-8')
            # print(text)
        except ConnectionError:
            # print('[FAIL-TEMP]receive error')
            self.send_info('[FAIL-TEMP]receive error')
            text = ',9990'
        return text

    # 指令 (发送指令)
    def command(self, command):
        self.send('m')
        time.sleep(1)
        self.send(command)
        time.sleep(1)

    # 写入指令 (无返回值)
    def write_command(self, command):
        self.command(command)
        self.ack()

    # 询问指令 (有返回值)
    def query_command(self, command):
        self.command(command)
        return self.recv()

    # 设备应答
    def ack(self):
        while True:
            if self.recv() == 'OK':
                break

    # 温度预设 (四个通道)
    def preset(self, channel):
        temp = int(channel[0])
        temp_command = ''
        if temp == 0:
            temp_command = '0000'
        elif (temp > 0) and (temp < 10):
            temp_command = '00' + str(temp) + '0'
        elif (temp > 9) and (temp < 100):
            temp_command = '0' + str(temp) + '0'
        elif temp > 99:
            temp_command = str(temp) + '0'
        elif (temp < 0) and (temp > -10):
            temp_command = '0' + str(temp) + '0'
        elif temp < -9:
            temp_command = '' + str(temp) + '0'
        elif temp >= 175:
            temp_command = '1750'
        elif temp <= -75:
            temp_command = '-750'
        channel_command = preset_command[channel[1]][1]
        command = channel_command + temp_command
        self.write_command(command)
        # print('[INFO-TEMP]channel%s, %s℃ set successfully!' % (channel[1], channel[0]))
        self.send_info('[INFO-TEMP]channel' + str(channel[1]) + ', ' + str(channel[0]) +'℃ set successfully!')

    # 选择温度预设为当前值
    def change_channel(self, channel):
        state_command = preset_command[channel[1]][0]
        self.write_command(state_command)
        # print('[INFO-TEMP]change channel:', channel[1])
        self.send_info('[INFO-TEMP]change channel ' + str(channel[1]) + " " + str(channel[0]) + '℃')

    # 将测试项添加到任务列表中
    def task_generate(self):
        if self.is_channel1_temp:
            self.preset((self.channel1_temp, 1))
            self.task.append(self.channel1)
        if self.is_channel2_temp:
            self.preset((self.channel2_temp, 2))
            self.task.append(self.channel2)
        if self.is_channel3_temp:
            self.preset((self.channel3_temp, 3))
            self.task.append(self.channel3)
        if self.is_channel4_temp:
            self.preset((self.channel4_temp, 4))
            self.task.append(self.channel4)

        self.write_command(force_command)
        # print('[INFO-TEMP]force on')
        self.send_info('[INFO-TEMP]force on')

    # 检查设备温度 (1秒询问一次)
    def check_temp(self, channel):
        while True:
            for i in range(3):
                text = self.query_command('MI0006?')  # 获取格式为 MI6,250
                temp1 = int(text.split(',')[1])  # 250 整数位+小数位
                # print('[INFO-TEMP]temp: ', temp1 / 10.0, '℃')
                self.send_info('[INFO-TEMP]temp: ' + str(temp1 / 10.0) + '℃')

                temp = int(channel[0])
                if (temp1 == temp * 10) and (i == 2):
                    return
                elif temp1 == temp * 10:
                    pass
                else:
                    break

    # 启动设备
    def start(self):
        self.write_command(start_command)
        # print('[INFO-TEMP]running!')
        self.send_info('[INFO-TEMP]running!')

    # 关闭设备
    def stop(self):
        self.write_command(stop_command)
        # print('[INFO-TEMP]close!')
        self.send_info('[INFO-TEMP]close!')

    # 用于切换不同task
    def run(self, task):
        self.change_channel(task)
        self.check_temp(task)
        time.sleep(1)

    # 向主线程发送数据
    def send_info(self, info):
        self.info = info
        self.is_info = True


if __name__ == '__main__':
    temperature = Temperature()



