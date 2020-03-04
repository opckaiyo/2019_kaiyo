from multiprocessing import Manager, Process
# import readchar
import time
from datetime import datetime
import sys
import os
sys.path.append("/kaiyo/test")

from char_test import move_test


if __name__ == "__main__":
    try:
        with Manager() as manager:
            #センサーのdata
            data = manager.dict()
            #my_blanceの操作量
            MV = manager.Value("d", 0.0)
            #my_blanceの目標値
            goal_yaw = manager.Value("i", 0)

            process1 = Process(target=move_test, args=[])

            process1.start()

            # while True:
            #     pass

        process1.join()
        # process2.join()
    except Exception as e:
        print("\n------")
        print("main.py : ",e)
        print("------\n")

    print("end")
    exit()
