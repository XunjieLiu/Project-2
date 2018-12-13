import pickle, struct

data1 = {'a': [1, 2.0, 3],
         'b': ('string', 123),
         'c': None}

packData = pickle.dumps(data1)

print(type(packData))
print(packData)
print(pickle.loads(packData))