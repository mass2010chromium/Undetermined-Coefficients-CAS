from collections import deque

lst = [1,2,3,4]
q = deque(lst)
q.rotate()

print(list(q))