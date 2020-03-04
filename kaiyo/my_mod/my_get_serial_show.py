# sudo pip install pyserial
import serial
import ast
import time
import sys
from datetime import datetime
from multiprocessing import Manager, Process
# from multiprocessing import Manager, Process, Queue, Lock
sys.path.append("/kaiyo/my_mod")

# ArduinoMEGAとpinで接続
# ser = serial.Serial('/dev/ttyS0', 115200,timeout=3)
# ArduinoMEGAとUSBケーブル接続
ser = serial.Serial('/dev/ttyACM0', 115200,timeout=3)

# def get_data():
#     while True:
#         # Arduino から一行取得
#         data = ser.readline()
#         # 受信エラー確認
#         try:
#             return data
#
#         except SyntaxError:
#             # 受信エラー
#             print("Reception Error!!")

def get_data(data):
    while True:
        # Arduino から一行取得
        val = ser.readline()
        # print("data")
        print(val,"\n")
        # 受信エラー確認
        try:
            # print("でーただよー")

            # dictに変換
            val = ast.literal_eval(val.decode('unicode-escape'))
            # print(val)
            for i in val:
                data[i] = val[i]

            # print(data,"\n")
        except SyntaxError:
            # 受信エラー
            print("Reception Error!!")
#ArduinoMEGAにコマンド送信---------------------------------------------

#("  'run':'シリアル通信を開始する。', ");
#("  'stop':'シリアル通信を停止する。', ");
#("  'reboot':'Arduinoを再起動する。', ");
#("  'reset xxx':'curまたはrotの値をリセットする。', ");
#("  'debug':'デバッグモードに移行offをつけると通常モードに戻る。', ");
#("  'time XXXX':'無限ループ時の待機時間をXXXXミリ秒にする。', ");
#("  'yaw_zero off':'yawの初期リセット値を無効化', ");
#("  'remove error':'状態を確認し問題なかったらstateをnormalにする', ");

#主に通信開始時に動機をとるために再起動する val = reboot

def send_data(val):
    ser.write(val.encode('unicode-escape'))

#ArduinoMEGAにコマンド送信---------------------------------------------


if __name__ == '__main__':
    # send_data("reboot")
    # data = ser.readline()
    # print("data:",data)
    # print(data.decode('unicode-escape'))
    # str = ast.literal_eval(data.decode('unicode-escape'))
    # print(str)

    print("wait:reboot now")
    while True:
        try:
            print("\nsend_data(reboot)\n")
            send_data("reboot")
            # print("\nsend_data(reboot)\n")
            # time.sleep(0.2)
            val = ser.readline() #.decode('unicode-escape') *#
            print("val1",val)
            val = ast.literal_eval(val.decode('unicode-escape'))
            print("val2",val)



            if val["time"] <= 10.0:
                print("Nice")
                # time.sleep(1)
                break

        except SyntaxError:
            # 受信エラー
            print("\nserial : Reception Error!!\n")
        except TimeoutError:
            print("serial : timeout Error!\n")
        # except ValueError:
        #     print("serial : Value Error!\n")


    while True:
        print("OK")
        # print type(get_data("all"))
        # get_read_data()
        # print("b   ",data)
        # get_read_data()
        # print(get_data())
        get_data(val)
        # print(data)
        # get_data("depth")
        # print("str")
        # print(str)

    ser.close()
