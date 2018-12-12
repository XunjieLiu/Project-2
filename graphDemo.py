from heapq import *
from copy import *

def get_graph(file):
	graphTxt = open(file, 'r')
	graph = dict() # {'1': [['2', 4], ['3', 2]], '2': [['3', 5]]}
	# 真傻逼 给图也特么不给全 还得自己去创造节点

	node = ''
	for line in graphTxt.readlines():
		if line.find('Node') >= 0:
			node = line.strip('\n').split(' ')[1]
			node = str(node)
			graph[node] = []
		else:
			line = line.strip('\n').split('\t') # ['Node', '1']
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

def dijkstra(graph, source):
	distance = dict()
	previous = dict()
	distance[source] = 0
	heap = [] # 最小堆
	keys = []

	for i in graph.keys(): # 没有意义 只是强迫症所迫
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
		# 终于找到Bug根源了：我错把字典当成优先队列了MD
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

def get_route(destination, map, source):
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

if __name__ == '__main__':	
	graph = get_graph('nodeExample.txt')
	print(graph)
	dist, previous = dijkstra(graph, '1')

	route = get_route('3', previous, '1')
	print(route)


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