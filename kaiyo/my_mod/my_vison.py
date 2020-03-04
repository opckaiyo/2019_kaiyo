#!/bin/env python
# coding: utf-8
import time

import sys
sys.path.append("/kaiyo/my_mod")
# from my_get_serial import get_data, send_data
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, br_xr, go_back_each, up_down_each, spinturn_each, spinturn_meca
from my_voice import jtalk, jtalk_say
from my_gpio import led_red, led_green, led_yellow, led_off, led_blue, led_purple, led_lihtblue



def my_main(val):
    if val == "a":
        # jtalk(file_name="modea", voice="エイチワイの皆さんこんにちは、これから、海洋ロボットの説明を始めます。　私のなまえは「ちぶるまぎーもでるじーです」")
        jtalk(file_name="modea", voice="皆さんこんにちは、これから、海洋ロボットの説明を始めます。　私のなまえは「ちぶるまぎーもでるじーです」")

    if val == "b":
        jtalk(file_name="modedb", voice="私は「海洋ロボットコンペティション、イン、沖縄」に出場するためにかいはつされた、海洋ロボットです。")

    if val == "c":
        jtalk(file_name="modedc", voice="私は主に、アルミニウムとアクリルで構成されています。モータには12ボルトのDCモータ、メインコントローラにはラズベリーパイモデルBを使用しています。バッテリは11.1ボルトのしゅ制御用と「制御回路用」の7.4ボルトのリポバッテリを使用しています。センサ類は主に方向検出用の9軸センサ、水深の検出には圧力センサ、また、各スラスターにはモータの回転数を検出するための「ロータリエンコーダ」を搭載しています。")
        # jtalk(file_name="modedc2", voice="潜航深度は最大で5メートル、航行速度は最大で2メートル毎秒です。")
        # jtalk(file_name="modedc3", voice="それでは、実際にスラスタを動かしてみたいと思います。機体から少しだけ離れてください。　このスラスタで潜水や浮上を行います。　　")
        # jtalk(file_name="modedc4", voice="また、こちらのスラスタでは、前進や行進、旋回などを行います。　　")
        # jtalk(file_name="modedc5", voice="また、こちらのLEDは外部からロボットがどのような「動作」をしているかがわかりやすいように7しょくで「現在」の状態を表現しています")
        # jtalk(file_name="modedc6", voice="これで海洋ロボットの説明を終了します。ご清聴、ありがとうございました。")

    if val == "d":
        jtalk_say(file_name="modea")
        time.sleep(9)
        jtalk_say(file_name="modedb")
        time.sleep(10)
        # jtalk_say(file_name="modedc")
        jtalk_say(file_name="sensor_add")
        time.sleep(23)
        jtalk_say(file_name="sensor_add2")
        time.sleep(40)
        jtalk_say(file_name="modedc2")
        time.sleep(8)

        jtalk_say(file_name="modedc3")
        led_blue()
        time.sleep(7)
        up_down(20)
        time.sleep(2)
        up_down(90)
        time.sleep(3)
        stop()
        led_off()

        jtalk_say(file_name="modedc4")
        led_purple()
        time.sleep(3)
        go_back(20)
        time.sleep(2)
        go_back(90)
        time.sleep(3)
        stop()
        led_off()


        jtalk_say(file_name="modedc5")
        led_red()
        time.sleep(1.5)
        led_blue()
        time.sleep(1.5)
        led_green()
        time.sleep(1.5)
        led_purple()
        time.sleep(1.5)
        led_yellow()
        time.sleep(1.5)
        led_lihtblue()
        time.sleep(1.5)
        led_off()
        time.sleep(3)

        jtalk_say(file_name="modedc6")



def atumeru_led():
    time_led = 0.1
    for i in range(12):
        led_red()
        time.sleep(time_led)
        led_red()
        time.sleep(time_led)
        led_green()
        time.sleep(time_led)
        led_purple()
        time.sleep(time_led)
        led_yellow()
        time.sleep(time_led)
        led_lihtblue()
        time.sleep(time_led)
        led_off()

if __name__ == '__main__':
    # jtalk(file_name="sensor_add", voice="")
    # jtalk(file_name="sensor_add", voice="私は主に、アルミニウムとアクリルで構成され,、腐食を防ぐために表面はアルマイト処理されています。モータには12ボルトのDCモータ、メインコントローラにはラズベリーパイモデルビーーを使用しています。バッテリは11.1ボルトの主制御用と「制御回路用」の7.4ボルトのリポバッテリを使用しています。")

    # jtalk(file_name="sensor_add2", voice="センサ類は主に方向検出用の9軸センサ、潜っている深さの検出には圧力センサ、波の強さを検出するための流量計、また、各スラスターにはモータの回転数を検出するための「ロータリエンコーダー」、モータにかかる負荷を監視するための「電流計」、モータの温度を確認するための「温度センサ」を搭載しています。また、前方と下方向の様子を確認するための「カメラ」を２つ、さらに私の向いている方向を、操縦者が目視で確認できるように「スマートフォン」を搭載しています。")
    # my_main(val = "d")
    try:
        while True:
            my_main(val = "d")
            time.sleep(60)

            # jtalk(file_name="min3", voice="皆さんこんにちは、今から3分後に自動デモンストレーションを開始します。ご覧になるかたは集まってください。")
            jtalk_say(file_name="min3")
            atumeru_led()
            time.sleep(60)
            # jtalk(file_name="min2", voice="皆さんこんにちは、今から2分後に自動デモンストレーションを開始します。ご覧になるかたは集まってください。")
            jtalk_say(file_name="min2")
            atumeru_led()
            time.sleep(60)
            # jtalk(file_name="min1", voice="皆さんこんにちは、今から1分後に自動デモンストレーションを開始します。ご覧になるかたは集まってください。")
            jtalk_say(file_name="min1")
            atumeru_led()
            time.sleep(50)
            # jtalk(file_name="sec10", voice="皆さんこんにちは、今から10秒後に自動デモンストレーションを開始します。ご覧になるかたは集まってください。")
            jtalk_say(file_name="sec10")
            atumeru_led()
            time.sleep(10)
    except KeyboardInterrupt as e:
        print("\nCtrl-c!!")
        led_off()
        stop()
