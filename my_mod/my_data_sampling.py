# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# sudo pip install pyserial
# Arduinoとのシリアル通信はmy_get_serial.pyで行う
# import serial
import ast
import time
from datetime import datetime
from multiprocessing import Manager, Process
import sys
import os
sys.path.append("/kaiyo/my_mod")

# ArduinoMegaとシリアル通信してセンサデータをもらう関数
from my_get_serial import get_data, send_data

# from my_get_serial import get_data
# -----------------------------------------------------------------------------

# ArduinoMEGAとpinで接続
# ser = serial.Serial('/dev/ttyS0', 115200)
# ArduinoMEGAとUSBケーブル接続
# ser = serial.Serial('/dev/ttyACM0', 115200)

# -----------------------------------------------------------------------------

# file_name ='/kaiyo/log/sensor_log/'+str(datetime.now().strftime('%Y%m%d'))+'/sensor_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt'

# def meke_dirs():
#     try:
#         os.makedirs('/kaiyo/log/sensor_log/'+str(datetime.now().strftime('%Y%m%d')))
#     except FileExistsError:
#         pass
#     open(file_name, 'a')
#
# def data_write():
#     global file_name
#     data = get_data("all")
#     sensor_log_file_time = open(file_name, 'a')
#     data["datetime"] = str(datetime.now())
#     # print(data)
#
#     #ソートするがlist型になってしまう
#     sensor_log_file_time.writelines(str(sorted(data.items(), key = lambda x:x[0])) + "\n")
#     sensor_log_file_time.close()



def data_sampling(sensordata,set_sample_rate=0.2):
    # logsをテキストに残すか聞くプログラム
    try:
        os.makedirs('/kaiyo/log/sensor_log/'+str(datetime.now().strftime('%Y%m%d')))
    except FileExistsError:
        pass
    sensor_log_file_time = open('/kaiyo/log/sensor_log/'+str(datetime.now().strftime('%Y%m%d'))+'/sensor_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt', 'a')
    sensor_log_file = open('/kaiyo/log/sensor_log/sensor_log.txt', 'w')

    # print(type(sensordata))

    start_time = time.time()
    while True:

        # サンプリングレート以上時間が経過したら書き込み
        ela_time = time.time() - start_time
        if ela_time >= set_sample_rate:
            data = sensordata
            # print(str(sorted(data.items(), key = lambda x:x[0]))) # 書き込む内容の表示
            data["datetime"] = str(datetime.now())

            #ソートするがlist型になってしまう
            sensor_log_file_time.writelines(str(sorted(data.items(), key = lambda x:x[0])) + "\n")
            sensor_log_file.writelines(str(sorted(data.items(), key = lambda x:x[0])) + "\n")

            start_time = time.time()


# -----------------------------------------------------------------------------

if __name__ == '__main__':
    # send_data("reboot")
    while True:
        try:
            data_sampling(set_sample_rate=0.2)
            # pass
        except KeyboardInterrupt as e:
            quit()
            # pass
            # print "\nFile close!!\n"
            # sensor_log_file_time.close()
            # sensor_log_file.close()
