#coding: utf-8
# 時間制御を行うライブラリ
import time
# 自作関数をインポートするためのライブラリ
import sys
# 並列処理に必要な関数
from multiprocessing import Manager,  Process
# シリアル通信に必要な関数
import serial
# データ整形に必要
import ast

import termios

import os




# 自作関数のインポート
sys.path.append("/kaiyo/my_mod")
# ArduinoMegaとシリアル通信してセンサデータをもらう関数
from my_get_serial import get_data,  send_data
# PCA9685と通信しモータを制御する関数
from my_motor import go_back,  up_down,  spinturn,  roll,  stop,  stop_go_back,  stop_up_down,  go_back_each,  up_down_each,  spinturn_each
# 主にロボットの姿勢制御（方向、深度）を行う関数
from my_balance import go_yaw,  roteto,  go_depth
# プロポ（t19j）を使って、ロボットを制御するための関数
from my_rc import t10j,  t10j_time,  t10j_mode_sumo
# プログラムスタート時にロボットの状態や初期設定の動作を行う関数
from my_check import operation_check,  battery_check,  my_exit,  first_action
# 7色LEDの制御を行う関数
from my_gpio import led_red,  led_green,  led_yellow,  led_off,  led_blue,  led_purple,  led_lihtblue
# 大会コースに沿った動作を行う関数。（主にこの関数の値を調整して大会挑んだ）
# from my_course import course_convention,  course_pool
# プログラムがエラーを発生したときにエラーの内容をテキストファイルに記録する関数
from my_text_write import error_log_write
# GPSデータの取得や、GPSデータをテキストファイルに保存する関数
from my_gps import gps_sensor_join_data
# GPSによるウェイポイント制御を行う関数
# from my_waypoint import waypoint,  pad_rc_route_data_creation
# 水中ロボット班から借りたゲームパッドでラジコン制御するとに使う関数
from my_gamepad import pad_rc
# from my_move_puropo import move_puropo
from my_move_test import move_test
# from my_camera2 import camera
from my_camera4 import cap_main
from my_data_sampling import data_sampling
from threading import Thread
# import readchar
try:
    # windows用なければ、似たようなの作る
    from msvcrt import getch
except ImportError:
    def getch():
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd,  termios.TCSADRAIN,  old)


# ArduinoMEGAとpinで接続---------
# ArduinoMEGAとpinで接続
# ser = serial.Serial('/dev/ttyS0',  115200, timeout=3)
# ArduinoMEGAとUSBケーブル接続
ser = serial.Serial('/dev/ttyACM0',  115200, timeout=3)
# ArduinoMEGAとpinで接続---------

puropo_log_make = 0 #1:ログ読み込み　0:ログ書き込み

# この関数にメインのプログラムを記述する------------------------------------------

# サーミスタの値は温度ではなく抵抗値です。
# 目安として「4.5」ぐらいが50度なので注意が必要でしょう。

# この関数にメインのプログラムを記述する



def input_key(m_val,old_rot):
    try:
        # 直前の入力ログを消去
        os.remove('/kaiyo/log/input_log/just_before_read_input_log.txt')
    except FileNotFoundError:
        pass

    CTRL_C = 3
    while True:
        key = ord(getch())
        # 終了
        if key == CTRL_C:
            stop()
            old_rot = move_test(data, 'p', 0, goal_yaw, yaw_MV, goal_depth, depth_MV, set_yaw, set_depth,
             old_rot, True)
            print("main終了 Crtl+C押して")
            break
        else:
            kb = format(chr(key))
            print("test_key",  kb)
            # ログ再現
            if kb == 'S':
                send_data("reset rot")
                time.sleep(1)
                print("どのログを再生する？　9:大会時　0:直前")
                key = ord(getch())
                kb = format(chr(key))
                print("test_key",  kb)
                old_rot = move_test(data, kb, m_val, goal_yaw, yaw_MV, goal_depth, depth_MV, set_yaw, set_depth,
                 old_rot, False)

            # モータ出力------------------------
            elif kb == 'k':   #モータ出力の低下
                if m_val > 0:
                    m_val = m_val - 5;
                    print(m_val)

            elif kb == 'l':   #モータ出力の上昇
                if m_val <= 60:
                    m_val = m_val + 5;
                    print(m_val)
            # モータ出力------------------------

            else:
                # print("1",old_rot)
                old_rot = move_test(data, kb, m_val, goal_yaw, yaw_MV, goal_depth, depth_MV, set_yaw, set_depth,
                 old_rot, True)
                # print("2",old_rot)
        kb = None
        time.sleep(0.2)


