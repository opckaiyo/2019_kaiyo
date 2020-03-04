#coding: utf-8
import math
import time
import ast

import sys
sys.path.append("/kaiyo/my_mod")
from my_gps import get_gps_data
from my_balance import yaw, go_yaw_time, go_yaw_rot, diving, diving_while, go_yaw_onoff, go_yaw_onoff_iki, go_yaw_onoff_kaeri, yaw_rot, compass, go_compass_onoff
from my_check import operation_check, battery_check, my_exit, first_action
from my_motor import go_back, up_down, spinturn, roll, stop, stop_go_back, stop_up_down, go_back_each, up_down_each, spinturn_each
from my_gamepad import get_pad_data
from my_gpio import led_red, led_green, led_yellow, led_off, led_blue, led_purple, led_lihtblue


# -----------------------------------------------------------------------------

# pgsで現在地を取得して目標地点までの角度と距離を計算
def get_direction_distance(goal_lat, goal_lng):
    # gpsで現在地を取得
    now_gps_data = get_gps_data()
    now_lat = now_gps_data["lat"]
    now_lng = now_gps_data["lng"]

    print("now_lat  :", now_lat)
    print("now_lng  :", now_lng)
    print("goal_lat :", goal_lat)
    print("goal_lng :", goal_lng)

    lat_length = goal_lat - now_lat
    lng_length = goal_lng - now_lng

    # 方位を計算
    direction = math.atan2(lat_length, lng_length) / 0.01745329
    direction -= 90
    if direction < -180:
        direction += 360

    # 距離を計算
    lat_distance = lat_length * 111263.283
    lng_distance = lng_length * 111263.283
    distance = math.sqrt((lng_distance * lng_distance) + (lat_distance * lat_distance))

    # 回転数を計算（30回転で1m）
    set_rot = int(distance * 30)

    goal_gps_data = {"direction":int(direction), "distance":int(distance), "set_rot":set_rot}
    print(goal_gps_data)

    return goal_gps_data


# def waypoint(waypoint_data):
#     # up_down(40)
#     for route_number, lat_lng_data in waypoint_data.items():
#         print "-"*60
#         print "route_number :", route_number
#         print "lat :", lat_lng_data["lat"]
#         print "lng :", lat_lng_data["lng"]
#
#         goal_lat = lat_lng_data["lat"]
#         goal_lng = lat_lng_data["lng"]
#
#         while True:
#             up_down(40)
#             # 目標地点までの角度と距離を取得
#             goal_gps_data = get_direction_distance(goal_lat=goal_lat, goal_lng=goal_lng)
#             # 目的地と現在地が直径1m以下なら次の目的地
#             if goal_gps_data["distance"] <= 1:
#                 print "Next waypoint!!"
#                 break
#             # 移動開始
#             else:
#                 print "Try waypoint!!"
#                 # その場で目標地点の角度(direction)を向く
#                 compass(set_angle=goal_gps_data["direction"], set_diving=False)
#                 # 目標地点まで角度を調整しながら前進
#                 # go_back(30)
#                 # time.sleep(3)
#                 go_compass_onoff(set_speed=30, set_angle=0, set_rot=goal_gps_data["set_rot"], set_diving=True)

# メカナム用
def waypoint(waypoint_data):
    for route_number, lat_lng_data in list(waypoint_data.items()):
        print("-"*60)
        print("route_number :", route_number)
        print("lat :", lat_lng_data["lat"])
        print("lng :", lat_lng_data["lng"])

        goal_lat = lat_lng_data["lat"]
        goal_lng = lat_lng_data["lng"]

        while True:
            # up_down(40)
            # 目標地点までの角度と距離を取得
            goal_gps_data = get_direction_distance(goal_lat=goal_lat, goal_lng=goal_lng)
            # 目的地と現在地が直径1m以下なら次の目的地
            if goal_gps_data["distance"] <= 1:
                for i in range(10):
                    led_purple()
                    time.sleep(0.1)
                    led_off()
                    time.sleep(0.1)
                print("Next waypoint!!")
                break
            # 移動開始
            else:
                print("Try waypoint!!")
                # その場で目標地点の角度(direction)を向く
                compass(set_angle=goal_gps_data["direction"], set_diving=False)
                # 目標地点まで角度を調整しながら前進
                # go_compass_onoff(set_speed=30, set_angle=0, set_rot=goal_gps_data["set_rot"], set_diving=True)
                go_compass_onoff(set_speed=30, set_angle=goal_gps_data["direction"], set_rot=30, set_diving=True)


# 経路作成
def pad_rc_route_data_creation():
    gps_route_data = open('/kaiyo/log/gsp_route_data/gps_route_data.txt', 'a')
    # gps_route_data = open('/kaiyo/log/gsp_route_data/gps_route_data.txt', 'w')
    up_down_val = 0
    while True:
        # padの状態を取得
        pad_data = get_pad_data()
        go_back_each(pad_data["joy_ly"], pad_data["joy_ry"])
        if pad_data["hat_y"]:
            time.sleep(0.1)
            if up_down_val < 100 and pad_data["hat_y"] == 1:
                up_down_val += 10
            if up_down_val > -100 and pad_data["hat_y"] == -1:
                up_down_val -= 10
            up_down(up_down_val)

        # gps 取得
        if pad_data["btn_a"] == 1:
            led_yellow()
            gps_data = get_gps_data()
            print(gps_data)
            gps_route_data.writelines(str(gps_data) + "\n")
            led_off()
        if pad_data["btn_x"] == 1:
            led_yellow()
            gps_route_data.close()
            print("pad_rc_route_data_creation END!!")
            test()
            return 0

def test():
    gps_route_data_file = open('/kaiyo/log/gsp_route_data/gps_route_data.txt', 'r')
    waypoint_route_data = {}
    cnt = 0
    while True:
        gps_route_data = gps_route_data_file.readline()
        if gps_route_data:
            gps_route_data = ast.literal_eval(gps_route_data)
            gps_route_data.pop("datetime")
            gps_route_data.pop("alt")
            waypoint_route_data[cnt] = gps_route_data
            cnt += 1
        else:
            print(waypoint_route_data)
            # 移動開始
            waypoint(waypoint_data = waypoint_route_data)
            break


# -------------------------------------------------------------------

if __name__ == '__main__':
    try:
        pad_rc_route_data_creation()
        # test()
        my_exit()
    except KeyboardInterrupt as e:
        my_exit()
