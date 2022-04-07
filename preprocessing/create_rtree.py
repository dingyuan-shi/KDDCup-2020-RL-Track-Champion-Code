import numpy as np
from rtree import index
grid_name  = "hexagon_grid_table.csv"

# 加载grids
grids = []
f = open(grid_name, "r")
line = f.readline()
while line:
    grid = [len(grids)]
    points = line.split(',')[1:]
    grid.append([[float(points[i]), float(points[i + 1])] for i in range(0, len(points), 2)])
    grids.append(grid)
    line = f.readline()
f.close()
# 结束加载  entry [index from 0, [[], [], [], ]

class Hex(object):
    def __init__(self, no, points):
        self.no = no
        self.points = points

tree_idx = index.Index('rtree')

for entry in grids:
    idx, points = entry
    hexa = Hex(idx, points)
    bottom_point = points[0]
    tree_idx.insert(idx, (bottom_point[0], bottom_point[1], bottom_point[0], bottom_point[1]), obj=hexa)
    if idx % 1000 == 0:
        print(idx)
