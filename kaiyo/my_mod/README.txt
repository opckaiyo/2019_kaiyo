
my_mod　ディレクトリは自作のモジュールである。


意味わからんくなったらここまでメールしてねー
opckaiyo@gmail.com


モジュール一覧


READMR.txt
my_modディレクトリの説明

my_analysis.py
収集したデータを分析する
データ数、最小値、最大値

my_get_serial
# ArduinoMegaとシリアル通信してセンサデータをもらう関数

my_motor
# PCA9685と通信しモータを制御する関数

my_balance
# 主にロボットの姿勢制御（方向、深度）を行う関数

my_rc
# プロポ（t19j）を使って、ロボットを制御するための関数

my_check
# プログラムスタート時にロボットの状態や初期設定の動作を行う関数

my_gpio
# 7色LEDの制御を行う関数

my_course
# 大会コースに沿った動作を行う関数。（主にこの関数の値を調整して大会挑んだ）

my_text_write
# プログラムがエラーを発生したときにエラーの内容をテキストファイルに記録する関数

my_gps
# GPSデータの取得や、GPSデータをテキストファイルに保存する関数

my_waypoint
# GPSによるウェイポイント制御を行う関数

my_gamepad
# 水中ロボット班から借りたゲームパッドでラジコン制御するとに使う関数

my_voice.py
スピーカーでテキストを読み上げるための関数


* .pyc とかいうファイルは何か知らないけど勝手にできる
