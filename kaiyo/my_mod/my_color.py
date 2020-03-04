#coding: utf-8
import cv2
import os
import numpy as np
import sys

sys.path.append("/kaiyo/my_mod")

def Coordinate_Align(frame,area_range,lower,upper):
    #高さ，幅，Cは使わない値
    h,w,c = frame.shape

    #hsv色空間に変換
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    #色を抽出する
    find_color = cv2.inRange(hsv,lower,upper)

    #輪郭検知
    _,contours,hierarchy = cv2.findContours(find_color,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #面積を計算
    areas_cal = np.array(list(map(cv2.contourArea,contours)))

    #見つからない場合
    if len(areas_cal) == 0 or np.max(areas_cal) / (h*w) < area_range:
        print("Area is small or not")
        return None
    #発見した場合
    else:
        print("Area discovery")
        max_idx = np.argmax(areas_cal)
        result = cv2.moments(contours[max_idx])
        x = int(result["m10"]/result["m00"])
        y = int(result["m01"]/result["m00"])
        return (x,y)


#色の範囲(lower,upper),対象物の大きさ(aera_renge)
def color_find_hsv(lower,upper,aera_renge):
    lower = np.array([lower, 50, 50])
    upper = np.array([upper, 255, 255])

    cap = cv2.VideoCapture(0)
    ret, img = cap.read()

    pos = Coordinate_Align(
        img,
        aera_renge,
        lower,
        upper
    )

    if pos is not None:
        cv2.circle(img,pos,10,(0,0,255),-1)

    cv2.imwrite('/kaiyo/camera/save_image/output.jpg',img)
    return pos

if __name__ == '__main__':
    x,y = color_find_hsv(5,15,0.005)
    print("x =",x,"y =",y)
    # pass
