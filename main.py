from multiprocessing.pool import ThreadPool
import cv2
import json

from feature_utils import *
from download_utils import *
from img_finder import *
from img_cmp import *
from geo import geo

def main():
    portal_list = getPortals("Portal_Export.csv")
    run = ThreadPool(12).imap_unordered(fetch_url, portal_list)
    for res in run:
        if res != "":
            print(res)
    dlist = []
    for portal in portal_list:
        _, d = get_features(portal['id'])
        dlist.append(d)
    img, cnts = process_mainfile()
    row = {}
    for idx, f in enumerate(cnts):
        (x, y, w, h) = cv2.boundingRect(f)
        if (w*h > 300*300):
            print("Result for pic " + str(idx))
            pname, lat, lng, valid = cmpImage(
                img[y:y+h, x:x+w], dlist, portal_list)
            if valid:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 5)
                cv2.putText(img, 'Lat: ' + lat, (x, y + 40),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(img, 'Lng: ' + lng, (x, y + 80),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
            if str(int(x/200)) not in row.keys():
                row[str(int(x/200))] = [{
                    "id": idx,
                    "name": pname,
                    "y": y/100,
                    "lat": lat,
                    "lng": lng
                }]
            else:
                row[str(int(x/200))].append({
                    "id": idx,
                    "name": pname,
                    "y": y/100,
                    "lat": lat,
                    "lng": lng
                })
            print("----------------------------")
    for k in row.keys():
        row[k] = sorted(row[k], key=lambda kk: kk['y'])
    with open('result.json', 'w') as fp:
        json.dump(row, fp)
    cv2.imwrite("result.jpg", img)

    geo()

if __name__ == "__main__":
    main()