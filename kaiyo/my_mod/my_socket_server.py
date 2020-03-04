# socket サーバを作成

import socket
import pickle

def socket_server(pad_data,is_stop):
    # AF = IPv4 という意味
    # TCP/IP の場合は、SOCK_STREAM を使う
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # IPアドレスとポートを指定
        s.bind(('0.0.0.0', 50007))
        # 1 接続
        s.listen(1)

        # connection するまで待つ
        while True:
            # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
            conn, addr = s.accept()
            with conn:
                while True:
                    # データを受け取る
                    data = pickle.loads(conn.recv(1024))

                    if not data:
                        break
                    # print('data : {}, addr: {}'.format(data, addr))

                    for i in data:
                        pad_data[i] = data[i]
                    
                    # print("my : ",pad_data)

                    if (is_stop):
                        break
                    # 受信完了通知　クライアントにデータを返す(b -> byte でないといけない)
                    conn.sendall(b'OK')
            break
        print("終了")

if __name__ == '__main__':
    print("start")
    is_stop = 0
    pad_data = {"joy_lx":0, "joy_ly":0, "joy_rx":0, "joy_ry":0,\
                "hat_x":0, "hat_y":0, \
                "btn_a":0, "btn_b":0, "btn_x":0, "btn_y":0, \
                "btn_lb":0, "btn_rb":0, "btn_back":0, \
                "btn_start":0, "btn_logicool":0, \
                "btn_joyl":0, "btn_joyr":0}
    socket_server(pad_data,is_stop)
