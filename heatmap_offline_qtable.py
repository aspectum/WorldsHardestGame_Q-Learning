import matplotlib.pyplot as plt
import numpy as np
import math

xs = []
ys = []
vals = []
with open('result/offline_learn.txt', 'r') as f:
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
vmax = max(vals)

w = int((ymax - ymin) / step) + 1
h = int((xmax - xmin) / step) + 1

m = np.zeros((w, h))

for x, y, v in zip(xs, ys, vals):
    j = int((x - xmin) / step)
    i = int((y - ymin) / step)
    m[i, j] = math.log(v - vmin + 1)


maxlog = math.log(vmax - vmin + 1)

fig = plt.imshow(m, cmap='hot')
cbar = plt.colorbar(fig)
cbar.draw_all()
img = plt.gcf()
img.set_size_inches(4, 3)
img.savefig('result/offline_heatmap.png', bbox_inches='tight', dpi=150)
