# author: Dingyuan
# date: May 15 2020
# this scripts draw the hexagon
import turtle as t
import random
import pickle
def draw_hex(points, color=(-1,-1,-1)):
    if color[0] == -1:
        r = int(random.random() * 255)
        g = int(random.random() * 255) 
        b = int(random.random() * 255)
    else:
        r, g, b = color
    t.fillcolor(r, g, b)
    t.pencolor(0, 0, 0)
    t.penup()
    t.goto(points[0][0], points[0][1])
    t.pendown()
    t.begin_fill()
    for i in range(1, len(points)):
        t.goto(points[i][0], points[i][1])
    t.goto(points[0][0], points[0][1])
    t.end_fill()
    t.penup()

# 加载grids
grids = []
f = open("./hexagon_grid_table.csv", "r")
line = f.readline()
while line:
    grid = [len(grids)]
    points = line.split(',')[1:]
    grid.append([[(float(points[i]) -104.35) * 500, (float(points[i + 1]) - 30.83) * 500] for i in range(0, len(points), 2)])
    grids.append(grid)
    line = f.readline()
f.close()

# 加载values
values = pickle.load(open("values", "rb"))
value_cnt = [0 for i in range(len(grids))]

# 加载订单
# f = open("./samples_ride1", "r")
# line = f.readline()
# cnt = 0
# while line:
#     cnt += 1
#     if cnt % 100000 == 0:
#         print(cnt)
#     elems = line.split(',')
#     value_cnt[int(elems[2])] += 1
#     value_cnt[int(elems[3])] += 1
#     line = f.readline()
# f.close()


# # ABBCCCC A- dow BB- time CCCC grids
# 加载value值
for dow in range(7):
    for ti in range(48):
        for i in range(len(grids)):
            state = dow * 1000000 + ti * 10000 + i
            try:
                value_cnt[i] += values[state]
            except:
                #print(state)
                pass

max_val = max(value_cnt)
min_val = min(value_cnt)
print(min_val, max_val)
# 绘图
t.colormode(255)
t.tracer(False)
t.setup(width=1400,height=1000)
for i in range(len(grids)):
    r = int((value_cnt[i] - min_val) / max_val * 254 * 255 * 255)
    if abs(value_cnt[i]) > 0.000001:
        draw_hex(grids[i][1], (r // (255 * 255), (r // 255) % 255, r % 255))
    else:
        draw_hex(grids[i][1], (255, 255, 255))
input()
