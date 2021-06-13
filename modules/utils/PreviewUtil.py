import cv2
import os
import numpy as np


def init():
    if not os.path.exists('data_features_matches'):
        os.makedirs('data_features_matches')


def saveImageFeaturePreview(imgFile, kp):
    img = cv2.imread("data/" + imgFile)
    for kpit in kp:
        cv2.circle(img, tuple(map(int, kpit.pt)), 1, (0, 0, 255), 4)
    cv2.imwrite("data_features_preview/" + imgFile, img)


def saveFullImageFeaturePreview(kp):
    img = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE"))
    for kpit in kp:
        cv2.circle(img, tuple(map(int, kpit.pt)), 1, (0, 0, 255), 4)
    cv2.imwrite("data_features_preview/ifs.jpg", img)


def saveMatchedFeaturePreview(imgFile, kp, kpFull, matches):
    img = cv2.imread("data/" + imgFile)
    imgFull = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE"))
    imgDual = np.empty(
        (max(img.shape[0], imgFull.shape[0]), img.shape[1]+imgFull.shape[1], 3), dtype=np.uint8)

    imgPts = np.float32(
        [kp[m[0].queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    imgFullPts = np.float32(
        [kpFull[m[0].trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(imgPts, imgFullPts, cv2.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h, w = img.shape[:2]
    pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]
                     ).reshape(-1, 1, 2)

    dst = cv2.perspectiveTransform(pts, M)
    dst += (w, 0)

    MM = cv2.moments(dst)
    cX = int(MM["m10"] / MM["m00"])
    cY = int(MM["m01"] / MM["m00"])

    imgMatches = cv2.drawMatchesKnn(img, kp, imgFull, kpFull, matches, None)
    imgMatches = cv2.polylines(
        imgMatches, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)
    imgMatches = cv2.circle(imgMatches, (cX, cY), 1, (0, 255, 255), 8)
    cv2.imwrite("data_features_matches/" + imgFile, imgMatches)


def saveMatchedCenter(matchedList):
    imgFull = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE"))
    for matched in matchedList:
        imgFull = cv2.circle(
            imgFull, (matched["center"]["x"], matched["center"]["y"]), 1, (0, 255, 255), 8)
    cv2.imwrite("data_features_matches/ifs.jpg", imgFull)
