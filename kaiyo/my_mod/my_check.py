#coding: utf-8
#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import configparser
import distutils.util
from multiprocessing import Manager, Process
import sys
sys.path.append("/kaiyo/my_mod")
from my_get_serial import get_data, send_data
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down,go_back_each, up_down_each, spinturn_each
# from my_balance import yaw, go_yaw_time
from my_rc import t10j
from my_gpio import led_red, led_green, led_yellow, led_off, led_blue, led_purple, led_lihtblue
from my_voice import jtalk
from my_data_sampling import data_sampling
from my_gps import get_gps_data
from my_camera3 import camera



# -------------------------------------------------------------------
# プログラムを終了する手順
def my_exit():
    led_off()
    GPIO.cleanup()
    stop()
    sys.exit()


# 起動前にマシンの状態をチェック
def battery_check(set_lipoC2=8, set_lipoC3S3=11):
    data = get_data("all")
    print()
    print("----------------------------------")
    print("Lipo checking!!")
    time.sleep(0.5)


    if data["lipoC2"] <= set_lipoC2 or data["lipoC3S3"] <= set_lipoC3S3:
        if data["lipoC2"] <= 1 or data["lipoC3S3"] <= 1:
            if data["lipoC2"] <= 1:
                print("lipoC2 : No connection!!")
            if data["lipoC3S3"] <= 1:
                print("lipoC3S3 : No connection!!")
        else:
            while True:
                if data["lipoC2"] <= set_lipoC2:
                    print("lipoC2 : "+str(get_data("lipoC2"))+"[V]")
                if data["lipoC3S3"] <= set_lipoC3S3:
                    print("lipoC3S3 : "+str(get_data("lipoC3S3"))+"[V]")

                print("Lipo Low!!")
                led_red()
                time.sleep(0.1)
                led_off()
                time.sleep(0.1)

    print("lipoC2 : "+str(get_data("lipoC2"))+"[V]")
    print("lipoC3S3 : "+str(get_data("lipoC3S3"))+"[V]")
    print("Status okay!!")
    print("----------------------------------")
    print()

# 動作確認
def operation_check():
    while True:
        my_time = 0.002
        print("Do you check the operation? [Y/n]")
        key_in = input()

        if key_in == "y" or key_in == "Y":
            print("Yes operation check!!")
            for i in range(100):
                go_back_each(i, 0)
                print(i)
                time.sleep(my_time)
            for i in range(100):
                go_back_each(0, i)
                print(i)
                time.sleep(my_time)
            stop()
            for i in range(100):
                up_down_each(0, i)
                print(i)
                time.sleep(my_time)
            for i in range(100):
                up_down_each(i, 0)
                print(i)
                time.sleep(my_time)
            stop()
            for i in range(0, -100, -1):
                up_down_each(i, 0)
                print(i)
                time.sleep(my_time)
            for i in range(0, -100, -1):
                up_down_each(0, i)
                print(i)
                time.sleep(my_time)
            stop()
            for i in range(0, -100, -1):
                go_back_each(0, i)
                print(i)
                time.sleep(my_time)
            for i in range(0, -100, -1):
                go_back_each(i, 0)
                print(i)
                time.sleep(my_time)
            stop()
            for i in range(0, -100, -1):
                go_back_each(i, i)
                up_down_each(i, i)
                print(i)
                time.sleep(my_time)
            stop()
            for i in range(0, 100, 1):
                go_back_each(i, i)
                up_down_each(i, i)
                print(i)
                time.sleep(my_time)
            stop()
            print("It worked normally!!")
            return 0
        elif key_in == "n" or key_in == "N":
            print("No operation check!!")
            return 0

# 取得した値を読み上げ
def voice_check(val):
    data = get_data("all")
    print(data[val])
    time.sleep(1)

# 最初の動作
def first_action(sensordata):

    # 設定ファイルから設定やパラメータを読み込む
    inifile = configparser.SafeConfigParser()
    inifile.read('/kaiyo/my_config/my_config.ini')
    set_send_reboot =       distutils.util.strtobool(inifile.get('set_mode', 'set_send_reboot'))
    set_battery_check =     distutils.util.strtobool(inifile.get('set_mode', 'set_battery_check'))
    set_sensor_log =        distutils.util.strtobool(inifile.get('set_mode', 'set_sensor_log'))
    set_gps_log =           distutils.util.strtobool(inifile.get('set_mode', 'set_gps_log'))
    set_camera =            distutils.util.strtobool(inifile.get('set_mode', 'set_camera'))
    set_operation_check =   distutils.util.strtobool(inifile.get('set_mode', 'set_operation_check'))
    set_move_test =         distutils.util.strtobool(inifile.get('set_mode', 'set_move_test'))
    set_start_mgs =         distutils.util.strtobool(inifile.get('set_mode', 'set_start_mgs'))
    set_send_pwm =          distutils.util.strtobool(inifile.get('set_mode', 'set_send_pwm'))
    set_countdown =         int(inifile.get('set_mode', 'set_countdown'))

    print()
    print("----------------------------------")
    print("set_send_reboot :",      set_send_reboot)
    print("set_battery_check :",    set_battery_check)
    print("set_sensor_log :",       set_sensor_log)
    print("set_gps_log :",          set_gps_log)
    print("set_camera :",           set_camera)
    print("set_operation_check :",  set_operation_check)
    print("set_start_mgs :",        set_start_mgs)
    print("set_send_pwm :",         set_send_pwm)
    print("set_countdown :",        set_countdown)
    print("set_move_test :",        set_move_test)
    print("----------------------------------")

    # 念のためモーターstop
    stop()

    if set_send_reboot:
        # センサー初期化
        send_data("reboot")

    if set_battery_check:
        # マシンの状態をチェック
        battery_check(set_lipoC2=7.0, set_lipoC3S3=11)

    # 待機状態のLEDをセット
    led_purple()


    if set_operation_check:
        # 動作チェックするか？
        operation_check()

    if set_start_mgs:
        # リードスイッチでスタート
        # data =  get_data("all")

        # スタート動作なし
        # while data["mgs"] == 1:
        # スタート動作あり
        while data["mgs"] == 0:
            data =  get_data("all")
            print(data["mgs"])
            print("Ready !!")

    print("\nPlease wait!!")
    # センサー初期化
    send_data("reboot")
    time.sleep(0.5)
    send_data("reboot")
    time.sleep(0.5)
    send_data("reboot")
    time.sleep(0.5)


    if set_send_pwm:
        # プロポ受信モード
        send_data("pwm on")

        # センサを安定状態にするため
        for i in range(20):
            data = get_data("all")


    if set_sensor_log:
        set_sample_rate = 0.2
        sensor_process = Process(target=data_sampling, args=[data,set_sample_rate])
        sensor_process.start()

    #
    # if set_gps_log:
    #     gps_process = Process(target=get_gps_data, args=())
    #     gps_process.start()
    #
    # if set_camera:
    #     camera_process = Process(target=camera2)
    #     camera_process.start()



    if set_countdown:
        # カウントダウン
        for cnt in range(set_countdown, 0, -1):
            led_red()
            print(cnt)
            time.sleep(0.5)
            led_off()
            time.sleep(0.5)

        print("Go !!")


# -------------------------------------------------------------------
if __name__ == '__main__':
    # operation_check()
    first_action()

    while True:
        # send_data("reboot")
        try:
            # voice_check("yaw")
            pass

        except KeyboardInterrupt as e:
            stop()
            break
