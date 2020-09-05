from multiprocessing.pool import ThreadPool
import cv2
from os import path, makedirs
import json

from feature_utils import *
from download_utils import *
from img_finder import *
from img_cmp import *
from geo import geo
from fix import *

def create_dir():
    if not path.exists('data'):
        os.makedirs('data')
    if not path.exists('data_feature'):
        os.makedirs('data_feature')
    if not path.exists('data_feature_preview'):
        os.makedirs('data_feature_preview')
    if not path.exists('cmp'):
        os.makedirs('cmp')

def main_download():
    print("[IFSolver] Downloading latest intel package")
    portal_list = getPortals("Portal_Export.csv")
    run = ThreadPool(12).imap_unordered(fetch_url, portal_list)
    for res in run:
        if res != "":
            print(res)
    return portal_list

def main_features(portal_list):
    print("[IFSolver] Getting Features")
    dlist = []
    for portal in portal_list:
        _, d = get_features(portal['id'])
        dlist.append(d)
    if not path.exists("ifs.jpg"):
        print("[IFSolver] No IFS jpg found, exit")
        exit()
    return dlist

def main_preextract(mat_size=2, thres=10):
    psf = process_mainfile(mat_size, thres)
    print("Matrix Size: " + str(mat_size))
    print("Thres: " + str(thres))
    p = input("Please check result_pre.jpg, is it correct? (y/n)")
    if p != "y":
        mat_size = input("New Matrix Size: ")
        thres = input("New Thres: ")
        return main_preextract(mat_size, thres)
    else:
        return psf

def main_extract(img,cnts):
    print("[IFSolver] Extracting pictures")
    row = {}
    bds = []
    if not path.exists("result_pics.json"):
        for idx, f in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(f)
            if (w*h > 40000):
                bds.append({"idx": idx, "bd": (x, y, w, h)})
        with open('result_pics.json', 'w') as fp:
            json.dump(bds, fp)
    else:
        with open("result_pics.json", 'r') as fp:
            bds = json.loads(fp.read())
    img_s = img.copy()
    for f in bds:
        (x, y, w, h) = f["bd"]
        cv2.rectangle(img_s, (x, y), (x+w, y+h), (0, 0, 255), 5)
        cv2.putText(img_s, '#' + str(f["idx"]), (x, y + 40),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
    cv2.imwrite("result_raw.jpg", img_s)
    p = input("Please check result_raw.jpg, is it correct? (y/n)")
    if p != "y":
        fix_p()
        return main_extract(img,cnts)
    else:
        return img, bds, row

def main_fix():
    img, cnts = main_preextract()
    return main_extract(img, cnts)

def main():
    portal_list = main_download()
    dlist = main_features(portal_list)
    img, bds, row = main_fix()
    print("[IFSolver] Comparing pictures")
    for idx, f in enumerate(bds):
        (x, y, w, h) = f["bd"]
        print("Result for pic " + str(idx))
        pname, lat, lng, valid = cmpImage(
            img[y:y+h, x:x+w], dlist, portal_list)
        if valid:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
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
                "lng": lng,
                "valid": valid
            }]
        else:
            row[str(int(x/200))].append({
                "id": idx,
                "name": pname,
                "y": y/100,
                "lat": lat,
                "lng": lng,
                "valid": valid
            })
        print("----------------------------")
    for k in row.keys():
        row[k] = sorted(row[k], key=lambda kk: kk['y'])
    with open('result.json', 'w') as fp:
        json.dump(row, fp)
    cv2.imwrite("result.jpg", img)
    print("[IFSolver] Doing geograpjical image generation")
    geo()

if __name__ == "__main__":
    create_dir()
    main()
