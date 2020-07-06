import json
import numpy as np
import cv2


def geo():
    with open('result.json', 'r') as f:
        data = json.load(f)
    ks = list(data.keys())
    ks = list(map(int, ks))
    ks.sort()
    rimg = np.zeros((640, 1, 3), np.uint8)
    for kid, k in enumerate(ks):
        row = data[str(k)]
        img = np.zeros((640, 640, 3), np.uint8)
        tmplat = [float(i['lat']) for i in row]
        tmplng = [float(i['lng']) for i in row]
        latmin = min(tmplat)
        lngmin = min(tmplng)
        lats = max(tmplat) - latmin
        lngs = max(tmplng) - lngmin
        row = sorted(row, key=lambda k: k['y']) 
        for idx, p in enumerate(row):
            x = float(p["lng"])
            x = ((x - lngmin) / lngs) * 600 + 20
            x = int(x)
            y = float(p["lat"])
            y = ((y - latmin) / lats) * 600 + 20
            y = 640 - int(y)
            if idx != 0:
                print("from x " + str(x) + " y " + str(y))
                print("to x " + str(ox) + " y " + str(oy))
                cv2.line(img, (x, y), (ox, oy), (255, 0, 0), 5)
            ox = x
            oy = y

        #cv2.imshow("test", img)
        cv2.imwrite("result_" + str(kid) + "_" + str(k) + ".jpg", img)
        rimg = np.hstack((rimg, img))
        #cv2.waitKey(999)
    cv2.imwrite("result_full.jpg", rimg)


if __name__ == "__main__":
    geo()
