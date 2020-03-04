# -*- coding: utf-8 -*-
import pygame
import time

import sys
# sys.path.append("/kaiyo/my_mod")
# from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each

# -----------------------------------------------------------------------------

pygame.init()

# Initialize the joysticks
#ジョイスティックを初期化
pygame.joystick.init()

# -------- Main Program Loop -----------
#while done==False:
def get_pad_data():
    # EVENT PROCESSING STEP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done=True

    joystick_count = pygame.joystick.get_count()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        name = joystick.get_name()

        axes = joystick.get_numaxes()

        joy_lx = map_axis(round(joystick.get_axis(0), 2))
        joy_ly = map_axis(round(joystick.get_axis(1), 2))
        # joy_lt = map_axis(round(joystick.get_axis(8), 2))
        joy_rx = map_axis(round(joystick.get_axis(2), 2))
        joy_ry = map_axis(round(joystick.get_axis(3), 2))
        # joy_rt = map_axis(round(joystick.get_axis(9), 2))

        # joy_ly = int((joy_ly - (-100)) * (30 - (-30)) / (100 - (-100)) + (-30))
        # joy_ry = int((joy_ry - (-100)) * (30 - (-30)) / (100 - (-100)) + (-30))

        # joy_ly = int((joy_ly - (-100)) * (50 - (-50)) / (100 - (-100)) + (-50))
        # joy_ry = int((joy_ry - (-100)) * (50 - (-50)) / (100 - (-100)) + (-50))

        joy_ly = -joy_ly
        joy_ry = -joy_ry
        # joy_lt = map_lt_rt(joy_lt)
        # joy_rt = map_lt_rt(joy_rt)

        hat_x = joystick.get_hat(0)[0]
        hat_y = joystick.get_hat(0)[1]

        btn1 = joystick.get_button(0)
        btn2 = joystick.get_button(1)
        btn3 = joystick.get_button(2)
        btn4 = joystick.get_button(3)
        btn5 = joystick.get_button(4)
        btn6 = joystick.get_button(5)
        btn7 = joystick.get_button(6)
        btn8 = joystick.get_button(7)
        btn9 = joystick.get_button(8)
        btn10 = joystick.get_button(9)
        btn11= joystick.get_button(10)

        btn_a = btn1
        btn_b = btn2
        btn_x = btn3
        btn_y = btn4
        btn_lb = btn5
        btn_rb = btn6
        btn_back = btn7
        btn_start = btn8
        btn_logicool = btn9
        btn_joyl = btn10
        btn_joyr = btn11

        pad_data = {"joy_lx":joy_lx, "joy_ly":joy_ly, "joy_rx":joy_rx, "joy_ry":joy_ry,\
                     "hat_x":hat_x, "hat_y":hat_y, \
                    "btn_a":btn_a, "btn_b":btn_b, "btn_x":btn_x, "btn_y":btn_y, \
                    "btn_lb":btn_lb, "btn_rb":btn_rb, "btn_back":btn_back, \
                    "btn_start":btn_start, "btn_logicool":btn_logicool, \
                    "btn_joyl":btn_joyl, "btn_joyr":btn_joyr}

        return pad_data


def pad_rc():
    up_down_val = 0
    while True:
        pad_data = get_pad_data()
        print (pad_data)
        # go_back_each(pad_data["joy_ly"], pad_data["joy_ry"])

        # if pad_data["joy_rt"]:
        #     up_down(pad_data["joy_rt"])
        # else:
        #     up_down(-pad_data["joy_lt"])

        if pad_data["hat_y"]:
            time.sleep(0.1)
            if up_down_val < 100 and pad_data["hat_y"] == 1:
                up_down_val += 10
            if up_down_val > -100 and pad_data["hat_y"] == -1:
                up_down_val -= 10



            # print (up_down_val)
            # up_down(up_down_val)

def map_axis(val):
    in_min = -1
    in_max = 1
    out_min = -100
    out_max = 100
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def map_lt_rt(val):
    if val <= 0 and val >= -100:
        in_min = -100
        in_max = 0
        out_min = 0
        out_max = 50
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    else:
        in_min = 0
        in_max = 100
        out_min = 50
        out_max = 100
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


if __name__ == '__main__':
    try:
        pad_rc()
    except KeyboardInterrupt as e:
        stop()
