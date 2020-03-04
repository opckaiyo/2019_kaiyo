#coding: utf-8
#! /usr/bin/env python3

# import readchar
import time
from datetime import datetime
import sys
import os
import ast



# 自作関数のインポート
sys.path.append("/kaiyo/my_mod")
# PCA9685と通信しモータを制御する関数
from my_motor import go_back,  up_down,  spinturn,  roll,  stop,  stop_go_back,  stop_up_down,  go_back_each,  up_down_each,  spinturn_each,  xrf,  xrb,  xlf,  xlb,  yr,  yl
# プログラムスタート時にロボットの状態や初期設定の動作を行う関数
# from my_check import my_exit
# ArduinoMegaとシリアル通信してセンサデータをもらう関数
from my_get_serial import get_data,  send_data


# ティーチング用のログ作成またはログを読込んで機体を動かす
# data:センサーデータ　set_input_kb:1ログ作成・0読込みの切り替え
def move_test(data, kb, m_val, goal_yaw, yaw_MV, goal_depth, depth_MV,
 set_yaw, set_depth, old_rot=[0]*6, set_input_kb=True):
    # m_val = 30
    # CTRL_C = 3
    # 大会用のログ
    path1 ='/kaiyo/log/input_log/read_input_log.txt'
    # 直前の入力ログ　次回実行時に消える
    path2 ='/kaiyo/log/input_log/just_before_read_input_log.txt'

    # ティーチング用のログを作る-----------------------------------------
    if set_input_kb == True:
        # 今日の日付でフォルダを作る
        try:
            os.makedirs('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d')))
        except FileExistsError:
            pass
        # input_log_file_make = open('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d'))+'/input_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt',  'a')
        input_log_file_make = open('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d'))+'/input_log_.txt',  'a')
        just_before_input_log_file = open('/kaiyo/log/input_log/just_before_read_input_log.txt',  'a')

    # ティーチング用のログを作る-----------------------------------------


    # ティーチング用のログを読込む---------------------------------------
    # elif set_input_kb == False:
    if set_input_kb == False:
        try:
            if kb == '9':
                path = path1
            if kb == '0':
                path = path2
            with open(path) as f:
                # l_strip = [s.strip() for s in f.readlines()]
                # input_log_file_read = ast.literal_eval(l_strip[1])

                input_log_file_read = [s.strip() for s in f.readlines()]
                fr_len = len(input_log_file_read)
        except FileExistsError:
            print("file_error")
            pass
        else:
            print("move start")

    # ティーチング用のログを読込む---------------------------------------


    line_num = 0
    now_rot  = 0
    next_rot = 0
    data_rot = 0
    old_data_rot = 0
    s_flg = 0

    while True:
        try:
            # ログのから１行ずつ処理
            if set_input_kb == False:
                # print(line_num)

                now_line = ast.literal_eval(input_log_file_read[line_num])
                # リストがあるなら
                # rot4, 5を使っているのはロータリーが4つしか取れなかったから配線を入れ替えたため
                if line_num + 1 < fr_len:
                    next_line = ast.literal_eval(input_log_file_read[line_num + 1])
                    next_rot = (next_line["rot0"] + next_line["rot1"] + next_line["rot4"] + next_line["rot5"]) / 4

                data_rot = (data["rot0"] + data["rot1"] + data["rot4"] + data["rot5"]) / 4
                now_rot = (now_line["rot0"] + now_line["rot1"] + now_line["rot4"] + now_line["rot5"]) / 4
                print("line_num", line_num, "next_key:", now_line['input_key'], "kb:", kb, "data:", data_rot, "now:", now_rot, "next:", next_rot, "差:", (old_data_rot - next_rot), "残:", (now_rot - (data_rot - old_data_rot)), "\n")

                if line_num == 0 :
                    line_num = line_num + 1

                    kb = str(now_line['input_key'])
                    m_val = now_line['m_val']
                    goal_yaw.value = now_line['goal_yaw']
                    goal_depth.value = now_line['goal_depth']
                    set_yaw.value = now_line['set_yaw']
                    set_depth.value = now_line['set_depth']
                    old_data_rot = data_rot
                    print("test,test0", set_yaw, set_depth)


                else:
                    # ロータリが指定回数以上回った　か　スラスタが回らないコマンドだったら　次の行を読み込む
                    if  (((now_rot - (data_rot - old_data_rot)) <= 0) or (kb == 's') or s_flg == 1):# and ((kb != 'A') or (kb != 'D')):
                        s_flg = 0
                        line_num = line_num + 1
                        # 各値の更新
                        kb = str(now_line['input_key'])
                        m_val = now_line['m_val']
                        goal_yaw.value = now_line['goal_yaw']
                        goal_depth.value = now_line['goal_depth']
                        set_yaw.value = now_line['set_yaw']
                        set_depth.value = now_line['set_depth']
                        old_data_rot = data_rot
                        print("data_rot",old_data_rot)
                        print("test, test1", set_yaw, set_depth)




            # キー入力のログを残す
            if set_input_kb == True:
                # input_log_file_make.write("{'time':" + str(datetime.now().strftime('%M:%S.%f')) +",  'inputkey':" + str(kb) + ",  'moterval':" + str(m_val) + "}\n")
                # end_time = time.time()

                # 日付ごとに入力したログ用
                input_log_file_make.write(
                "{'time':" + str(data["time"]) +
                ",  'input_key':'" + str(kb) + "'" +
                ",  'm_val':" + str(m_val) +
                ",  'goal_yaw':" + str(goal_yaw.value) +
                ",  'goal_depth':" + str(goal_depth.value) +
                ",  'set_yaw':" + str(set_yaw.value) +
                ",  'set_depth':" + str(set_depth.value) +
                ",  'rot0':" + str(data["rot0"] - old_rot[0]) +
                ",  'rot1':" + str(data["rot1"] - old_rot[1]) +
                ",  'rot2':" + str(data["rot2"] - old_rot[2]) +
                ",  'rot3':" + str(data["rot3"] - old_rot[3]) +
                ",  'rot4':" + str(data["rot4"] - old_rot[4]) +
                ",  'rot5':" + str(data["rot5"] - old_rot[5]) +
                "}\n")
                # 直前の動作用
                just_before_input_log_file.write(
                "{'time':" + str(data["time"]) +
                ",  'input_key':'" + str(kb) + "'" +
                ",  'm_val':" + str(m_val) +
                ",  'goal_yaw':" + str(goal_yaw.value) +
                ",  'goal_depth':" + str(goal_depth.value) +
                ",  'set_yaw':" + str(set_yaw.value) +
                ",  'set_depth':" + str(set_depth.value) +
                ",  'rot0':" + str(data["rot0"] - old_rot[0]) +
                ",  'rot1':" + str(data["rot1"] - old_rot[1]) +
                ",  'rot2':" + str(data["rot2"] - old_rot[2]) +
                ",  'rot3':" + str(data["rot3"] - old_rot[3]) +
                ",  'rot4':" + str(data["rot4"] - old_rot[4]) +
                ",  'rot5':" + str(data["rot5"] - old_rot[5]) +
                "}\n")

                old_rot[0] = data["rot0"]
                old_rot[1] = data["rot1"]
                old_rot[2] = data["rot2"]
                old_rot[3] = data["rot3"]
                old_rot[4] = data["rot4"]
                old_rot[5] = data["rot5"]


            # モータ一個ずつ動かす------------------------
            if kb == '1':   #xlf
                xlf(m_val)
                print("xlf:", m_val)

            if kb == '2':   #xrf
                xrf(-m_val)
                print("xrf:", m_val)

            if kb == '3':   #xl
                xlb(m_val)
                print("xlb:", m_val)

            if kb == '4':   #xr
                xrb(-m_val)
                print("xrb:", m_val)

            if kb == '5':   #yl
                yl(m_val)
                print("yl:", m_val)

            if kb == '6':   #yr
                yr(-m_val)
                print("yr:", m_val)

            # モータ一個ずつ動かす------------------------

            # 航行---------------------------------------
            if kb == 'w':   #前進
                go_back(m_val)
                print("前進:", m_val)

            if kb == 'W':   #前進
                if set_yaw.value == True:
                    set_yaw.value = False
                    stop()
                    print("制御前進:end", set_yaw.value)
                    s_flg = 1
                else:
                    set_yaw.value = True
                    print("制御前進:end_key:W", set_yaw.value)
                # s_flg = 1

            if set_yaw.value == True:
                if ( yaw_MV.value >= 0 ):
                    go_back_each(
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value,
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value)
                elif ( yaw_MV.value < 0 ):
                    go_back_each(
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value,
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value)

            if set_yaw.value == True:
                if ( yaw_MV.value >= 0 ):
                    go_back_each(
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value,
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value)
                elif ( yaw_MV.value < 0 ):
                    go_back_each(
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value,
                    m_val + yaw_MV.value,
                    m_val - yaw_MV.value)

            if kb == 'x':   #後退
                go_back(-m_val)
                print("後退:", m_val)

            if kb == 'q':   #潜水
                up_down(-m_val)
                print("潜水:", m_val)

            if kb == 'X':   #制御潜水
                if set_depth.value == True:
                    set_depth.value = False
                    stop()
                    print("制御潜水:end")
                else:
                    set_depth.value = True
                    print("制御潜水:end_key:X")

            if set_depth.value == True:   #前進
                print("depth_MV.value:", depth_MV.value)
                up_down(depth_MV.value)
                print("制御前進:", m_val)

            if kb == 'e':   #上昇
                up_down(m_val)
                print("上昇:", m_val)

            if kb == 'z':   #左傾き
                roll(m_val)
                print("左傾き:", m_val)

            if kb == 'c':   #右傾き
                roll(-m_val)
                print("右傾き:", m_val)

            if kb == 'a':   #左旋回
                spinturn(m_val)
                print("右旋回:", m_val)

            if kb == 'd':   #右旋回
                spinturn(-m_val)
                print("左旋回:", m_val)

            if (kb == 'A') or (kb == 'D'):   #180旋回
                set_yaw.value = False
                goal_yaw.value = goal_yaw.value + 180
                if goal_yaw.value >= 360:
                    goal_yaw.value = 0
                # ある程度旋回させる (180度超えないぐらいがいいと思う)
                if (kb == 'A'):
                    spin_val = 60
                if (kb == 'D'):
                    spin_val = -60
                spinturn(spin_val)
                time.sleep(3.5)
                # 回転させたときの誤差を修正
                while True:
                    try:
                        print("goal",goal_yaw.value,"com:",data["compass"],
                        "yaw",(abs(data["yaw"]) - 10), (abs(data["yaw"])), (abs(data["yaw"] + 10)), "180度旋回:", yaw_MV.value)

                        yaw_val = 10 * yaw_MV.value
                        yaw_val = min(60, yaw_val)
                        # if (yaw_val >= 60):
                        #     yaw_val = 60
                        spinturn(yaw_MV.value)

                        if ((data["yaw"] - 10) < goal_yaw.value < (data["yaw"] + 10)) or \
                           ((data["yaw"] - 10) > goal_yaw.value > (abs(data["yaw"] + 10))):
                            break
                        time.sleep(0.2)

                    except KeyboardInterrupt as e:
                        # Ctrl-cを押したときの処理
                        print("\n-----------")
                        print("move.py_180trun : ", e)
                        print("-----------\n")

                # line_num = line_num + 1
                s_flg = 1
                print("spin_end")
                stop_go_back()


            if kb == 'E':   #右前
                xlf(m_val * 1.3)
                xrb(-m_val)
                print("右前:", m_val)

            if kb == 'Q':   #左前
                xrf(-m_val * 1.3)
                xlb(m_val)
                print("左前:", m_val)

            if kb == 'C':   #右後
                xlf(-m_val * 1.3)
                xrb(m_val)
                print("右後:", m_val)

            if kb == 'Z':   #左後
                xrf(m_val * 1.3)
                xlb(-m_val)
                print("左後:", m_val)


            # 航行---------------------------------------


            # 停止---------------------------------------
            if kb == 's':   #全停止
                stop()
                print("全停止:")

            if kb == 'g':   #推進用停止
                stop_go_back()
                print("推進用停止:")

            if kb == 'v':   #潜水用停止
                stop_up_down()
                print("潜水用停止:")

            # 停止---------------------------------------

            # オプション---------------------------------------

            if kb == 'i':   #データ表示
                print(data)

            if kb == 'R':   #データ表示
                old_rot[0] = 0
                old_rot[1] = 0
                old_rot[2] = 0
                old_rot[3] = 0
                old_rot[4] = 0
                old_rot[5] = 0
                while True:
                    try:
                        print("send:reboot")
                        send_data("reboot")
                        time.sleep(1)

                        if data["time"] <= 10.0:
                            # time.sleep(1)
                            print("OK\n Start")
                            break

                    except TimeoutError:
                        print("main:timeout Error!\n")

                    except SyntaxError:
                        # 受信エラー
                        print("main : Reception Error!!\n")

            # yawの目標値を変更する
            if kb == 'y':
                print("g_now:", goal_yaw.value, "y_now", data["yaw"])
                in_str = input("goal_yaw.val=")
                goal_yaw.value = int(in_str)
                print(goal_yaw.value)

            if kb == 't':
                print("now", goal_depth.value)
                in_str = input("goal_depth.val=")
                goal_depth.value = float(in_str)
                print(goal_depth.value)

            if kb == 'f':   #arduinoにコマンド送信
                in_str = input("command>>>")
                send_data(in_str)

            if kb == 'h':
                print("'run':'シリアル通信を開始する。',  ");
                print("'stop':'シリアル通信を停止する。',  ");
                print("'reboot':'Arduinoを再起動する。',  ");
                print("'reset xxx':'curまたはrotの値をリセットする。',  ");
                print("'debug on/off':'デバッグモードに移行/通常モードに戻る。',  ");
                print("'time XXXX':'無限ループ時の待機時間をXXXXミリ秒にする。',  ");
                print("'yaw_zero off':'yawの初期リセット値を無効化',  ");
                print("'remove error':'状態を確認し問題なかったらstateをnormalにする',  ");
                print("'puropo on/off':'プロポを有効/無効にする',  ");

            if kb == 'b':   #指定時間潜水
                up_down(m_val)
                print("10秒潜水:", m_val)
                time.sleep(10)
                stop_up_down()

            if kb == 'n':   #指定時間浮上
                up_down(-m_val)
                print("3秒浮上:", m_val)
                time.sleep(3)
                stop_up_down()
                s_flg = 1
                print("3秒浮上終了")

            if kb == 'p':   #終了
                # my_exit()
                stop()
                print("終了します")
                return old_rot
            # オプション---------------------------------------

            # 意味なし
            if set_input_kb == True:
                if (kb == "w") or (kb == "W") or (kb == "s") or (kb == "a") or (kb == "A") or (kb == "d") or (kb == "D") or (kb == "x") or (kb == "X") or (kb == "p"):
                    return old_rot
                else:
                    return old_rot
                    # break
            # ティーチングのとき使うかもしれないからリセット
            if (kb != "W") or (kb != "X") or (kb != 's'):
                kb = None
            time.sleep(0.2)
            # print(kb)

        except KeyboardInterrupt as e:
            stop()
            prtin("move:Keyerror")
            break
        # except ValueError as e :
        #     stop()
        #     print("move:Valueerror")
        #     break




if __name__ == '__main__':
    while True:

        try:
            move_test(None, 1)
            # move_test(None, False)
            stop()
            break
            # go_back(50)
            # up_down(20)
            # go_back_each(10, 10, 0)
            # dc_u( 100 )
        except KeyboardInterrupt as e:
            stop()
            break
