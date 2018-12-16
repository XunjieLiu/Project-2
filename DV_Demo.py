from socket import *
from multiprocessing import Process
from multiprocessing import Pool
from threading import Lock
from copy import *
import json, struct, pickle, threading, time
from graphDemo import *

'''
1. 读取第一个node, 并建立单独的文件，存储路由表
2. 路由表该咋存储呢
3. 不同进程之间交换路由表
4. 通过Socket进行通信
5. 规定：node数字 +１０００为端口号
6. 规定：node数字小的向数字大的发起通信
7. 规定：一旦某个节点的路由表得到更新，广播其新的路由表
8. 规定：网络中没有路由表更新，停止程序


修正：
规定：一次循环是 每个Node向邻居交换表并更新（交换方式根据第六条规定）
循环Node - 1 次（根据Bellman-ford算法）
'''
def read_file(file):
    graphTxt = open(file, 'r')
    graph = dict() # {'1': [['2', 4], ['3', 2]], '2': [['3', 5]]}

    node = ''
    for line in graphTxt.readlines():
        if line.find('Node') >= 0:
            node = line.strip('\n').split(' ')[1]
            node = str(node)
            graph[node] = []
        else:
            line = line.strip('\n').split('\t') # ['Node', '1']
            line[1] = int(line[1]) # 表示这是权重值
            temp = graph[node]
            temp.append(line)
            graph[node] = temp

    return graph
'''
路由表：
Desti: [Cost, Next_Node]
'''
class Router(object):
    def __init__(self, node, node_info, blank_table):
        self.name = node
        self.info = node_info
        self.routing_table = blank_table
        self.port = 12000 + int(node)

    def write(self):
        file_name = self.name + '.json'
        with open(file_name,"w") as f:
            json.dump(self.routing_table, f) # 存入JSON文件

    def init_routing_table(self):
        for edge in self.info:
            neighbor = edge[0]
            cost = edge[1]

            self.routing_table[neighbor] = [cost, neighbor]

        self.routing_table[self.name] = [0, self.name]

        Router.write(self)

    def relax(self, routing_table, name):
        if_change = False
        keys = self.routing_table.keys()
        extra_cost = self.routing_table[name][0] # 中转延时

        for key in keys:
            if key == self.name or key == name:
                continue
            else:
                original_cost = self.routing_table[key][0]
                new_cost = extra_cost + routing_table[key][0] # relax过程
                if original_cost > new_cost:
                    if_change = True
                    self.routing_table[key][0] = new_cost
                    self.routing_table[key][1] = name

        Router.write(self) # 每次修改路由表 都重新写入文件
        return if_change

    def get_routing_table(self):
        return self.routing_table

    def get_name(self):
        return self.name

    def get_info(self):
        return self.info

    def get_port(self):
        return self.port

    def get_neighbors(self):
        neighbor = []

        for edge in self.info:
            neighbor.append(edge[0])

        return neighbor


    
# 字典是可变对象 如果只新建一个字典对象 然后循环把这个字典传进函数里面，那么始终只有一个字典
def get_blank_table(graph):
    table = deepcopy(graph)
    for key, value in graph.items():
        table[key] = [1000000, None] # 初始化（清空）

    return table

def print_dict(dictionary):
    for item in dictionary.items():
        print(item)

    print(" ")

def get_neighbor_port(neighbors):
    ports = []
    for node in neighbors:
        port = 10000 + int(node)
        ports.append(port)

    return ports

def listen(port):
    server_port = port
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', serverPort))
    server_socket.listen()

    print("Start listening port: ", port)


def run_process(router):
    tables = []
    lock = Lock()
    print("This is my neighbors")
    neighbors = router.get_neighbors()
    connect_to = [] # Node数字小的向大的连接
    connect_in = []
    for neighbor in neighbors:
        if int(neighbor) > int(router.get_name()):
            connect_to.append(neighbor)
        else:
            connect_in.append(neighbor)
    print(neighbors)

    '''
    Listener 负责监听 connect_in数组标记了理应发送过来连接的Node(数字比它小的)， 一旦此数组为空，则结束线程
    Messager 负责发送数据，connect_to数组标记了应该发送的Node（数字比他大的），一旦此数组为空，结束线程
    Listener在接收数据之后 立刻发送本身的路由表
    Messager在发送本身路由表之后 立刻接收对方路由表
    '''

    class Listener(threading.Thread):
        def __init__(self, port):
            threading.Thread.__init__(self)
            self.port = port

        def run(self):
            server_socket = socket(AF_INET, SOCK_STREAM)

            server_socket.bind(('', self.port))

            server_socket.listen()
            print("Start listening")

            while len(connect_in) > 0:
                connectionSocket, addr = server_socket.accept()

                # 使用pickle发送数据 第一步 接收数据
                data = pickle.loads(connectionSocket.recv(4096)) # [name, table] 接收到路由表
                tables.append(data)

                reply = [router.get_name(), router.get_routing_table()] # 发送自身路由表
                reply = pickle.dumps(reply)

                connectionSocket.sendall(reply)
                connect_in.remove(data[0]) # 理应的链接都收到了 就停止监听

            server_socket.close()


    class Messager(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

        def run(self):
            for node in connect_to:
                print("Node: ", node) # 规定只连接大的Node， 实现双向连接 
                new_socket = socket(AF_INET, SOCK_STREAM)
                server = '127.0.0.1'
                while True:      
                    try:
                        new_socket.connect((server, new_port))
                        print("Node %s success"%node)
                        msg = [router.get_name(), router.get_routing_table()] # 发送自身路由表
                        msg = pickle.dumps(msg)

                        new_socket.sendall(msg)

                        reply = pickle.loads(new_socket.recv(4096))
                        new_socket.close()
                        break
                    except Exception as e:
                        print("Connect failed")
                        time.sleep(2)

    print("Process %s start!"%router.get_name())

    listen_thread = Listener(router.get_port())
    messager_thread = Messager()

    listen_thread.start()
    messager_thread.start()

if __name__ == '__main__':
    Nodes = []
    graph = get_graph('graphTest.txt')
    for key, value in graph.items():
        new_node = Router(key, value, get_blank_table(graph))
        new_node.init_routing_table()
        Nodes.append(new_node)

    # print(Nodes[0].get_neighbors())

    test_router = Nodes[0]
    # print(test_router.get_port())

    for router in Nodes:
        process = Process(target=run_process, args=(router, ))
        process.start()
