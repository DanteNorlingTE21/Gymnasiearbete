import numpy as np

test = np.loadtxt('MoveLog\moves.txt', dtype='int', delimiter=',')
inp = test[:, 0]
out = test[:, 1]
print(type(inp[0]))