#! /usr/bin/env python
#coding: utf-8

import time
import Adafruit_PCA9685
import sys
sys.path.append("/kaiyo/my_mod")
# from my_state_write import state_write

pwm = Adafruit_PCA9685.PCA9685()
# pwm周波数設定
# pwm.set_pwm_freq(66)
# pwm.set_pwm_freq(500)
pwm.set_pwm_freq(1000)

# コマンド----------------------------------------------
# set_pwm_freq(周波数Hz)
# set_pwm(チャンネル番号, パルスのスタート, パルスの終了)
# ------------------------------------------------------

# HAT-MDD10ピン設定
# --------------------------------
br_xr_pwm = 2
br_xl_pwm = 3
# ---------------
dc_xr_pwm = 7
dc_xr_dir = 13
# ---------------
# dc_xl_pwm = 8
# dc_xl_dir = 4

# ドライバ負荷軽減
dc_xl_pwm = 12
dc_xl_dir = 6
# ---------------
dc_yr_pwm = 9
dc_yr_dir = 14
# ---------------
dc_yl_pwm = 10
dc_yl_dir = 5
# ---------------
dc_u_pwm = 11
dc_u_dir = 15
# --------------------------------


# モータ1個の関数
def br_xr(val):
    val = my_map_br(val)
    pwm.set_pwm(br_xr_pwm, 0, int(val))

def br_xl(val):
    val = my_map_br(val)
    pwm.set_pwm(br_xl_pwm, 0, int(val))

def dc_xr( val ):
    val, pone = my_map(val)
    pwm.set_pwm(dc_xr_pwm, 0, int(val))
    pwm.set_pwm(dc_xr_dir, 0, pone)

def dc_xl( val ):
    val, pone = my_map(val)
    pwm.set_pwm(dc_xl_pwm, 0, int(val))
    pwm.set_pwm(dc_xl_dir, 0, pone)

def dc_yr( val ):
    val, pone = my_map(val)
    pwm.set_pwm(dc_yr_pwm, 0, int(val))
    pwm.set_pwm(dc_yr_dir, 0, pone)

def dc_yl( val ):
    val, pone = my_map(val)
    pwm.set_pwm(dc_yl_pwm, 0, int(val))
    pwm.set_pwm(dc_yl_dir, 0, pone)

def dc_u( val ):
    motor_vals("dc_u", val)
    val, pone = my_map(val)
    pwm.set_pwm(dc_u_pwm, 0, int(val))
    pwm.set_pwm(dc_u_dir, 0, pone)

def solenoid_on():
    val, pone = my_map(99)
    pwm.set_pwm(dc_u_pwm, 0, int(val))
    pwm.set_pwm(dc_u_dir, 0, pone)

def solenoid_off():
    val, pone = my_map(0)
    pwm.set_pwm(dc_u_pwm, 0, int(val))
    pwm.set_pwm(dc_u_dir, 0, pone)


# 前進_後進(go_back)
def go_back( val ):
    dc_xl(val)
    dc_xr(-val)
    # dc_u(val)

# 前進_後進(それぞれの出力を指定）
def go_back_each(l, r):
    dc_xl(l)
    dc_xr(-r)
    # dc_u( u )

# 上昇_下降(up_down)
def up_down( val ):
    dc_yl(val)
    dc_yr(-val)

# 上昇_下降(それぞれの出力を指定)
def up_down_each( l, r ):
    dc_yl(l)
    dc_yr(-r)

# 右回り_左回り(spinturn)
def spinturn( val ):
    dc_xl(val)
    dc_xr(val)


# 右回り_左回り(それぞれの出力を指定)
def spinturn_each( l, r ):
    dc_xl(l)
    dc_xr(-r)

# 右傾き_左傾き
def roll( val ):
    dc_yl(val)
    dc_yr(val)

# 停止
def stop():
    # print"\nSTOP"
    pwm.set_pwm(dc_xr_pwm, 0, 0)
    pwm.set_pwm(dc_xl_pwm, 0, 0)
    pwm.set_pwm(dc_yr_pwm, 0, 0)
    pwm.set_pwm(dc_yl_pwm, 0, 0)
    pwm.set_pwm(dc_u_pwm, 0, 0)

def stop_pump():
    pwm.set_pwm(dc_u_pwm, 0, 0)

def stop_go_back():
    # print"\nSTOP_GO_BACK"
    pwm.set_pwm(dc_xr_pwm, 0, 0)
    pwm.set_pwm(dc_xl_pwm, 0, 0)
    pwm.set_pwm(dc_u_pwm, 0, 0)

def stop_up_down():
    # print"\nSTOP_UP_DOWN"
    pwm.set_pwm(dc_yr_pwm, 0, 0)
    pwm.set_pwm(dc_yl_pwm, 0, 0)



# 値変換関数----
# 値変換関数(入力0-100, 出力0-4000)
def my_map(val):
    # val = my_map_half(val)
    if val == 0:
        val = 0
        pone = 1
    elif val >= 0:
        pone = 4000
        in_min = 0
        in_max = 100
        out_min = 0
        out_max = 4000
        val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    else:
        pone = 1
        in_min = 0
        in_max = -100
        out_min = 0
        out_max = 4000
        val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    return val, pone


# 値変換関数----
# 値変換関数(入力0-100, 出力0-4000)
def my_map_half(val):
    if val == 0:
        val = 0
        pone = 1
    elif val >= 0:
        pone = 4000
        in_min = 0
        in_max = 100
        out_min = 0
        out_max = 20
        val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    else:
        pone = 1
        in_min = 0
        in_max = -100
        out_min = 0
        out_max = -20
        val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    return val


def my_map_br( val ):
    in_min = -100
    in_max = 100
    out_min = 200
    out_max = 640
    val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    return val


if __name__ == '__main__':
    while True:
        stop()
        try:
            spinturn(10)
            # dc_xl(30)
        except KeyboardInterrupt as e:
            stop()
            break
