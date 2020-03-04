
import readchar
import time
from datetime import datetime
import sys
import os

def move_test():
    val = 30

    try:
        os.makedirs('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d')))
    except FileExistsError:
        pass
    input_log_file_time = open('/kaiyo/log/input_log/'+str(datetime.now().strftime('%Y%m%d'))+'/input_log_'+str(datetime.now().strftime('%Y%m%d_%H%M%S'))+'.txt', 'a')

    while True:
        try:
            # print ("input please:")
            # if(readchar.readchar() != null):
            kb = readchar.readchar()
            # print(kb)
            # print(type(kb))
            kb = kb.decode()
            print(kb)

            if kb == 'p':   #終了
                # my_exit()
                print("終了:「ctrl + c」 押してね joinlog")
                input_log_file_time.write("time:" + str(datetime.now().strftime('%H:%M:%S')) + " inputkey:" + str(kb) + " moterval:" + str(val) + "\n")
                break

        except KeyboardInterrupt as e:
            stop()
            break

if __name__ == '__main__':
    while True:
        t1 = time.time()
        try:
            move_test()
            stop()
            break
            # go_back(50)
            # up_down(20)
            # go_back_each(10,10,0)
            # dc_u( 100 )
        except KeyboardInterrupt as e:
            stop()
            break
