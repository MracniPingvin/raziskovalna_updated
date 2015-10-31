__author__ = 'FAMILY'

import time
import pickle

from classes.graph import Graph
from functions.generate import generate
from functions.clean import clean

e=pickle.load(open("matrix_list_fixed.p", "rb"))
for i in clean(e):
    print(i)
maxtime = 0
avg_time = 0
count = 0
g = Graph(10, 10, [4, 4, 0], "squared")
for i in generate("squared", 4, 2, 2, 2, 2, 2):
    count += 1
    start = time.clock()
    g.draw_layers(*i)
    end = time.clock()
    if (end - start > maxtime):
        maxtime = end - start

    avg_time = (avg_time * count + (end - start)) / (count + 1)
    if (count % 10000 == 0):
        print("count: ", count)
        print("time: ", time.clock())
        print("found: ", g.found)
        print("average: ", avg_time)
        print("max: ", maxtime)
pickle.dump(g.matrix_list, open("matrix_list_5segment.p", "wb"))
print(time.clock())
print(g.found)
print(avg_time)
print(maxtime)
print(count)
