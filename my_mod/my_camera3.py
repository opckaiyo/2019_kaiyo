#coding: utf-8
import cv2
import numpy as np

cap1 = cv2.VideoCapture(0)
#cap2 = cv2.VideoCapture(2)
cap1.set(3,320) # WIDTH
cap1.set(4,240) # HEIGHT
cap1.set(5,1) # FPS
# cap2.set(3,320) # WIDTH
# cap2.set(4,240) # HEIGHT
# cap2.set(5,1) # FPS
def camera():
    while (True):
        ret, im1 = cap1.read()
        #ret, im2 = cap2.read()

        hsv = cv2.cvtColor(im1, cv2.COLOR_BGR2HSV)

        #オレンジ
        lower_blue = np.array([5,75,75])
        upper_blue = np.array([10,255,255])

        print (lower_blue)
        print (upper_blue)

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        res = cv2.bitwise_and(im1,im1, mask= mask)

        cv2.imshow('res',res)
        cv2.imshow('image1:f',im1)#sita
        # cv2.imshow('image2:b',im2)#mae
        if cv2.waitKey(1) != -1:
            break
        pass

    cap1.release()
    #cap2.release()
    cv2.destroyAllWindows()
