#coding: utf-8
import time
import sys
# sys.path.append("/kaiyo/serial")
sys.path.append("/kaiyo/my_mod")
from my_get_serial import get_data, send_data
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down,go_back_each, up_down_each, spinturn_each
from my_gpio import led_red, led_green, led_yellow, led_off, led_blue, led_purple, led_lihtblue


def t10j_map_data():
    data =  get_data("all")
    # print "LY  LX  RY  RX"
    t10j_data = [data["duty2"], data["duty0"], data["duty1"], data["duty3"]]
    # print t10j_data

    t10j_map = []
    for val in t10j_data:
        in_min = 1104
        in_max = 1918
        out_min = -100
        out_max = 100
        val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
        if val < -100: val = -100
        if val > 100: val = 100
        if val <= 10 and val >= -10: val = 0
        t10j_map.append(val)

    t10j_map = {"ly":t10j_map[0],"lx":t10j_map[1],"ry":t10j_map[2],"rx":t10j_map[3]}
    # print t10j_map
    return t10j_map


def t10j_start_check():
    while True:
        t10j_map = t10j_map_data()
        print("RY joystick upper!!")
        # if 100 == t10j_map["ly"] and t10j_map["lx"] and t10j_map["ry"] and t10j_map["rx"]:
        if 100 == t10j_map["ry"]:
            led_green()
            while True:
                t10j_map = t10j_map_data()
                print("RY joystick center!!")
                if 0 == t10j_map["ry"]:
                    while True:
                        print("Joysticks OK!!")
                        led_blue()
                        return 0

# -------------------------------------------------------------------


def t10j(set_time=10):
    t10j_start_check()
    # カウントダウン
    for cnt in range(3, 0, -1):
        # led_red()
        print(cnt)
        time.sleep(0.5)
        # led_off()
        time.sleep(0.5)

    # start_time = time.time()
    while True:
        t10j_map = t10j_map_data()
        print(t10j_map)

        ly = t10j_map["ly"]
        lx = t10j_map["lx"]
        ry = t10j_map["ry"]
        rx = t10j_map["rx"]

        m_xr = 0
        m_xl = 0
        m_yr = 0
        m_yl = 0

        # 0 ~ 90
        if ly >= 1 and lx >= 1:
            m_xl = ly
            m_xr = ly - lx

        # 91 ~ 180
        if ly >= 1 and lx <= -1:
            m_xr = ly
            m_xl = ly + lx

        # 180 ~ 270
        if ly <= -1 and lx <= -1:
            m_xr = ly
            m_xl = ly - lx

        # 270 ~ 360
        if ly <= -1 and lx >= 1:
            m_xl = ly
            m_xr = ly + lx

        # go_back
        if ly != 0 and lx == 0:
            m_xl = ly
            m_xr = ly

        # spinturn
        if lx != 0 and ly == 0:
            m_xl = lx
            m_xr = -lx

        # ----------------------------------

        if ry != 0 and rx == 0:
            m_yl = ry
            m_yr = ry

        if rx != 0 and ry == 0:
            m_yl = -rx
            m_yr = rx

        # 0 ~ 90
        if ry >= 1 and rx >= 1:
            m_yl = ry
            m_yr = ry - rx

        # 91 ~ 180
        if ry >= 1 and rx <= -1:
            m_yr = ry
            m_yl = ry + rx

        # 180 ~ 270
        if ry <= -1 and rx <= -1:
            m_yr = ry
            m_yl = ry - rx

        # 270 ~ 360
        if ry <= -1 and rx >= 1:
            m_yl = ry
            m_yr = ry + rx


        # 出力調整
        m_xr = motor_adjustment(m_xr)
        m_xl = motor_adjustment(m_xl)

        m_yr = motor_adjustment(m_yr)
        m_yl = motor_adjustment(m_yl)

        dc_xr(-m_xr)
        dc_xl(m_xl)

        dc_yr(-m_yr)
        dc_yl(m_yl)

        # ela_time = time.time() - start_time
        # print ela_time
        # if ela_time >= set_time:
        #     stop()
        #     break


def motor_adjustment(val):
    in_min = -100
    in_max = 100
    out_min = -50
    out_max = 50
    val = (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return int(val)

# -------------------------------------------------------------------

def t10j_mode_sumo():
    t10j_start_check()
    while True:

        t10j_map = t10j_map_data()
        print(t10j_map)

        ly = t10j_map["ly"]
        lx = t10j_map["lx"]
        ry = t10j_map["ry"]
        rx = t10j_map["rx"]



        # モータ出力
        if ly >= 30:
            ly = 30
        if ry >= 30:
            ry = 30

        dc_xr(-ry)
        dc_xl(ly)

        if lx >= 1:
            up_down(50)
        elif lx <= -1:
            up_down(-50)
        if lx == 0:
            up_down(0)



    # return 0


# -------------------------------------------------------------------

def t10j_time(set_time=10):
    # ジョイスティックの位置を正す
    t10j_start_check()
    # カウントダウン
    for cnt in range(3, 0, -1):
        # led_red()
        print(cnt)
        time.sleep(0.5)
        # led_off()
        time.sleep(0.5)

    start_time = time.time()
    while True:

        t10j_map = t10j_map_data()

        up_down(t10j_map["ry"])
        if t10j_map["lx"] == 0:
            go_back(t10j_map["ly"])
        else:
            spinturn(t10j_map["lx"])

        ela_time = time.time() - start_time
        print(ela_time)
        if ela_time >= set_time:
            stop()
            break


# -------------------------------------------------------------------

if __name__ == '__main__':
    try:
        ini_val = get_data("yaw")
        # センサー初期化
        # send_data("reboot")
        while True:
            t10j(set_time=10)
        stop()

    except KeyboardInterrupt as e:
        stop() #Ctrl + Cを押したときの処理
