import json
import numpy as np
import cv2


def GenGeoImage(matchedGridList, portalList):
    rimg = np.zeros((640, 1, 3), np.uint8)
    for colid, col in enumerate(matchedGridList):
        img = np.zeros((640, 640, 3), np.uint8)
        tmplat = [float(next(item for item in portalList if item["id"]
                             == i["portalID"])["Latitude"]) for i in col]
        tmplng = [float(next(item for item in portalList if item["id"]
                             == i["portalID"])["Longitude"]) for i in col]
        latmin = min(tmplat)
        lngmin = min(tmplng)
        lats = max(tmplat) - latmin
        lngs = max(tmplng) - lngmin
        for idx, p in enumerate(col):
            x = float(next(item for item in portalList if item["id"]
                           == p["portalID"])["Longitude"])
            x = ((x - lngmin) / lngs) * 600 + 20
            x = int(x)
            y = float(next(item for item in portalList if item["id"]
                           == p["portalID"])["Latitude"])
            y = ((y - latmin) / lats) * 600 + 20
            y = 640 - int(y)
            color = (0, 255, 0)
            # if not p["valid"]:
            #     color = (0, 0, 255)
            cv2.circle(img,  (x, y), 8, color, 4)
            if idx != 0:
                cv2.line(img, (x, y), (ox, oy), (255, 0, 0), 5)
            ox = x
            oy = y

        cv2.imwrite("result_" + str(colid) + ".jpg", img)
        rimg = np.hstack((rimg, img))
    cv2.imwrite("result_full.jpg", rimg)
