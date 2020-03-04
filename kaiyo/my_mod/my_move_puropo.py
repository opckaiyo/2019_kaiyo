#coding: utf-8

# /*
#  * CH1 →　右の左右
#  * CH2 →　左の上下
#  * CH3 →　右の上下
#  * CH4 →　左の左右
#  */

import numpy as np
import time
import sys
import os
import math
from datetime import datetime
sys.path.append("/kaiyo/my_mod")
from my_get_serial import get_data, send_data
from my_motor_old import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each
from multiprocessing import Manager, Process
from my_balance import go_yaw, roteto, go_depth

def move_puropo(data,yaw_MV,set_val):

    set_write = 0
    dive = 0
    val = 30
    set_log = 0
    ch = 0
    start_time = time.time()
    line_num = 0
    path = 'txtlogデータ'
    inch = ""
    di = ""

    if(set_val == 0):
        try:
            os.makedirs('/kaiyo/log/puropo_log/'+str(datetime.now().strftime('%Y%m%d')))#ファイル生成
        except FileExistsError:
            pass
        input_log_file_make = open('/kaiyo/log/puropo_log/'+str(datetime.now().strftime('%Y%m%d'))+'/puropo_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt', 'a')#openファイル

    elif(set_val == 1):
        try:
            with open(path) as file:
                input_log_file_read = [s.strip() for s in f.readlines()]
                fr_len = len(input_log_file_read)
                set_write = 0

        except FileExistsError:
            print("file_error")
            pass

    while True:
        try:
            if(set_val == 0):
                CH1 = data["puropo_ch1"] - 50
                CH2 = data["puropo_ch2"] - 50
                CH3 = data["puropo_ch3"] - 50
                CH4 = data["puropo_ch4"] - 50

            if(set_val == 1):
                now_line = ast.literal_eval(input_log_file_read[line_num])
                if line_num + 1 < fr_len:
                    next_line = ast.literal_eval(input_log_file_read[line_num + 1])

                if(line_num == 0):
                    ch = str(now_line['inputCH'])
                    line_num = line_num + 1

                else:
                    time.sleep(next_line['time'] - now_line['time'])
                    inch = str(now_line['inputCH'])
                    di = str(now_line['diving'])
                    line_num = line_num + 1



            if(CH3 <= -25):#未接続
                ch = "0"
                print("puropo is got")
                stop()
            else:
                # if(CH2 >= 25):
                #     set_log = 1
                #     ch = "2"
                #     go_back(val)

                if(CH2 >= 25 or inch == "2"):
                    set_log = 1
                    ch = "2"
                    if ( yaw_MV.value >= 0 ):
                        go_back_each(
                        val + yaw_MV.value,
                        val - yaw_MV.value)
                    elif ( yaw_MV.value <= 0 ):
                        go_back_each(
                        val + yaw_MV.value,
                        val - yaw_MV.value)

                elif(CH2 <= -25 or inch == "-2"):
                    set_log = 1
                    ch = "-2"
                    go_back(-val)

                elif(CH4 <= -25 or inch == "4"):
                    set_log = 1
                    ch = "4"
                    spinturn(val)

                elif(CH4 >= 25 or inch == "-4"):
                    set_log = 1
                    ch = "-4"
                    spinturn(-val)

                else:
                    set_log = 0
                    stop_go_back()

                if(CH3 >= 25 or di == 1):
                    set_log = 1
                    dive = 1
                    up_down(val)

                else:
                    dive = 0
                    stop_up_down()

            if (set_log == 1 and set_val == 0):
                # print("write")
                # time_now = str(math.floor(time.time()))
                # time_now = time_now[-1]
                end_time = time.time()
                input_log_file_make.write("{'time':" + str(round(end_time - start_time,2)) + ", 'inputCH':'" + str(ch) + "', 'diving':" + str(dive) + ", 'moterval':" + str(val) + "}\n")

            # print("CH1",CH1)
            # print("CH2",CH2)
            # print("CH3",CH3)
            # print("CH4",CH4)
            time.sleep(0.2)



        except KeyboardInterrupt as e:
            print("puropo:era-")
            stop()
            break

if __name__ == '__main__':
    pass