def my_main(spin_cnt):

    # go_back(15)
    # print (data, "\n")
    # print (data["compass"])

    # # go_depth確認用-------------------------------
    # print("time:", data["time"], "depth:", data["depth"])
    # print("depth_MV :",  depth_MV.value,  "\n")
    # up_down(depth_MV.value)
    #
    #
    # # go_depth確認用-------------------------------
    # #
    # # go_back(60)
    # # up_down(13)
    # if set_depth.value == True:
    #     up_down(depth_MV.value)
    # #
    # # print(data["time"], data["depth"])
    # # # go_yaw確認用-------------------------------

    # # print(data["time"], data["yaw"])
    # # print("yaw_MV :",  yaw_MV.value,  "\n")
    # # spinturn(yaw_MV.value)

    # if set_yaw.value == True:
    #     if ( yaw_MV.value >= 0 ):
    #         go_back_each(
    #         m_val + yaw_MV.value,
    #         m_val - yaw_MV.value,
    #         m_val + yaw_MV.value,
    #         m_val - yaw_MV.value)
    #     elif ( yaw_MV.value < 0 ):
    #         go_back_each(
    #         m_val + yaw_MV.value,
    #         m_val - yaw_MV.value,
    #         m_val + yaw_MV.value,
    #         m_val - yaw_MV.value)
    # # go_yaw確認用-------------------------------
    #
    # ave_rot = ((data["rot0"] + data["rot1"]) / 2) - spin_cnt
    # print("\nrot", ave_rot)
    # print(ave_rot % 100.0)
    #
    # if (ave_rot % 100.0 <= 5.0 and data["time"] >= 10):
    #     ave_rot_now = ave_rot
    #     # print("test")
    #     goal_yaw.value = goal_yaw.value + 180
    #     if(goal_yaw.value >= 360):
    #         goal_yaw = 0
    #
    #     print("goal_yaw", goal_yaw.value)
    #     print("spin")
    #     yaw_MV.value = yaw_MV.value
    #     spinturn(yaw_MV.value)
    #     time.sleep(5)
    #     while True:
    #         yaw_MV.value = yaw_MV.value
    #         print("spin now")
    #         spinturn(yaw_MV.value)
    #         if (-3.0 <= yaw_MV.value <= 3.0):
    #             spin_cnt = ((data["rot0"] + data["rot1"]) / 2) - ave_rot_now
    #             print("spin_cnt:", spin_cnt)
    #             break
    #         time.sleep(0.2)


    time.sleep(0.2)
    pass

# この関数にメインのプログラムを記述する------------------------------------------


if __name__ == '__main__':
    try:
        print("wait:reboot now")
        # send_data("puropo_on")
        # send_data("puropo_off")
        while True:
            try:
                print("send:reboot")
                send_data("reboot")
                # time.sleep(1)
                val = ser.readline()
                # print(val)
                val = ast.literal_eval(val.decode('unicode-escape'))
                if val["time"] <= 10.0:
                    # time.sleep(1)
                    break

            except SyntaxError:
                print("main : Reception Error!!\n")
            except TimeoutError:
                print("main : timeout Error!\n")
            # except ValueError:
            #     print("serial : Value Error!\n")



        # 出力
        m_val = 30
        old_rot = [0] * 6
        spin_cnt = 0

        with Manager() as manager:
            print("OK")
            #センサーのdata
            data = manager.dict()
            #yawの操作量
            yaw_MV = manager.Value("d", 0.0)
            #depthの操作量
            depth_MV = manager.Value("d", 0.0)
            # goal_yawの目標値
            goal_yaw = manager.Value("i", 0)
            # goal_depthの目標値
            goal_depth = manager.Value('d', 1.00)
            # yawをメインで実行
            set_yaw = manager.Value('i', False)
            # depthをメインで実行
            set_depth = manager.Value('i', False)
            # 受信データの大きさ
            try:
                val = ser.readline()
                val = ast.literal_eval(val.decode('unicode-escape'))
            except SyntaxError:
                # 受信エラー
                print("main : Reception Error!!")

            # 受信データの大きさに合わせる
            for i in val:
                data[i] = val[i]

            # 各プロセスの定義
            get_data = Process(target=get_data, args=[data])
            # get_puropo = Process(target=move_puropo, args=[data, yaw_MV, puropo_log_make])
            go_yaw = Process(target=go_yaw,  args=[goal_yaw, data, yaw_MV])
            go_depth = Process(target=go_depth,  args=[goal_depth, data, depth_MV])
            sensor_log = Process(target=data_sampling,  args=[data, 0.2]) # 0.2はsample_rate
            # f_camera = Process(target=cap_main,  args=[])
            # キーボード入力、ソケット通信なしだと単体でしか動かない(mainから実行不可)
            # move_test = Process(target=move_test,  args=[data, True])
            Thread_key = Thread(target=input_key, args=[m_val,old_rot])




            get_data.start()
            # get_puropo.start()
            go_yaw.start()
            go_depth.start()
            sensor_log.start()
            # f_camera.start()
            Thread_key.start()


            # モードなどの設定 2019使ってない
            # first_action(data)

            # ave_rot = 0

            print("start")

            while True:
                # 予期せぬエラーが発生した時の処理
                try:
                    # Ctrl-cを押したときの処理
                    try:
                        # メインのプログラム
                        # ----------------------------------------
                        my_main(spin_cnt)
                        # my_exit()
                        # break
                        # ----------------------------------------
                    except KeyboardInterrupt as e:
                        # Ctrl-cを押したときの処理
                        print("\n-----------")
                        print("main.py : ", e)
                        print("-----------\n")
                        my_exit()
                except Exception as e:
                    # 予期せぬエラーが発生した時の処理
                    stop()
                    # エラーの内容を残す(日付ごと)
                    error_log_write(e)
                    print("\n-----------")
                    print("\nmain.py Error :", e)
                    print("Error!!!!!!!!!!!!!!!!!!!!!!!")
                    print("-----------\n")
                    for i in range(20):
                        led_green()
                        time.sleep(0.05)
                        led_off()
                        time.sleep(0.05)
                    # my_exit()

        # get_data.join()
        # get_puropo.join()
        # go_yaw.join()
        # go_depth.join()

    except KeyboardInterrupt as key:
        # プログラムを終了するときの処理
        print("\n-----------")
        print("main.py : ", key)
        print("-----------\n")
        my_exit()
