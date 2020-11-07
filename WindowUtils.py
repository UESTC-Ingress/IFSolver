import cv2
import numpy as np
import os
import sys

cropping = False

x_start, y_start, x_end, y_end = 0, 0, 0, 0

global oriImage


def mouse_crop(event, x, y, flags, param):
    # grab references to the global variables
    global x_start, y_start, x_end, y_end, cropping
    global croppedImage

    # if the left mouse button was DOWN, start RECORDING
    # (x, y) coordinates and indicate that cropping is being
    if event == cv2.EVENT_RBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True

    # Mouse is Moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    # if the left mouse button was released
    elif event == cv2.EVENT_RBUTTONUP:
        # record the ending (x, y) coordinates
        x_end, y_end = x, y
        cropping = False  # cropping is finished

        refPoint = [(x_start, y_start), (x_end, y_end)]

        if len(refPoint) == 2:  # when two points were found
            roi = oriImage[refPoint[0][1]:refPoint[1]
                           [1], refPoint[0][0]:refPoint[1][0]]
            croppedImage = roi
            cv2.imshow("Cropped", roi)


def get_img(image):
    global x_start, y_start, x_end, y_end, cropping, oriImage

    cropping = False
    x_start, y_start, x_end, y_end = 0, 0, 0, 0

    cv2.namedWindow("IFSolver Cropper", cv2.WINDOW_GUI_NORMAL)
    cv2.setWindowProperty("IFSolver Cropper",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.setMouseCallback("IFSolver Cropper", mouse_crop)

    oriImage = image.copy()

    key = cv2.waitKey(1) & 0xFF

    while True:
        i = image.copy()

        if not cropping:
            cv2.imshow("IFSolver Cropper", image)

        elif cropping:
            cv2.rectangle(i, (x_start, y_start),
                          (x_end, y_end), (255, 0, 0), 2)
            cv2.imshow("IFSolver Cropper", i)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            cv2.destroyAllWindows()
            return None
        if key == 13:
            cv2.destroyAllWindows()
            return ((x_start, y_start), (x_end, y_end))

    cv2.destroyAllWindows()
