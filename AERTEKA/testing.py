a = [[1,2], [3,4], [5,6]]

b = [ [1,2], [7,8] ]
a = [[k, v] for k, v in a.items() if k not in b or b[k] < v]
b = [[k, v] for k, v in b.items() if k not in a or a[k] < v]
a += b 
print(a)