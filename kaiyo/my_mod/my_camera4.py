#coding: utf-8
import cv2
import os
import numpy as np
import sys

#https://www.petitmonte.com/javascript/rgb_hsv_convert.html
lower = np.array([5, 50, 50])
upper = np.array([15, 255, 255])

# 抽出する目標の範囲
area_range = 0.005

#目標座標を出力する関数
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

def cap_main():
    cap = cv2.VideoCapture(0)

    cap.set(3,320) # WIDTH
    cap.set(4,240) # HEIGHT
    cap.set(5,1) # FPS

    #カメラが見つからないとき
    if cap.isOpened() is False:
        print("no camera")
        sys.exit()

    while True:
        ret,frame = cap.read()
        #cap.read()がエラーしたとき
        if ret is False:
            print("no read image")
            continue

        # 指定した色の座標取得
        pos = Coordinate_Align(frame,area_range,lower,upper)

        #座標表示
        print (pos)

        #posの値がNoneじゃない場合
        if pos is not None:
            #中心に点をおく
            cv2.circle(frame,pos,1,(0,0,255),-1)
            #http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html

        #画面出力
        cv2.imshow('frame',frame)

        #キー入力待ち
        if cv2.waitKey(1) != -1:
            break

    #キャプチャ解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print("start camera")
    cap_main()
