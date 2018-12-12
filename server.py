from socket import *
import time
from time import ctime
import threading

host=''
port=10005
buffsize=1024
address = (host, port)

mySocket = socket(AF_INET,SOCK_STREAM)
mySocket.bind(address)
mySocket.listen(1)

socks=[] # 放每个客户端的socket

def handle():
    while True:
        for s in socks:
            try:
                data = s.recv(BUFSIZ)     #到这里程序继续向下执行
            except Exception as e:        
                continue
            if not data:
                socks.remove(s)
                continue
            s.send('[%s],%s' % (ctime(), data)) 

'''
主线程循环监听 子线程（一个）循环接收数据
'''
t = threading.Thread(target=handle)             #子线程

if __name__ == '__main__':
    t.start()
    print(u'我在%s线程中 ' % threading.current_thread().name)
    print('waiting for connecting...')

    while True:
        client, addr = mySocket.accept()
        print('connected from:', addr)
        client.setblocking(0) # 阻塞模式
        socks.append(client)