# from __future__ import print_function
import shelve
import hid
import time


class Power:
    def __init__(self):
        self.is_info = False
        self.info = ''
        self.task = []

        # 打开配置文件
        self.init_power = shelve.open('init/init_power')

        self.vid = self.init_power['power_vid']
        self.pid = self.init_power['power_pid']
        self.high_voltage = self.init_power['power_high_voltage']
        self.mid_voltage = self.init_power['power_mid_voltage']
        self.low_voltage = self.init_power['power_low_voltage']

        # 关闭配置文件
        self.init_power.close()

        # 连接设备
        try:
            self.h = hid.device()
            self.h.open(int(self.vid, 16), int(self.pid, 16))
            self.send_info('[INFO-POWER]connect success')
            time.sleep(1)
        except:
            self.send_info('[FAIL-POWER]connect fail')

    # 处理电压值
    def data_process(self, data):
        argv_low_bit = int(data / 2.56)
        argv_high_bit = int(data * 100 % 256)
        return [argv_high_bit, argv_low_bit, data]

    # 将测试任务添加到任务列表中
    def task_generate(self):
        h, l, data = self.data_process(float(self.high_voltage))
        command = ([[0, 170, 0, h, l] + [0] * 60, 'high_voltage ' + str(data)])
        self.task.append(command)
        self.send_info('[INFO-POWER]high voltage ' + str(data) + 'V append task success')
        time.sleep(1)
        h, l, data = self.data_process(float(self.mid_voltage))
        command = ([[0, 170, 0, h, l] + [0] * 60, 'mid_voltage ' + str(data)])
        self.task.append(command)
        self.send_info('[INFO-POWER]mid voltage ' + str(data) + 'V append task success')
        time.sleep(1)
        h, l, data = self.data_process(float(self.low_voltage))
        command = ([[0, 170, 0, h, l] + [0] * 60, 'low_voltage ' + str(data)])
        self.task.append(command)
        self.send_info('[INFO-POWER]low voltage ' + str(data) + 'V append task success')
        time.sleep(1)

    # 用于切换不同task
    def run(self, task):
        self.h.write(task[0])
        self.send_info('[INFO-POWER]' + str(task[1]) + 'V set success')
        time.sleep(1)

    # 向主线程发送数据
    def send_info(self, info):
        self.info = info
        self.is_info = True


if __name__ == '__main__':
    power = Power()
    t1 = [[0, 170, 0, 0, 1] + [0] * 60, 'debug test']
    power.run(t1)

# try:
#     print("Opening the device")
#
#     h = hid.device()
#     h.open(0x0483, 0x5750)  # TREZOR VendorID/ProductID
#     # h.open(0x413C, 0x301A)  # TREZOR VendorID/ProductID
#
#     print("Manufacturer: %s" % h.get_manufacturer_string())
#     print("Product: %s" % h.get_product_string())
#     print("Serial No: %s" % h.get_serial_number_string())
#
#     # enable non-blocking mode
#     h.set_nonblocking(1)
#
#     # write some data to the device
#     print("Write the data")
#     # h.write([0, 63, 35, 35] + [0] * 61)
#     h.write([0, 170, 0, 255, 0] + [0] * 60)
#
#     # wait
#     time.sleep(0.05)
#
#     # read back the answer
#     # print("Read the data")
#     # while True:
#     #     try:
#     #         d = h.read(64)
#     #         print(d)
#     #     except:
#     #         print('e')
#     while True:
#         d = h.read(65)
#         if d:
#             print(d)
#         else:
#             break
#
#     print("Closing the device")
#     h.close()
#
# except IOError as ex:
#     print(ex)
#     print("You probably don't have the hard-coded device.")
#     print("Update the h.open() line in this script with the one")
#     print("from the enumeration list output above and try again.")
#
# print("Done")