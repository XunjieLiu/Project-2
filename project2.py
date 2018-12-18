from heapq import *
from copy import *
from socket import *
from copy import *
from multiprocessing import Process
from multiprocessing import Pool
from threading import Lock
import json, struct, pickle, threading, time, sys

def get_graph(file):
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
    # 补全
    temp = deepcopy(graph) # python是引用传递，直接用等号不管用
    for key, value in temp.items():
        for edge in value:
            if edge[0] not in graph: # 如果graph没有，说明这是首次判断，添加空的进去
                graph[edge[0]] = [] # 在下次if中添加值

            if edge[0] not in temp: # 如果temp没有，说明这个edge是新的，但是在上一个if里面已经初始化了
                newEdge = [key, edge[1]] 
                tempNode = graph[edge[0]]
                tempNode.append(newEdge)
                graph[edge[0]] = tempNode

    # 由于这连通的双向图 所以可能有的节点没有标全，比如Node1标明连接Node2, 但是在Node2里面并没有标明
    temp = deepcopy(graph)
    for key, value in temp.items():
        for edge in value:
            linked_node = edge[0]
            linked_node_edges = graph[linked_node]
            newEdge = [key, edge[1]]
            if newEdge not in linked_node_edges:
                graph[linked_node].append(newEdge)

    return graph

def takeFirst(elem): # 用于list排序
    return elem[0]

def dijkstra(graph, source='1'):
    distance = dict()
    previous = dict()
    distance[source] = 0
    heap = [] # 最小堆
    keys = []

    for i in graph.keys():
        heappush(keys, i)

    for key in keys:
        if key != source:
            distance[key] = 10000000
            previous[key] = None
        heappush(heap, [distance[key], key]) 

    while len(heap) > 0:
        u = heappop(heap) # u = [dist[key], key]

        nodes = graph[u[1]] # graph = {'Node1': [['2', 4], ['3', 2]], 'Node2': [['3', 5]]}
        # nodes = [['2', 4], ['3', 2]]
        for neighbor in nodes: # neighbor = ['3', 2] for each neighbor v of u
            alt = distance[u[1]] + neighbor[1] # alt := dist[u] + length(u, v), 这里是计算source到V的距离
            if alt < distance[neighbor[0]]:
                # 算法里面distance是一个优先队列，但字典没法实现这一点
                # 所以每次修改一次值，相对应的heap里面的值就要修改一次
                oldItem = [distance[neighbor[0]], neighbor[0]]
                distance[neighbor[0]] = alt
                previous[neighbor[0]] = u[1]
                newItem = [alt, neighbor[0]] # [value, key]
                heap.remove(oldItem)
                heappush(heap, newItem)
            heap.sort(key=takeFirst) #以防万一　再排序一次

    return distance, previous

def get_route(destination, previous, source='1'):
    route = ''
    next_node = destination
    nodes = []
    while next_node != source:
        next_node = previous[next_node]
        nodes.append(next_node)

    nodes = nodes[::-1]

    for node in nodes:
        route+=(node + '->')

    route += destination

    return route

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

    def read(self):
        file_name = self.name + '.json'
        with open(file_name,"r") as f:
            self.routing_table = json.load(f)

    def init_routing_table(self):
        for edge in self.info:
            neighbor = edge[0]
            cost = edge[1]

            self.routing_table[neighbor] = [cost, neighbor]

        self.routing_table[self.name] = [0, self.name]

        Router.write(self)

    def relax(self, routing_table, name):
        Router.read(self) # 更新
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
        Router.read(self)
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

def get_neighbor_port(neighbors):
    ports = []
    for node in neighbors:
        port = 10000 + int(node)
        ports.append(port)

    return ports

def run_process(router):
    tables = []
    lock = Lock()
    neighbors = router.get_neighbors()
    connect_to = [] # Node数字小的向大的连接
    connect_in = []
    for neighbor in neighbors:
        if int(neighbor) > int(router.get_name()):
            connect_to.append(neighbor)
        else:
            connect_in.append(neighbor)

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
                # print("Node: ", node) # 规定只连接大的Node， 实现双向连接 
                new_socket = socket(AF_INET, SOCK_STREAM)
                server = '127.0.0.1'
                while True:      
                    try:
                        new_port = 12000 + int(node)
                        new_socket.connect((server, new_port))
                        print("Node %s success"%node)
                        msg = [router.get_name(), router.get_routing_table()] # 发送自身路由表
                        msg = pickle.dumps(msg)

                        new_socket.sendall(msg)

                        reply = pickle.loads(new_socket.recv(4096))
                        tables.append(reply)
                        new_socket.close()
                        break
                    except Exception as e:
                        print("Waiting to reconnect")
                        time.sleep(2)

    print("Process %s start!"%router.get_name())

    listen_thread = Listener(router.get_port())
    messager_thread = Messager()

    listen_thread.start()
    listen_thread.join()
    messager_thread.start()
    messager_thread.join()

    for table in tables:
        name = table[0]
        routing_table = table[1]
        if_change = router.relax(routing_table, name)

def main_process(Nodes):
    for router in Nodes:
        process = Process(target=run_process, args=(router, ))
        process.start()

def main_2(fileName):
    print("-------------------------Part 2 Start------------------------------")
    Nodes = []
    graph = get_graph(fileName)
    print("Initializing.......")
    for key, value in graph.items():
        new_node = Router(key, value, get_blank_table(graph))
        new_node.init_routing_table()
        Nodes.append(new_node)

    for i in range(len(Nodes) - 1):
        print("---------------Round %d------------------"%(i+1))
        p = Process(target=main_process, args=(Nodes, ))
        p.start()
        p.join()

    print("-------------------------Part 2 End------------------------------")


def main_1(fileName):
    print("\n\n-------------------------Part 1 Start------------------------------")
    graph = get_graph(fileName)
    dist, previous = dijkstra(graph)

    route_map = dict()

    for node in graph.keys():
        if node == '1':
            continue
        else:
            route = get_route(node, previous)
            cost = dist[node]

            print("From 1, To %s, Path: %s, Minimum Cost: %d"%(node, route, cost))

            route_map[node] = [route, cost]

    print("\nRead route information into JSON file, with name as 'Route_Map.json'\n")

    file_name = 'Route_Map.json'

    with open(file_name, 'w') as f:
        json.dump(route_map, f)
    print("-------------------------Part 1 End------------------------------\n\n\n")

if __name__ == '__main__':
    file_name = sys.argv[1] 
    main_1(file_name) # program for question 1 and question 2

    main_2(file_name) # program for question 2