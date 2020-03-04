#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import gps
import ast
import time

# -------------------------------------------------------------------

# GPSのデータを取得して還す
def get_gps_data():
    session = gps.gps("localhost", "2947")
    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    lat = ""
    lon = ""
    alt = ""
    while True:
        try:

            # gps データ取得
            report = next(session)
            # print(report)
            # print report # To see all report data, uncomment the line below
            if report['class'] == 'TPV':
                if hasattr(report, 'lat'):
                    lat = float(report.lat)
                if hasattr(report, 'lon'):
                    lon = float(report.lon)
                if hasattr(report, 'alt'):
                    alt = float(report.alt)
                if( lat!=""and lon!="" and alt!="" ):
                    gps_data_dict = {"lat":lat, "lng":lon, "alt":alt}
                    # str に変換
                    gps_data_dict["datetime"] = str(datetime.now())
                    # print gps_data_dict
                    return gps_data_dict
        except KeyError:
                pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print("GPSD has terminated!!")


# GPSのデータをテキストファイルに保存
def gps_data_logging():
    # log ファイル生成
    gps_log_file_time = open('/kaiyo/log/gps_log/gps_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt', 'a')
    gps_log_file = open('/kaiyo/log/gps_log/gps_log.txt', 'w')

    session = gps.gps("localhost", "2947")

    session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
    lat = ""
    lon = ""
    alt = ""

    while True:
        try:
            # print("hello!!!!!!")
            # gps データ取得
            report = next(session)
            # print report # To see all report data, uncomment the line below
            if report['class'] == 'TPV':
                if hasattr(report, 'lat'):
                    lat = float(report.lat)
                if hasattr(report, 'lon'):
                    lon = float(report.lon)
                if hasattr(report, 'alt'):
                    alt = float(report.alt)
                if( lat!=""and lon!="" and alt!="" ):
                    # 2秒間待つ
                    time.sleep(2)

                    gps_data_dict = {"lat":lat, "lng":lon, "alt":alt}
                    # str に変換
                    gps_data_dict["datetime"] = str(datetime.now())
                    # log に書き込み
                    gps_log_file_time.writelines(str(gps_data_dict) + "\n")
                    gps_log_file.writelines(str(gps_data_dict) + "\n")

                    print(gps_data_dict)
                    # return gps_data_dict
        except KeyError:
                pass
        except KeyboardInterrupt:
            quit()
        except StopIteration:
            session = None
            print("GPSD has terminated!!")


# gps と sensor を結合
def gps_sensor_join_data():
    # ファイルのパスを指定
    gps_log_file = "/kaiyo/log/gps_log/gps_log.txt"
    sensor_log_file = "/kaiyo/log/sensor_log/sensor_log.txt"
    join_log_file_time = '/kaiyo/log/join_log/join_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt'
    join_log_file = '/kaiyo/log/join_log/join_log.txt'

    # ファイルを開く
    gps_log_file = open(gps_log_file, 'r')
    sensor_log_file = open(sensor_log_file, 'r')
    join_log_file_time = open(join_log_file_time, 'w')
    join_log_file = open(join_log_file, 'w')

    try:
        # 1行読み込み
        gps_log_data = gps_log_file.readline()
        # str から dictに変換
        gps_log_data = ast.literal_eval(gps_log_data)
        # str から datetime に変換
        gps_log_data["datetime"] = datetime.strptime(gps_log_data["datetime"], '%Y-%m-%d %H:%M:%S.%f')
        while True:
            # 1行読み込み
            sensor_log_data = sensor_log_file.readline()
            # str から dictに変換
            sensor_log_data = ast.literal_eval(sensor_log_data)
            # str から datetime に変換
            sensor_log_data["datetime"] = datetime.strptime(sensor_log_data["datetime"], '%Y-%m-%d %H:%M:%S.%f')

            # dict 生成
            join_log_data = sensor_log_data

            if gps_log_data["datetime"] > sensor_log_data["datetime"]:
                # dict から str に変換
                join_log_data["datetime"] = str(join_log_data["datetime"])

                # GPS のデータを追加
                join_log_data["lat"] = float(gps_log_data["lat"])
                join_log_data["lng"] = float(gps_log_data["lng"])
                join_log_data["alt"] = float(gps_log_data["alt"])
                # テキストに書き込み
                join_log_file_time.writelines(str(join_log_data) + "\n")
                join_log_file.writelines(str(join_log_data) + "\n")
            else:
                # 1行読み込み
                gps_log_data = gps_log_file.readline()
                # str から dictに変換
                gps_log_data = ast.literal_eval(gps_log_data)
                # str から datetime に変換
                gps_log_data["datetime"] = datetime.strptime(gps_log_data["datetime"], '%Y-%m-%d %H:%M:%S.%f')

                # dict から str に変換
                join_log_data["datetime"] = str(join_log_data["datetime"])

                # GPS のデータを追加
                join_log_data["lat"] = float(gps_log_data["lat"])
                join_log_data["lng"] = float(gps_log_data["lng"])
                join_log_data["alt"] = float(gps_log_data["alt"])
                # テキストに書き込み
                join_log_file.writelines(str(join_log_data) + "\n")
                join_log_file_time.writelines(str(join_log_data) + "\n")

            # print join_log_data
    except Exception as e:
        # ファイルを閉じる
        gps_log_file.close()
        sensor_log_file.close()
        join_log_file.close()
        print("gps_sensor_join_data Creation complete!!")


# -------------------------------------------------------------------


if __name__ == '__main__':
    print("保存はCtrl-C")
    # gps_sensor_join_data()
    # while(1):
          #print(get_gps_data())
    gps_data_logging()
