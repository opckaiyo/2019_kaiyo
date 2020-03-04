#coding: utf-8
# 時間制御を行うライブラリ
import time
# 自作関数をインポートするためのライブラリ
import sys
# 並列処理に必要な関数
from multiprocessing import Manager, Process
# シリアル通信に必要な関数
import serial
# データ整形に必要
import ast


# 自作関数のインポート
sys.path.append("/kaiyo/my_mod")
# ArduinoMegaとシリアル通信してセンサデータをもらう関数
from my_get_serial import get_data, send_data
# PCA9685と通信しモータを制御する関数
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each
# 主にロボットの姿勢制御（方向、深度）を行う関数
from my_balance import go_yaw, roteto, go_depth
# プロポ（t19j）を使って、ロボットを制御するための関数
from my_rc import t10j, t10j_time, t10j_mode_sumo
# プログラムスタート時にロボットの状態や初期設定の動作を行う関数
from my_check import operation_check, battery_check, my_exit, first_action
# 7色LEDの制御を行う関数
from my_gpio import led_red, led_green, led_yellow, led_off, led_blue, led_purple, led_lihtblue
# 大会コースに沿った動作を行う関数。（主にこの関数の値を調整して大会挑んだ）
# from my_course import course_convention, course_pool
# プログラムがエラーを発生したときにエラーの内容をテキストファイルに記録する関数
from my_text_write import error_log_write
# GPSデータの取得や、GPSデータをテキストファイルに保存する関数
from my_gps import gps_sensor_join_data
# GPSによるウェイポイント制御を行う関数
# from my_waypoint import waypoint, pad_rc_route_data_creation
# 水中ロボット班から借りたゲームパッドでラジコン制御するとに使う関数
from my_gamepad import pad_rc
from my_move_puropo import move_puropo
from my_move_test import move_test
from my_data_sampling import data_sampling
import readchar

# ArduinoMEGAとpinで接続---------
# ArduinoMEGAとpinで接続
ser = serial.Serial('/dev/ttyS0', 115200,timeout=3)
# ArduinoMEGAとUSBケーブル接続
# ser = serial.Serial('/dev/ttyACM0', 115200)
# ArduinoMEGAとpinで接続---------


# この関数にメインのプログラムを記述する------------------------------------------

# この関数にメインのプログラムを記述する
def my_main():

    # go_back(15)
    # print (data,"\n")

    # go_depth確認用-------------------------------
    # print("time:",data["time"],"depth:",data["depth"])
    # print("depth_MV :", depth_MV.value, "\n")
    # up_down(depth_MV.value)

    # go_depth確認用-------------------------------


    # print(data["time"],data["depth"])
    # go_yaw確認用-------------------------------
    print(data["time"],data["yaw"])
    print("yaw_MV :", yaw_MV.value, "\n")
    # if ( yaw_MV.value >= 0 ):
    #     go_back_each(
    #     30 + yaw_MV.value,
    #     30 - yaw_MV.value,
    #     30 + yaw_MV.value,
    #     30 - yaw_MV.value)
    # elif ( yaw_MV.value <= 0 ):
    #     go_back_each(
    #     30 + yaw_MV.value,
    #     30 - yaw_MV.value,
    #     30 + yaw_MV.value,
    #     30 - yaw_MV.value)

    # go_yaw確認用-------------------------------


    time.sleep(0.2)
    pass

# この関数にメインのプログラムを記述する------------------------------------------


if __name__ == '__main__':
    try:
        # print("wait:3s")
        # send_data("reboot")
        # time.sleep(1)
        # send_data("puropo_on")
        # send_data("puropo_off")
        # time.sleep(1)
        # send_data("puropo_off")
        # time.sleep(1)
        send_data("reboot")
        time.sleep(1)

        with Manager() as manager:
            print("start")
            #センサーのdata
            data = manager.dict()
            #yawの操作量
            yaw_MV = manager.Value("d", 0.0)
            #depthの操作量
            depth_MV = manager.Value("d", 0.0)
            # goal_yawの目標値
            goal_yaw = manager.Value("i", 0)
            # goal_depthの目標値
            goal_depth = manager.Value('d', 1.0)
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

            get_data = Process(target=get_data, args=[data])
            get_puropo = Process(target=move_puropo, args=[data,yaw_MV,0])
            go_yaw = Process(target=go_yaw, args=[goal_yaw,data,yaw_MV])
            go_depth = Process(target=go_depth, args=[goal_depth,data,depth_MV])
            # キーボード入力、ソケット通信なしだと単体でしか動かない(mainから実行不可)
            move_test = Process(target=move_test, args=[data])


            set_sample_rate = 0.2
            sensor_process = Process(target=data_sampling, args=[data,set_sample_rate])
            # sensor_process.start()

            get_data.start()
            get_puropo.start()
            go_yaw.start()
            # go_depth.start()

            # move_test.start()

            # print("start--")
            # print(val)

            # モードなどの設定
            # first_action(data)


            while True:
                # 予期せぬエラーが発生した時の処理
                try:
                    # Ctrl-cを押したときの処理
                    try:
                        # メインのプログラム
                        # ----------------------------------------
                        my_main()
                        # my_exit()
                        # break
                        # ----------------------------------------
                    except KeyboardInterrupt as e:
                        # Ctrl-cを押したときの処理
                        print("\n-----------")
                        print("main.py : ",e)
                        print("-----------\n")
                        my_exit()
                except Exception as e:
                    # 予期せぬエラーが発生した時の処理
                    stop()
                    # エラーの内容を残す(日付ごと)
                    error_log_write(e)
                    print("\n-----------")
                    print("\nmain.py Error :",e)
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
        print("main.py : ",key)
        print("-----------\n")
        my_exit()
