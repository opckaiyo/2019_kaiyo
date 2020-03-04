# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue, Manager
from threading import Thread
import time
import sys

from my_get_serial import get_read_data, get_data, send_data

sys.path.append("/kaiyo/test/")

def f1():
    while True:
        data = "test1"
        print('f1です', data, '\n')
        # time.sleep(0.1)

def f2():
    while True:
        data = "test2"
        print('f2です', data, '\n')
        # time.sleep(0.5)

def f3():
    while True:
        data = g"test3"
        print('f3です', data, '\n')
        # time.sleep(1)


if __name__ == '__main__':
    send_data('reboot')
    # データを受信するスレッド
    # thread1 = Thread(target=get_read_data)
    # thread1.start()
    # d1 = Manager().dict()
    # d2 = Manager().dict()
    # d3 = Manager().dict()

    # p0 = Process(target=get_read_data, args=())

    p1 = Process(target=f1, args=())
    p2 = Process(target=f2, args=())
    p3 = Process(target=f3, args=())

    # p0.start()
    p1.start()
    p2.start()
    p3.start()
    while True:
        # pass
        try:
            pass
        except KeyboardInterrupt as e:
            # p1.join()
            # p2.join()
            # p3.join()
            pass

        #     print(q.get())    # prints "[42, None, 'hello']"
        # except Exception as e:
        #     print("れーがいー")
        #
        # time.sleep(0.1)
