#!/usr/bin/env python
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

import csv

times_same = []
times_jap_us = []
with open('times_same.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        times_same.append(float(row[1]))
        
with open('times_jap_us.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        times_jap_us.append(float(row[1]))

def show_plot(i, data):
    p1 = plt.figure(i)
    n, bins, patches = plt.hist(data, 45)

    N = len(data)
    median = np.median(data)
    dev = np.std(data)
    print min(data), max(data), dev
    
    plt.xlabel('time in seconds')
    plt.ylabel('count')
    plt.title(r'$n=%i\ median=%.01f$' % (N, median))
    plt.grid(True)
    
    p1.show()

show_plot(1, times_same)
show_plot(2, times_jap_us)

raw_input()
