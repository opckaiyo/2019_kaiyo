#!/usr/bin/env python
# -*- coding:utf-8 -*-
import multiprocessing
import cv2
import time
import numpy as np
import os

def set_camera():
    print("camera2 : start")
    cap = cv2.VideoCapture(0)

    # cap.set(3,1920) # WIDTH
    # cap.set(4,1280) # HEIGHT
    # cap.set(5,1) # FPS


    cap.set(3,640) # WIDTH
    cap.set(4,480) # HEIGHT
    cap.set(5,30) # FPS


    while(True):
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ret, hsv = cv2.threshold(hsv,100,255,cv2.THRESH_BINARY)
        cv2.imshow('frame',hsv)
        # 検出したい青色の範囲をHSVで指定
        # lower_blue = np.array([70, 50, 50])
        # upper_blue = np.array([150, 255, 255])

        # 青色のみ検出するマスク
        # 青色のところのみ白色（1）になる
        # mask = cv2.inRange(hsv, lower_blue, upper_blue)
        #
        # # オリジナル画像にマスクをかける
        # # 青色のところのみ通過してほかは真っ黒
        # res = cv2.bitwise_and(frame, frame, mask=mask)

        canny_img = cv2.Canny(frame, 200, 255)

        # cv2.imshow('hsv', hsv)
        cv2.imshow('frame', frame)
        #cv2.imshow('mask', mask)
        #cv2.imshow('res', res)
        # cv2.imshow('canny_img', canny_img)
        if cv2.waitKey(1) != -1:
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    print("start")
    set_camera()
