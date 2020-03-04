#coding: utf-8
import subprocess
from datetime import datetime


# 音声ファイルの作成、読み上げ
def jtalk(file_name="a", voice="a"):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']

    speed=['-r','1.0']
    outwav=['-ow','/kaiyo/voice/'+file_name+'.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(voice)
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','/kaiyo/voice/'+file_name+'.wav']
    wr = subprocess.Popen(aplay)


# 現在時刻の読み上げ
def say_datetime():
    d = datetime.now()
    text = '%s月%s日、%s時%s分%s秒' % (d.month, d.day, d.hour, d.minute, d.second)
    # text = "こんにちは"
    print(text)
    jtalk(text)


# 渡されたfile_nameを読み上げるだけ
def jtalk_say(file_name="okinawa"):
    aplay = ['aplay','-q','/kaiyo/voice/'+file_name+'.wav']
    wr = subprocess.Popen(aplay)


if __name__ == '__main__':
    # say_datetime()
    # jtalk("ちぶるまぎーモデルジーがスタートします。機体から離れて下さい")
    # jtalk(file_name="goal", voice="ちぶるまぎーモデルジーはゴールしました。ダイバーさん機体を回収してください")
    jtalk(file_name="a", voice="aaaaaabbbbbb")
    # say("status")
    # jtalk()
