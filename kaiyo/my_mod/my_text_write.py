# coding:utf8
from datetime import datetime

# エラーログは日付ごとに生成される
def error_log_write(state):
    file = open('/kaiyo/log/error_log/state_log'+str(datetime.now().strftime('%Y%m%d'))+'.txt', 'a')
    file.writelines(str(state) + " : " + str(datetime.now()) + "\n")
    file.close()



if __name__ == '__main__':
    state_write("浮上")
