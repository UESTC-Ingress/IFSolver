import cv2
import os
import numpy as np

preview_enabled = True

def init(set_enabled=True):
    global preview_enabled
    preview_enabled = set_enabled
    if set_enabled:
        if not os.path.exists('data_features_matches'):
            os.makedirs('data_features_matches')
        if not os.path.exists('data_features_preview'):
            os.makedirs('data_features_preview')


def saveImageFeaturePreview(imgFile, kp):
    if not preview_enabled:
        return
    img = cv2.imread("data/" + imgFile)
    for kpit in kp:
        cv2.circle(img, tuple(map(int, kpit.pt)), 1, (0, 0, 255), 4)
    cv2.imwrite("data_features_preview/" + imgFile, img)


def saveFullImageFeaturePreview(kp):
    if not preview_enabled:
        return
    img = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE", "ifs.jpg"))
    for kpit in kp:
        cv2.circle(img, tuple(map(int, kpit.pt)), 1, (0, 0, 255), 4)
    cv2.imwrite("data_features_preview/ifs.jpg", img)


def saveMatchedCenterMultiple(matchedList):
    if not preview_enabled:
        return
    imgFull = cv2.imread(
        "input/" + os.environ.get("IFS_PHOTO_FILE", "ifs.jpg"))
    for matched in matchedList:
        for center in matched["centers"]:
            imgFull = cv2.circle(
                imgFull, (center["x"], center["y"]), 5, (0, 255, 255), 8)
            imgFull = cv2.putText(
                imgFull, str(matched["portalID"]), (center["x"], center["y"]), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 8)
    cv2.imwrite("data_features_matches/ifs.jpg", imgFull)


def saveGridInfo(matchedGridList):
    if not preview_enabled:
        return
    imgFull = cv2.imread("data_features_matches/ifs.jpg")
    for idx, colList in enumerate(matchedGridList):
        for center in colList:
            imgFull = cv2.putText(
                imgFull, str(idx), (center["x"], center["y"]), cv2.FONT_HERSHEY_COMPLEX, 4, (0, 0, 255), 15)
    cv2.imwrite("data_features_matches/ifs-grid.jpg", imgFull)
