graphTxt = open('graph.txt', 'r')
graph = dict()

node = ''
for line in graphTxt.readlines():
	line = line.strip('\n').split(' ') # ['Node', '1']

	if line[0] == 'Node':
		node = "".join(line) # 新的Node
		graph[node] = []
	else:
		line[1] = int(line[1]) # 表示这是权重值
		# 很傻逼 为什么Node的名字非得是数字而不能是字母呢
		temp = graph[node]
		temp.append(line)
		graph[node] = temp

print(graph)


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