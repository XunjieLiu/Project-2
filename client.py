from socket import *

serverNme = '127.0.0.0'
serverPort = 10005

# AF_INET表示ipv4网络， SOCK_STREAM表示TCP协议
clientSocket = socket(AF_INET, SOCK_STREAM)
# 这一行是与UDP协议不一样的地方，UDP协议直接调用sendto方法发送报文，但是TCP协议需要先进行连接
clientSocket.connect((serverNme, serverPort))

