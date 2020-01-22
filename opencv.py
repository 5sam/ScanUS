import numpy as np
from matplotlib import pyplot as plt
import cv2
def getcenter(contour):
    M = cv2.moments(contour)
    center_x = M['m10'] / M['m00']
    center_y = M['m01'] / M['m00']
    return [[center_x,center_y]]
def main():
    cap = cv2.VideoCapture(0)
    frame = cv2.imread('D:\_Udes\S4\Projet\ScanUS\Images/pi_test_loin.jpg', cv2.IMREAD_COLOR)
    cv2.namedWindow('gray',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('gray', 400, 300)
    cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('frame', 1000, 750)
    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('mask', 400, 300)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    centers = []
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(gray, 240, 255,0)
    contours,hier  = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            #print(cv2.contourArea(contour))
            center =  getcenter(contour)
            cv2.circle(frame, (int(center[0][0]),int(center[0][1])), 4, (0,0,255), -1)
            centers += center
            cv2.drawContours(frame, contour, -1, [255, 0, 0], 2)
    #cv2.drawContours(frame, contours,0,[255,0,0],3)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame, frame, mask=mask) 
    cv2.imshow('gray',gray)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)
    print(centers)

    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
    #img = cv2.imread('D:\_Udes\S4\Projet/red_dot.jpg', cv2.IMREAD_COLOR)


    #cv2.imshow('image', img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
