import json
import numpy as np
import cv2


def geo():
    with open('result.json', 'r') as f:
        data = json.load(f)
    rimg = np.zeros((640, 1, 3), np.uint8)
    for colid, col in enumerate(data):
        img = np.zeros((640, 640, 3), np.uint8)
        tmplat = [float(i['lat']) for i in col]
        tmplng = [float(i['lng']) for i in col]
        latmin = min(tmplat)
        lngmin = min(tmplng)
        lats = max(tmplat) - latmin
        lngs = max(tmplng) - lngmin
        sort_col = sorted(col, key=lambda k: k['pos'][1])
        for idx, p in enumerate(sort_col):
            x = float(p["lng"])
            x = ((x - lngmin) / lngs) * 600 + 20
            x = int(x)
            y = float(p["lat"])
            y = ((y - latmin) / lats) * 600 + 20
            y = 640 - int(y)
            color = (0, 255, 0)
            if not p["valid"]:
                color = (0, 0, 255)
            cv2.circle(img,  (x, y), 8, color, 4)
            if idx != 0:
                cv2.line(img, (x, y), (ox, oy), (255, 0, 0), 5)
            ox = x
            oy = y

        #cv2.imshow("test", img)
        cv2.imwrite("result_" + str(colid) + ".jpg", img)
        rimg = np.hstack((rimg, img))
        # cv2.waitKey(999)
    cv2.imwrite("result_full.jpg", rimg)


if __name__ == "__main__":
    geo()
