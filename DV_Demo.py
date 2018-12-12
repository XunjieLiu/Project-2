from socket import *
from multiprocessing import Process
from copy import *
import json

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

# 字典是可变对象 如果只新建一个字典对象 然后循环把这个字典传进函数里面，那么始终只有一个字典
def get_blank_table(graph):
	table = deepcopy(graph)
	for key, value in graph.items():
		table[key] = [key, 1000000, None] # 初始化（清空）

	return table

def init(graph):
	for key, value in graph.items():
		init_routing_table(key, value, get_blank_table(graph))

def init_routing_table(node, node_info, blank_table):
	for edge in node_info:
		neighbor = edge[0]
		cost = edge[1]

		blank_table[neighbor] = [cost, neighbor]

	blank_table[node] = [0, node]

	file_name = node + '.json'
	with open(file_name,"w") as f:
		json.dump(blank_table, f) # 存入JSON文件

if __name__ == '__main__':
	graph = read_file('graphTest.txt')
	init(graph)

	with open('A.json', 'r') as f:
		load_f = json.load(f)
		print(load_f)
