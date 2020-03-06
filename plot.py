import numpy as np
from matplotlib import pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
import time


def plot(points, mutex):
    plt.ion()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim(-11, 11)
    ax.set_ylim(-11, 11)
    ax.set_zlim(-11, 11)
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
                ax.scatter(x, y, z)


