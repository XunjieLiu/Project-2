from socket import *
from multiprocessing import Process

'''
1. 读取第一个node, 并建立单独的文件，存储路由表
2. 路由表该咋存储呢
3. 不同进程之间交换路由表
4. 通过Socket进行通信
5. 规定：node数字 +１０００为端口号
6. 规定：node数字小的向数字大的发起通信
7. 规定：一旦某个节点的路由表得到更新，广播其新的路由表
8. 规定：网络中没有路由表更新，停止程序
'''



'''
test = open('graphTest.txt', 'r')
test2 = open('nodeExample.txt', 'r')

print(test2.readlines())

print(get_graph('graphTest.txt'))
'''