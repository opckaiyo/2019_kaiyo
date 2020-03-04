# coding: utf-8

import RPi.GPIO as GPIO
import time

# -----------------------------------------------------------------------------

# BCMで設定
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)


# 00光らない
# 01赤
# 10緑
# 11白
def led_mode(a=1, b=1, c=1):
    GPIO.output(23, a)
    GPIO.output(24, b)
    GPIO.output(25, c)

def led_off():
    # print "OFF!!"
    led_mode(0, 0, 0)

def led_blue():
    # print "RED!!"
    led_mode(0, 0, 1)

def led_red():
    # print "GREEN!!"
    led_mode(0, 1, 0)

def led_purple():
    # print "WHITE!!"
    led_mode(0, 1, 1)

def led_green():
    # print "WHITE!!"
    led_mode(1, 0, 0)

def led_lihtblue():
    # print "WHITE!!"
    led_mode(1, 0, 1)

def led_yellow():
    # print "WHITE!!"
    led_mode(1, 1, 0)

def led_white():
    # print "WHITE!!"
    led_mode(1, 1, 1)


if __name__ == '__main__':
    a = 1
    while True:
        # 黄：赤：青
        # led_mode(0, 0, 0)
        led_white()
        print ("000")
        led_mode(0,0,0)
        time.sleep(a)

        print ("001")
        led_mode(0,0,1)
        time.sleep(a)

        print ("010")
        led_mode(0,1,0)
        time.sleep(a)

        print ("011")
        led_mode(0,1,1)
        time.sleep(a)

        print ("100")
        led_mode(1,0,0)
        time.sleep(a)

        print ("101")
        led_mode(1,0,1)
        time.sleep(a)

        print ("110")
        led_mode(1,1,0)
        time.sleep(a)

        print ("111")
        led_mode(1,1,1)
        time.sleep(a)


        # 000 薄い青
        # 001 薄い青
        # 010 赤
        # 011 赤
        # 100 緑
        # 101 緑
        # 110 黄色
        # 111 黄色
