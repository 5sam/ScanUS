import numpy as np
from matplotlib import pyplot as plt
import time
import camera
from calibration import calib_camera
from transform import intersect
import cv2
import math


def main():
    points_3d = [[0,0,0],[1,2,3],[1,1,1],[2,-1,3],[-2,0,-3]]
    plt.ion()

    fig, ax = plt.subplots()

    plot = ax.scatter([], [])
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    plot.set_offsets([0,0])
    while True:
        # get two gaussian random numbers, mean=0, std=1, 2 numbers
        point = [np.random.normal(0, 1, 2)]
        # get the current points as numpy array with shape  (N, 2)
        array = plot.get_offsets()

        # add the points to the plot
        array = np.concatenate((array,point))
        plot.set_offsets(array)

        # update x and ylim to show all points:
        ax.set_xlim(array[0].min() - 0.5, array[0].max() + 0.5)
        ax.set_ylim(array[1].min() - 0.5, array[1].max() + 0.5)
        # update the figure
        fig.canvas.draw()


if __name__ == "__main__":
    main()
