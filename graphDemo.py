from heapq import *
from copy import *

def get_graph():
	graphTxt = open('graph.txt', 'r')
	graph = dict() # {'1': [['2', 4], ['3', 2]], '2': [['3', 5]]}
	# 真傻逼 给图也特么不给全 还得自己去创造节点

	node = ''
	for line in graphTxt.readlines():
		line = line.strip('\n').split(' ') # ['Node', '1']

		if line[0] == 'Node':
			node = str(line[1]) # 新的Node
			graph[node] = []
		else:
			line[1] = int(line[1]) # 表示这是权重值
			# 很傻逼 为什么Node的名字非得是数字而不能是字母呢
			# 对不起 我错了
			temp = graph[node]
			temp.append(line)
			graph[node] = temp


	'''
	老师给的文件里面，格式是 Node：[LinkedNode1, value], [LinkedNode2, value]
	但特么，有些Node, 他只在LinkedNode提到了，压根就没声明，所以我特么还得自己去把这个图写完整
	你比如{'1': [['2', 4], ['3', 2]], '2': [['3', 5]]}， 这里面有三个节点（1 2 3）
	但你看看，他就声明了俩，你说操蛋不
	'''

	# 补全
	temp = deepcopy(graph) # python是引用传递，直接用等号不管用 傻逼python 我爱Java
	for key, value in temp.items():
		for edge in value:
			if edge[0] not in graph: # 如果graph没有，说明这是首次判断，添加空的进去
				graph[edge[0]] = [] # 在下次if中添加值

			if edge[0] not in temp: # 如果temp没有，说明这个edge是新的，但是在上一个if里面已经初始化了
				newEdge = [key, edge[1]] # 我不敢保证我一个月后回来 能不能看懂这段代码
				tempNode = graph[node]
				tempNode.append(newEdge)
				graph[edge[0]] = tempNode

	return graph

graph = get_graph()

def dijkstra(graph, source='1'):
	distance = dict()
	previous = dict()
	distance[source] = 0
	heap = [] # 最小堆
	print(graph.keys())

	for key in graph.keys():
		if key != source:
			distance[key] = 10000000
			previous[key] = None
		heappush(heap, [distance[key], key])
	print(heap)

	while len(heap) > 0:
		u = heappop(heap) # u = [dist[key], key]

		nodes = graph[u[1]] # graph = {'Node1': [['2', 4], ['3', 2]], 'Node2': [['3', 5]]}
		# nodes = [['2', 4], ['3', 2]]
		for neighbor in nodes: # neighbor = ['3', 2] for each neighbor v of u
			alt = distance[u[1]] + neighbor[1] # alt := dist[u] + length(u, v), 这里是计算source到V的距离
			if alt < distance[neighbor[0]]:
				distance[neighbor[0]] = alt
				previous[neighbor[0]] = u[1]

	return distance, previous

dist, previous = dijkstra(graph)
print(dist)
print(previous)

'''
 1  function Dijkstra(Graph, source):
 2      dist[source]  := 0                     // Distance from source to source
 3      for each vertex v in Graph:            // Initializations
 4          if v ≠ source
 5              dist[v]  := infinity           // Unknown distance function from source to v
 6              previous[v]  := undefined      // Previous node in optimal path from source
 7          end if 
 8          add v to Q                         // All nodes initially in Q (unvisited nodes)
 9      end for
10      
11      while Q is not empty:                  // The main loop
12          u := vertex in Q with min dist[u]  // Source node in first case
13          remove u from Q 
14          
15          for each neighbor v of u:           // where v has not yet been removed from Q.
16              alt := dist[u] + length(u, v)
17              if alt < dist[v]:               // A shorter path to v has been found
18                  dist[v]  := alt 
19                  previous[v]  := u 
20              end if
21          end for
22      end while
23      return dist[], previous[]
24  end function
'''

'''
['Node', '1']
['2', '4']
['3', '2']
['Node', '2']
['3', '5']

graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}
'''