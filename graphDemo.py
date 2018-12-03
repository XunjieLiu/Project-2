graphTxt = open('graph.txt', 'r')
for line in graphTxt.readlines():
	print(line.strip('\n').split(' '))



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