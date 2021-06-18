import cv2
import os
import numpy as np

matcher = cv2.BFMatcher()


def matchDescriptor(descriptor, descriptorFull):
    matches = matcher.knnMatch(descriptor, descriptorFull, k=2)
    bestMatches = [[m] for m, n in matches if m.distance < 0.6*n.distance]
    return bestMatches


def getMatchedCenterMultiple(imgFile, kp, kpFull, matches):
    img = cv2.imread("data/" + imgFile)
    imgFull = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE"))
    imgMatches = cv2.drawMatchesKnn(img, kp, imgFull, kpFull, matches, None)
    centers = []
    while True:
        if len(matches) < 4:
            break
        imgPts = np.float32(
            [kp[m[0].queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        imgFullPts = np.float32(
            [kpFull[m[0].trainIdx].pt for m in matches]).reshape(-1, 1, 2)
        M, mask = cv2.findHomography(imgPts, imgFullPts, cv2.RANSAC, 5.0)
        h, w = img.shape[:2]
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]
                         ).reshape(-1, 1, 2)
        if M is None:
            break
        dst = cv2.perspectiveTransform(pts, M)

        dstList = dst.tolist()

        dstListX = sorted(dstList, key=lambda x: x[0][0])
        dstListY = sorted(dstList, key=lambda x: x[0][1])

        w1 = abs(dstListX[0][0][0] - dstListX[3][0][0])
        w2 = abs(dstListX[1][0][0] - dstListX[2][0][0])
        h1 = abs(dstListY[0][0][1] - dstListY[3][0][1])
        h2 = abs(dstListY[1][0][1] - dstListY[2][0][1])

        if (w1/w2) < 2 and (w1/w2) > 0.5 and (h1/h2) < 2 and (h1/h2) > 0.5 and (h1/w1) < 8 and (h1/w1) > 0.125:
            MM = cv2.moments(dst)
            cX = int(MM["m10"] / MM["m00"])
            cY = int(MM["m01"] / MM["m00"])

            centers.append((cX, cY))

            dst += (w, 0)
            imgMatches = cv2.polylines(
                imgMatches, [np.int32(dst)], True, (0, 0, 255), 3, cv2.LINE_AA)

        mask = mask.ravel().tolist()
        matches = np.array(matches)[np.logical_not(mask)].tolist()   
    print("Found {} matched pictures for {}".format(len(centers), imgFile))
    if len(centers) >= 1:
        cv2.imwrite("data_features_matches/" + imgFile, imgMatches)
    return centers
