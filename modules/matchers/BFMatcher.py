import cv2
import os
import numpy as np

matcher = cv2.BFMatcher()


def matchDescriptor(descriptor, descriptorFull):
    matches = matcher.knnMatch(descriptor, descriptorFull, k=2)
    bestMatches = [[m] for m, n in matches if m.distance < 0.5*n.distance]
    return bestMatches


def getMatchedCenter(imgFile, kp, kpFull, matches):
    img = cv2.imread("data/" + imgFile)
    imgFull = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE"))
    imgPts = np.float32(
        [kp[m[0].queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    imgFullPts = np.float32(
        [kpFull[m[0].trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(imgPts, imgFullPts, cv2.RANSAC, 5.0)

    if M is None:
        return None

    h, w = img.shape[:2]
    pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]
                     ).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    MM = cv2.moments(dst)
    cX = int(MM["m10"] / MM["m00"])
    cY = int(MM["m01"] / MM["m00"])

    return (cX, cY)
