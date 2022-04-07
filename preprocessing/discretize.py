import numpy as np
import pandas as pd
import os
import sys
import time, datetime
import csv

FILE_PATH = "./total_ride_request"
grid_name  = "hexagon_grid_table.csv"
SAMPLE_NUM = 500000
obj_name = "samples_ride"

SAMPLE_PER_DAY = SAMPLE_NUM // 30

def discrete_time(start_time_stamp, cur_time):
    return int((cur_time - start_time_stamp) / (60 * 30))

def pnpoly(testx, testy, boundary):
    nvert = boundary.shape[0]
    c = 0
    i = 0
    j = nvert - 1
    vertx = boundary[:, 0]
    verty = boundary[:, 1]
    while i < nvert:
        if (((verty[i] > testy) != (verty[j] > testy)) and
                (testx < (vertx[j] - vertx[i]) * (testy - verty[i]) / (verty[j] - verty[i]) + vertx[i])):
            c = 1 ^ c
        j = i
        i = i + 1
    return c

def judge_area(lng, lat, boundary, fuzzy=False):
    boundary = np.array(boundary)
    [lng_max, lat_max] = np.amax(boundary, axis=0)
    [lng_min, lat_min] = np.amin(boundary, axis=0)
    if lng < lng_min or lng > lng_max or lat < lat_min or lat > lat_max:
        return False
    if fuzzy:
        return True
    else:
        c = pnpoly(lng, lat, boundary)
        if c == 1:
            return True
        else:
            return False

def discrete_location(lng, lat, grids):
    ids = list(tree_index.nearest((lng, lat, lng, lat), 5))[:5]
    for one_id in ids:
        if judge_area(lng, lat, grids[id][1]):
            return one_id
    return -1

def load_grids():
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
    print("load finished, %d grids found" % len(grids))
    return grids

# 加载六边形
grids = load_grids()
# 加载索引树
tree_index = index.Index('rtree')

fw = open(os.path.join(FILE_PATH, obj_name), "w")
csv_writer = csv.writer(fw)
# 对每天的order进行采样
for day in range(1, 31):
    date = "201611" + "%02d" %  day
    print("scanning" + date)
    file_name = "order_" + date
    # 当日开始时间戳
    start_time_stamp = int(datetime.datetime(2016, 11, day, 0, 0).timestamp())
    df = pd.read_csv(os.path.join(FILE_PATH, file_name), header=None).iloc[:,1:]
    print("load finish")
    choose_samples = df.sample(n = SAMPLE_PER_DAY, random_state=0, axis=0)
    print("get %d samples" % choose_samples.shape[0])
    cnt = 0
    for idx, row in choose_samples.iterrows():
        cnt += 1
        if cnt % 100 == 0:
            print(cnt)
        elems = [discrete_time(start_time_stamp, row[1]), discrete_time(start_time_stamp, row[2]), discrete_location(row[3], row[4], grids), discrete_location(row[5], row[6], grids), row[7], day % 7]
        print(elems)
        input()
        csv_writer.writerow(elems)
    print("finish ", date, "get %d entries" % cnt)

f.close()
