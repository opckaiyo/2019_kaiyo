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
sys.path.append("/kaiyo/my_mod")
from my_get_serial import get_data, send_data
from my_motor_old import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each
from multiprocessing import Manager, Process


def puropo(data):
    while True:
        CH1 = data["propo_ch1"] - 50
        CH2 = data["propo_ch2"] - 50
        CH3 = data["propo_ch3"] - 50
        CH4 = data["propo_ch4"] - 50

        if(CH2 >= 25):#前
            go_back(30)
            if(CH3 <= -25):
                up_down(30)
            if(CH4 <= -25):
                spinturn(30)
            if(CH4 >= 25):
                spinturn(-30)

        elif(CH2 <= -25):#後
            go_back(-30)
            if(CH3 <= -25):
                up_down(30)
            if(CH4 <= -25):
                spinturn(30)
            if(CH4 >= 25):
                spinturn(-30)


        elif(CH4 <= -25):#左
            spinturn(30)

        elif(CH4 >= 25):#右
            spinturn(-30)

        elif(CH3 <= -25):
            up_down(40)
            if(CH2 >= 25):
                go_back(30)
        else:
            stop()

        # print("CH1",CH1)
        # print("CH2",CH2)
        # print("CH3",CH3)
        # print("CH4",CH4)

        time.sleep(0.2)










if __name__ == '__main__':
    pass
