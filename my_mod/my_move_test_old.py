#coding: utf-8
#! /usr/bin/env python3

import readchar
import time
from datetime import datetime
import sys
import os
import ast


# 自作関数のインポート
sys.path.append("/kaiyo/my_mod")
# PCA9685と通信しモータを制御する関数
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each, xrf, xrb, xlf, xlb, yr, yl
# プログラムスタート時にロボットの状態や初期設定の動作を行う関数
# from my_check import my_exit
# ArduinoMegaとシリアル通信してセンサデータをもらう関数
# from my_get_serial import get_data, send_data

# ティーチング用のログ作成またはログを読込んで機体を動かす
# data:センサーデータ　set_input_kb:1ログ作成・0読込みの切り替え
def move_test(data,set_input_kb=True):
    m_val = 30

    path1 ='/kaiyo/log/input_log/20191003/input_log_20191003_122640.txt'

    # ティーチング用のログを作る-----------------------------------------
    if set_input_kb == True:
        try:
            os.makedirs('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d')))
        except FileExistsError:
            pass
        input_log_file_make = open('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d'))+'/input_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt', 'a')

    # ティーチング用のログを作る-----------------------------------------


    # ティーチング用のログを読込む---------------------------------------
    elif set_input_kb == False:
        try:

            with open(path1) as f:
                # l_strip = [s.strip() for s in f.readlines()]
                # input_log_file_read = ast.literal_eval(l_strip[1])

                input_log_file_read = [s.strip() for s in f.readlines()]
                fr_len = len(input_log_file_read)
        except FileExistsError:
            print("file_error")
            pass

    # ティーチング用のログを読込む---------------------------------------


    line_num = 0
    start_time = time.time()
    kb = 'p'
    print("move_start")

    while True:
        try:
            # print ("input please:")
            # if(readchar.readchar() != null):

            # ソケット通信からキー入力が来る予定
            if set_input_kb == True:
                # とりあえずソケットなしでキー入力
                kb = readchar.readchar()

            # ログのから１行ずつ処理
            elif set_input_kb == False:
                # print(line_num)

                now_line = ast.literal_eval(input_log_file_read[line_num])
                # リストがあるなら
                if line_num + 1 < fr_len:
                    next_line = ast.literal_eval(input_log_file_read[line_num + 1])

                if line_num == 0 :
                    print("now:",now_line)
                    print("next",next_line)
                    print()
                    # time.sleep(next_line['time'])
                    kb = str(now_line['inputkey'])
                    line_num = line_num + 1

                else:
                    print("now:",now_line)
                    print("next",next_line)
                    print()
                    time.sleep(next_line['time'] - now_line['time'])
                    kb = str(now_line['inputkey'])
                    line_num = line_num + 1



                # print(type(kb))
            # print(type(kb))
            # print(kb)
            # kb = kb.decode()
            # print(kb)

            # キー入力のログを残す
            if set_input_kb == True:
                # input_log_file_make.write("{'time':" + str(datetime.now().strftime('%M:%S.%f')) +", 'inputkey':" + str(kb) + ", 'moterval':" + str(m_val) + "}\n")
                end_time = time.time()
                input_log_file_make.write("{'time':" + str(round(end_time - start_time,2)) +", 'inputkey':'" + str(kb) + "', 'moterval':" + str(m_val) + "}\n")


            # モータ出力------------------------
            if kb == 'k':   #モータ出力の低下
                if m_val > 0:
                    m_val = m_val - 5;
                    print(m_val)

            if kb == 'l':   #モータ出力の上昇
                if m_val < 65:
                    m_val = m_val + 5;
                    print(m_val)

            # モータ出力------------------------


            # モータ一個ずつ動かす------------------------
            if kb == '1':   #xlf
                xlf(m_val)
                print("xlf:",m_val)

            if kb == '2':   #xrf
                xrf(-m_val)
                print("xrf:",m_val)

            if kb == '3':   #xl
                xlb(m_val)
                print("xlb:",m_val)

            if kb == '4':   #xr
                xrb(-m_val)
                print("xrb:",m_val)

            if kb == '5':   #yl
                yl(m_val)
                print("yl:",m_val)

            if kb == '6':   #yr
                yr(-m_val)
                print("yr:",m_val)

            # モータ一個ずつ動かす------------------------

            # 航行---------------------------------------
            if kb == 'w':   #前進
                go_back(m_val)
                print("前進:",m_val)

            if kb == 'x':   #後退
                go_back(-m_val)
                print("後退:",m_val)

            if kb == 'q':   #潜水
                up_down(-m_val)
                print("潜水:",m_val)

            # if kb == 'f':   #潜水
            #     up_down(depth_MV)
            #     print("潜水:",m_val)

            if kb == 'e':   #上昇
                up_down(m_val)
                print("上昇:",m_val)

            if kb == 'z':   #左傾き
                roll(m_val)
                print("左傾き:",m_val)

            if kb == 'c':   #右傾き
                roll(-m_val)
                print("右傾き:",m_val)

            if kb == 'a':   #左旋回
                spinturn(m_val)
                print("右旋回:",m_val)

            if kb == 'd':   #右旋回
                spinturn(-m_val)
                print("左旋回:",m_val)

            # 航行---------------------------------------


            # 停止---------------------------------------
            if kb == 's':   #全停止
                stop()
                print("全停止:")

            if kb == 'r':   #推進用停止
                stop_go_back()
                print("推進用停止:")

            if kb == 't':   #潜水用停止
                stop_up_down()
                print("潜水用停止:")

            # 停止---------------------------------------

            if kb == 'b':   #指定時間潜水
                up_down(m_val)
                print("潜水:",m_val)
                time.sleep(10)
                stop()

            if kb == 'p':   #終了
                # my_exit()
                stop()
                print("終了します")
                break


            # ティーチングのとき使うかもしれないからリセット
            kb = None
            # print(kb)

        except KeyboardInterrupt as e:
            stop()
            # prtin("move:Keyerror")
            break
        # except ValueError as e :
        #     stop()
        #     print("move:Valueerror")
        #     break


if __name__ == '__main__':
    while True:

        try:
            move_test(None,1)
            # move_test(None,False)
            stop()
            break
            # go_back(50)
            # up_down(20)
            # go_back_each(10,10,0)
            # dc_u( 100 )
        except KeyboardInterrupt as e:
            stop()
            break
