import matplotlib.pyplot as plt
import numpy as np
import os
import math

if not os.path.isdir("result/online_heatmap"):
    os.makedirs("result/online_heatmap")

xs = []
ys = []
V = []
T = []
with open("result/online_qtable.txt", "r") as f:
    step = int(f.readline())
    for line in f:
        words = line.split(",")
        xs.append(int(words[0]))
        ys.append(int(words[1]))
        times = []
        vals = []
        for i in range(2, len(words) - 1):
            if i % 2 == 0:
                times.append(int(words[i]))
            else:
                vals.append(float(words[i]))
        T.append(times)
        V.append(vals)

ymin = min(ys)
ymax = max(ys)

xmin = min(xs)
xmax = max(xs)

flat_time = [item for sublist in T for item in sublist]
tmax = max(flat_time)

flat_vals = [item for sublist in V for item in sublist]
vmax = max(flat_vals)
vmin = min(flat_vals)

w = int((ymax - ymin) / step) + 1  # 10,5,1 +-1
h = int((xmax - xmin) / step) + 1  # 10,5,1 +-1

m = np.zeros((w, h, tmax + 1))

for x, y, t, v in zip(xs, ys, T, V):
    j = int((x - xmin) / step)
    i = int((y - ymin) / step)
    for ti, val in zip(t, v):
        m[i, j, ti] = math.log(val - vmin + 1)

maxlog = math.log(vmax - vmin + 1)

for i in range(1, m.shape[2]):  # Sometimes frame 0 is weird
    fig = plt.imshow(m[:, :, i], cmap="hot")
    cbar = plt.colorbar(fig)
    cbar.set_clim(0, maxlog)
    cbar.draw_all()
    # plt.show()
    img = plt.gcf()
    img.set_size_inches(4, 3)
    img.savefig("result/online_heatmap/im_%04d.png" % i, bbox_inches="tight", dpi=150)
    plt.clf()
