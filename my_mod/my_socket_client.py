# クライアントを作成

import socket
import pickle
import time

from my_gamepad import get_pad_data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # サーバを指定
    s.connect(('172.21.25.160', 50007))
    # s.connect(('127.0.0.1', 50007))

    while True:

        data = get_pad_data()
        # test_data = "test"
        # data = pickle.dumps(data)
        # print(data)

        # サーバにメッセージを送る
        s.sendall(pickle.dumps(data))
        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        com_check = s.recv(1024)
        # print (com_check)

        # 終了
        if com_check == b'END' :
            break
        # 受信確認
        while com_check != b'OK' :
            pass
        com_check = ''

        print(repr(data))
        time.sleep(0.1)

    print( "終了しました。")
