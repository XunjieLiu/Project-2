from socket import *
from multiprocessing import Process
from multiprocessing import Pool
from copy import *
import json, struct, pickle
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
        self.port = 10000 + int(node)

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

def run_process(router):
    neighbors = router.get_neighbors()

    port = router.get_port()
    mySocket = socket(AF_INET, SOCK_STREAM)
    mySocket.bind(('', port))
    mySocket.listen()

    print("Start listening")

    while True:
        connectionSocket, addr = mySocket.accept()

        # 使用pickle发送数据 第一步 接收数据
        data = connectionSocket.recv(4096) # [table, name]
        reply = pickle.loads(data)
        print("I got data! ", reply)
        neighbors.remove(reply[1]) # 当neighbor是空的时候停止循环

        # 第二步 发送数据 以完成双向连接的目的
        msg = [router.get_routing_table(), router.get_name()]
        packedData = pickle.dumps(msg)
        connectionSocket.sendall(packedData)

if __name__ == '__main__':
    Nodes = []
    graph = get_graph('graphTest.txt')
    for key, value in graph.items():
        new_node = Router(key, value, get_blank_table(graph))
        new_node.init_routing_table()
        Nodes.append(new_node)

    print(Nodes[0].get_neighbors())

    '''
    print('Child process will start.')

    pool = Pool(len(Nodes))
    pool.map(run_process, Nodes)
    pool.close()
    pool.join()
    
    print('Child process end.')
    '''

    '''
    print(Nodes[0].get_name())
    print_dict(Nodes[0].get_routing_table())
    Nodes[0].relax(Nodes[1].get_routing_table(), Nodes[1].get_name())

    print_dict(Nodes[0].get_routing_table())
    '''
    
    # init(graph)
    '''
    with open('A.json', 'r') as f:
        A = json.load(f)

    with open('B.json', 'r') as f:
        B = json.load(f)

    with open('C.json', 'r') as f:
        C = json.load(f)

    with open('D.json', 'r') as f:
        D = json.load(f)

    print(relax(A, B, 'A', 'B'))
    relax(A, C, 'A', 'C')
    relax(A, D, 'A', 'D')
    print(relax(A, D, 'A', 'D'))

    print_dict(A)
    '''