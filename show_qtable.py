import matplotlib.pyplot as plt
import numpy as np
import math

xs = []
ys = []
vals = []
with open('resultado/offline_learn.txt', 'r') as f:
    step = int(f.readline())
    for line in f:
        words = line.split(',')
        xs.append(int(words[0]))
        ys.append(int(words[1]))
        vals.append(float(words[2]))

ymin = min(ys)
ymax = max(ys)

xmin = min(xs)
xmax = max(xs)

vmin = min(vals)

w = int((ymax - ymin) / step) + 1  # 10,5,1 +-1
h = int((xmax - xmin) / step) + 1  # 10,5,1 +-1

m = np.zeros((w, h))

for x, y, v in zip(xs, ys, vals):
    j = int((x - xmin) / step)
    i = int((y - ymin) / step)
    m[i, j] = v

plt.imshow(m, cmap='hot')
plt.colorbar()
plt.show()
