import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import colors
import multiprocessing
from mpl_toolkits.mplot3d import Axes3D
import time


class Plot:

    def __init__(self, name, range=[0, 10]):
        # this can last about 1 sec
        self.m = multiprocessing.Manager()
        self.mutex = self.m.Lock()
        self.points = self.m.list()
        self.t = multiprocessing.Process(target=plot_thread, args=(self.points, self.mutex, name, range))
        self.t.start()

    def close(self):
        self.t.terminate()

    def add_point(self, point):
        self.mutex.acquire()
        self.points += [point]
        self.mutex.release()


def plot_thread(points, mutex, name, range):
    norm = colors.Normalize(vmin=range[0], vmax=range[1])
    f2rgb = cm.ScalarMappable(norm=norm, cmap=cm.get_cmap('gnuplot'))
    plt.ion()
    fig = plt.figure(num=name)
    ax = Axes3D(fig)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(0, 150)
    while True:
        plt.pause(1 / 1000000)
        if points:
            mutex.acquire()
            print(points)
            ax = plt.gca()
            points_to_plot = list(points)
            points[:] = []
            mutex.release()
            for element in points_to_plot:
                x = element[0]
                y = element[1]
                z = element[2]
                try:
                    error = element[3]
                except:
                    error = 0
                ax.scatter(x, y, z, color=f2rgb.to_rgba(error))
