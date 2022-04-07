import numpy as np
import pandas as pd
import os
import sys
import time, datetime
import csv
import pickle

try:
    grids_hash2idx = pickle.load(open("grids_hash2idx", "rb"))
    grids_idx2hash = pickle.load(open("grids_idx2hash", "rb"))
except:
    grid_name  = "hexagon_grid_table.csv"
    grids_hash2idx = dict()
    grids_idx2hash = []
    f = open(grid_name, "r")
    line = f.readline()
    while line:
        hash_code = line.split(',')[0]
        grids_hash2idx[hash_code] = len(grids_idx2hash)
        grids_idx2hash.append(hash_code)
        line = f.readline()
    f.close()
    pickle.dump(grids_hash2idx, open("grids_hash2idx", "wb"))
    pickle.dump(grids_idx2hash, open("grids_idx2hash", "wb"))

dicts = [dict() for i in range(24)]

f = open("idle_transition_probability", "r")
line = f.readline()
while line:
    hour, from_hex, to_hex, prob = line.strip().split(',')
    hour = int(hour)
    from_hex_idx = grids_hash2idx[from_hex]
    to_hex_idx = grids_hash2idx[to_hex]
    if from_hex_idx not in dicts[hour]:
        dicts[hour][from_hex_idx] = [[], []]
    dicts[hour][from_hex_idx][0].append(to_hex_idx)
    dicts[hour][from_hex_idx][1].append(prob)
    line = f.readline()
    # print(dicts[0])
    # input()
f.close()
pickle.dump(dicts, open("dicts", "wb"))
~                                            