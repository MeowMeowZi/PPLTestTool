import shelve
import time
import serial.tools


class Debug:
    def __init__(self):
        self.is_info = False
        self.info = ''
        self.task = []

        # 打开配置文件
        self.init_debug =  shelve.open('init/init_debug')

        self.port = self.init_debug['debug_port']
        self.cpll_test = self.init_debug['debug_cpll_test']

        # 关闭配置文件
        self.init_debug.close()

        try:
            self.baudrate = 115200
            self.time_x = 1
            self.bytesize = 8
            self.parity = serial.PARITY_NONE
            self.stopbits = serial.STOPBITS_ONE
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.time_x)
            self.send_info('[INFO-DEBUG]connect success')
        except:
            self.send_info('[FAIL-DEBUG]connect fail')

    def task_generate(self):
        for i in self.cpll_test.split(','):
            result = i.split(' ')
            hz = 'cpll_' + str(int(result[0]) * 25 / (1 + int(result[1]))) + 'M'
            self.task.append(['cpll' + i, hz])
            self.send_info('[INFO-DEBUG]' + hz + ' append task success')
            time.sleep(1)

    def run(self, task):
        self.ser.write(task[0].encode('UTF-8'))
        self.send_info('[INFO-DEBUG]' + task[1] + 'set success')
        time.sleep(1)

    def send_info(self, info):
        self.info = info
        self.is_info = True


if __name__ == '__main__':
    # debug = Debug()
    # t1 = ['40 0', 'power test']
    # debug.run(t1)
    port = 'COM4'
    baudrate = 115200
    time_x = 1
    bytesize = 8
    parity = serial.PARITY_NONE
    stopbits = serial.STOPBITS_ONE
    ser = serial.Serial(port=port, baudrate=baudrate, timeout=time_x)
    ser.write('cpll 40 0'.encode('UTF-8'))

