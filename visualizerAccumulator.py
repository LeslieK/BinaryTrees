"""
This module defines a plotter that plots a scatter plot (gray)
and plots an average (red)
"""

import matplotlib.pyplot as plt
import numpy as np


class VisualAnalyzer(object):
    def __init__(self, trials, maxval, title="red black search tree"):
        self.count = 0
        self.total = 0
        self.vals = np.zeros((trials), dtype=np.float64)
        self.means = np.zeros((trials), dtype=np.float64)
        self.maxval = maxval
        self.trials = trials
        self.title = title

    def addDataValue(self, value):
        self.vals[self.count] = value
        self.total += value
        self.means[self.count] = self.total / float(self.count + 1)
        self.count += 1

    def plotData(self):
        fig = plt.figure()
        left, bot, w, h = .1, .1, .8, .8
        rect = [left, bot, w, h]
        axes = fig.add_axes(rect)
        axes.set_xlim(0, self.trials)
        axes.set_ylim(0, self.maxval)
        axes.set_xlabel("put operations")
        axes.set_ylabel("cost")
        axes.set_title(self.title)
        #axes.set_title("binary search tree")
        #axes.set_title("red-black tree: left and right rotations")
        axes.plot(self.vals, linestyle='*', marker='.', color="gray", markersize=1, label="values")
        axes.plot(self.means, linestyle='-', color="red", linewidth=5, label="means")
        #  1: upper right 2: upper left corner 3: lower-left 4: lower-right
        #  0: surprise!
        axes.legend(loc=2)

##########################################

if __name__ == "__main__":
    a = VisualAnalyzer(10, 5)
    for i in range(5):
        a.addDataValue(i)
    a.plotData()









