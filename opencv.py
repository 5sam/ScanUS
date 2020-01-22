import numpy as np
from matplotlib import pyplot as plt
import cv2

def main():
    cap = cv2.VideoCapture(0)
    frame = cv2.imread('D:\_Udes\S4\Projet\ScanUS\Images/bon_laser_papier.jpg', cv2.IMREAD_COLOR)

    while (True):
        print('hello')
        #ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # define range of blue color in HSV
        lower_blue = np.array([155,25,0])
        upper_blue = np.array([179, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow('hsv',gray)
        cv2.imshow('frame', frame)
        cv2.imshow('mask', hsv)
        cv2.imshow('res', res)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    #img = cv2.imread('D:\_Udes\S4\Projet/red_dot.jpg', cv2.IMREAD_COLOR)


    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
