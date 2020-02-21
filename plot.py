import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(points_3D):
    ax = plt.gca()
    for element in points_3D:
        x = element[0]
        y = element[1]
        z = element[2]
        ax.scatter(x, y, z)
    plt.pause(1/1000)

def init():
    plt.ion()
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim(-11, 11)
    ax.set_ylim(-11, 11)
    ax.set_zlim(-11, 11)