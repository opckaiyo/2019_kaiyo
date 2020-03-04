#!/usr/bin/env python
# -*- coding:utf-8 -*-

import multiprocessing
import cv2.cv as cv
import time

class camera2(multiprocessing.Process):

    capture = cv.CaptureFromCAM(1)

    # 画像サイズの指定
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,680)
    # cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,1200)
    # cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,480)
    # a = 0
    # i = 0
    # while True:
    #     if a == 0:
    #         img = cv.QueryFrame(capture)
    #         cv.ShowImage("camera", img)
    #         if cv.WaitKey(10) > 0:
    #             sbreak

    while True:
        img = cv.QueryFrame(capture)
        cv.ShowImage("camera", img)
        if cv.WaitKey(10) > 0:
            break

    cv.DestroyAllWindows()
