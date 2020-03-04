# -*- coding: utf-8 -*-
import ast
from time import sleep

import sys
sys.path.append("/kaiyo/my_mod")

#------------------------------------------------------------------------------


def get_log():
    print("start")
    path1 = "/kaiyo/log/sensor_log/20191009/0_depth_sensor_log_20191009_103541.txt"
    path2 = "/kaiyo/log/sensor_log/20191011/sensor_log_20191011_162000.txt"
    try:
        with open(path2) as f:
            # l_strip = [s.strip() for s in f.readlines()]
            # input_log_file_read = ast.literal_eval(l_strip[1])

            log_file = [s.strip() for s in f.readlines()]
            lf_len = len(log_file)
    except FileExistsError:
        print("file_error")
        pass

    out_log_file = open('/kaiyo/log/analysis.txt', 'w')

    for item in log_file:
        temp = ast.literal_eval(item)

        temp = dict(temp)
        # print(temp["depth"])
        out_log_file.write(str(temp["depth"]) + "\n")
        # print()
    print("end")

# ログがlistからdictになっているので使えない
# def get_log():
#     vals_min = {}
#     vals_max = {}
#     vals = {}
#     cnt = 0
#     print("Please file name :", end=' ')
#     file_name = input()
#
#     # file_name = "/kaiyo/log/log_181109_112516.txt"
#     file = open(file_name, 'r')
#     data = file.readline()
#     data = ast.literal_eval(data)
#
#     print("\n----------------------------")
#     print("File name :", file_name)
#     print("keys :", end=' ')
#     for key in list(data.keys()):
#         print(key, end=' ')
#         vals_min[key] = 0
#         vals_max[key] = 0
#     print("\n----------------------------\n")
#     file.close()
#     # sleep(2)
#     for key, val in list(vals_min.items()):
#         file = open(file_name, 'r')
#         a = -1000
#         while True:
#             try:
#                 data = file.readline()
#                 data = ast.literal_eval(data)
#
#                 vals[str(cnt)] = data[key]
#
#                 # 最大値を求める
#                 if a <= data[key]:
#                     a = data[key]
#
#                 cnt+=1
#             except Exception as e:
#                 print(key)
#                 print("----------------------------")
#                 print("MIN :", min(vals.values()))
#                 print("MAX :", max(vals.values()))
#                 print("----------------------------\n")
#
#                 vals_min[key] = min(vals.values())
#                 # vals_max[key] = max(vals.values())
#                 vals_max[key] = a
#                 file.close()
#                 break
#
#     print("ALL")
#     print("----------------------------")
#     print("Number of data :", cnt/len(vals_min))
#     # print "MIN :", vals_min
#     # print "MAX :", vals_max
#     print("----------------------------")
#     print("MIN")
#     for key, val in sorted(vals_min.items()):
#         print(key+"\t\t", val)
#     print("----------------------------")
#     print("MAX")
#     for key, val in sorted(vals_max.items()):
#         print(key+"\t\t", val)
#     print("----------------------------\n")

if __name__ == '__main__':
    # get_log("roll")
    get_log()
