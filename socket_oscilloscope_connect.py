import pyvisa
import time
import shelve

load_command = ':Disk:Load '
save_report_command = ':Disk:Save:MReport '


class Oscilloscope:
    def __init__(self):
        self.is_info = False
        self.info = ''
        self.task = [1]

        # 打开配置文件
        self.init_scope = shelve.open('init/init_scope')

        self.ip = self.init_scope['scope_ip']
        self.setup = self.init_scope['scope_setup']

        # 关闭配置文件
        self.init_scope.close()

        # 连接示波器
        try:
            self.rm = pyvisa.ResourceManager()
            self.inst = self.rm.open_resource('TCPIP0::' + str(self.ip) + '::hislip0::INSTR')
            self.inst.timeout = 20000
            self.inst.clear()
            self.send_info('[INFO-SCOPE]connect success')
            time.sleep(1)
        except:
            self.send_info('[FAIL-SCOPE]connect fail')

    def load_setup(self):
        try:
            self.inst.write(load_command + '"' + str(self.setup) + '"')
            self.send_info('[INFO-SCOPE]load ' + '"' + str(self.setup) + '"' + 'success')
            time.sleep(1)
        except:
            self.send_info('[FAIL-SCOPE]load setup fail')

    def save_report(self, name):
        try:
            self.inst.write(save_report_command + '"' + str(name) + '"')
            self.send_info('[INFO-SCOPE]save report success')
            time.sleep(1)
        except:
            self.send_info('[FAIL-SCOPE]save report fail')

    # 用于切换不同task
    def run(self, name):
        self.load_setup()
        time.sleep(15)
        self.save_report(name)
        time.sleep(5)

    # 向主线程发送数据
    def send_info(self, info):
        self.info = info
        self.is_info = True

# rm = pyvisa.ResourceManager()
# inst = rm.open_resource('TCPIP0::192.168.0.11::hislip0::INSTR')
#
# inst.timeout = 20000
# inst.clear()

# print(inst.query('*IDN?'))
# print(inst.write(':Waveform:Source Channel1'))
# time.sleep(1)
# print(inst.write(':Waveform:View Main'))
# time.sleep(1)
# print(inst.query(':Waveform:Segmented:Points?'))
# print(inst.query(':Waveform:Data?'))
# data = inst.query(':Waveform:Data?')
# print(inst.query(':Waveform:Segmented:TTag?'))
# inst.write(':Waveform:Segmented:ALL OFF')
# print(inst.write(':Waveform:View MAIN'))

# inst.write(':Stop')


# inst.write(':Measure:Frequency Channel1')
# time.sleep(1)
# inst.write('Measure:TieClock2 Channel1,Second,Both,Auto')
# time.sleep(1)
# inst.write('Measure:CTCDutyCycle Channel1,Rising')
# time.sleep(1)
# inst.write(':AutoScale')
# time.sleep(10)
# hz = float(inst.query(':Measure:Frequency? Channel1'))
# time.sleep(1)
# hz2time = 1.0/hz*200
# print(inst.write(':TIMebase:RANGe ', str(hz2time)))
# time.sleep(1)
# inst.write(':Measure:Jitter:Trend ON')
# time.sleep(1)
# inst.write(':Measure:Jitter:Histogram ON')
# time.sleep(15)
# inst.write(':Disk:Save:MReport "test.pdf"')
# time.sleep(5)
# inst.write(':Disk:Save:MReport "test.mht"')
# time.sleep(5)

# inst.write(':LTest:Test ON')
# inst.write(':LTest:Measurement Meas3')
# print(float(inst.query(':Measure:Frequency? Channel1')))
# print(inst.query(':MEASure:HISTogram:MAX?'))
# print(inst.query(':MEASure:HISTogram:MIN?'))
# print(inst.query(':MEASure:Mark?'))
# inst.write(':Disk:Load "ppl1.set"')








