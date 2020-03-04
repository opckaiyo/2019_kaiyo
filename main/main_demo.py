# ポリテクビジョン用

# 時間制御を行うライブラリ
import time
# ソケット通信
import socket
# データのシリアル化に必要
import pickle
# 自作関数をインポートするためのライブラリ
import sys


# 自作関数のインポート
sys.path.append("/kaiyo/my_mod")

from my_socket_server import socket_server
from threading import Thread
# 並列処理に必要な関数
from multiprocessing import Manager,  Process
# PCA9685と通信しモータを制御する関数
from my_motor import go_back,  up_down,  spinturn,  roll,  stop,  stop_go_back,  stop_up_down,  go_back_each,  up_down_each,  spinturn_each
from my_camera2 import set_camera

def val_map(val):
    if val <= 0 and val >= -100:
        in_min = -100
        in_max = 0
        out_min = -30
        out_max = 0
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    elif val >= 0 and val <= 100:
        in_min = 0
        in_max = 100
        out_min = 0
        out_max = 30
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def val_map2(val):
    if val <= 0 and val >= -100:
        in_min = -100
        in_max = 0
        out_min = -35
        out_max = 0
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    elif val >= 0 and val <= 100:
        in_min = 0
        in_max = 100
        out_min = 0
        out_max = 35
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == '__main__':
    print("start")
    try:

        is_stop = 0
        go_val = 0
        up_val = 0

        with Manager() as manager:
            # ゲームパッド用
            pad_data = manager.dict()

            pad_data = {"joy_lx":0, "joy_ly":0, "joy_rx":0, "joy_ry":0,\
                        "hat_x":0, "hat_y":0, \
                        "btn_a":0, "btn_b":0, "btn_x":0, "btn_y":0, \
                        "btn_lb":0, "btn_rb":0, "btn_back":0, \
                        "btn_start":0, "btn_logicool":0, \
                        "btn_joyl":0, "btn_joyr":0}

            socket_server = Thread(target=socket_server, args=[pad_data,is_stop])
            camera = Thread(target=set_camera, args=[])

            data = socket_server.start()
            camera.start()

            while True:
                # print("main : " , pad_data)
                # print('joy_ly : {}, joy_lx: {}, joy_ry : {}'.format(pad_data["joy_ly"],pad_data["joy_lx"],pad_data["joy_ry"]))
                # val_map(joy_ly)
                # val_map(joy_lx)
                # val_map(joy_ry)

                if (pad_data["joy_ly"] == 0 and pad_data["joy_lx"] == 0):
                    stop()
                elif (pad_data["joy_ly"] != 0 and pad_data["joy_lx"] == 0):
                    go_back(val_map(pad_data["joy_ly"]))
                    # print("go", val_map(pad_data["joy_ly"]))
                elif (pad_data["joy_ly"] == 0 and pad_data["joy_lx"] != 0):
                    spinturn(val_map(pad_data["joy_lx"]))
                    # print("spin", val_map(pad_data["joy_lx"]))

                if (pad_data["joy_ry"] != 0):
                    up_down(val_map2(-pad_data["joy_ry"]))
                    # print("up", val_map(pad_data["joy_ry"]))
                # print()

                time.sleep(0.1)

    except KeyboardInterrupt as key:
        # プログラムを終了するときの処理
        print("\n-----------")
        print("main_demo.py : ", key)
        print("-----------\n")
        is_stop = 1
