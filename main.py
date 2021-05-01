from multiprocessing.pool import ThreadPool
import cv2
from os import path, makedirs
import json

from FeatureFileUtils import *
from DownloadUtils import *
from CmpUtils import *
from GeoUtils import geo
from SplitUtils import *
from EntireCmpUtils import *
from GridUtils import *


def create_dir():
    if not path.exists('data'):
        os.makedirs('data')
    if not path.exists('data_feature'):
        os.makedirs('data_feature')
    if not path.exists('data_feature_preview'):
        os.makedirs('data_feature_preview')
    if not path.exists('data_feature_sift'):
        os.makedirs('data_feature_sift')
    if not path.exists('data_feature_sift_preview'):
        os.makedirs('data_feature_sift_preview')
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


def main_features(portal_list, sift=True):
    print("[IFSolver] Getting Features")
    dlist = []
    for portal in portal_list:
        if sift:
            _, d = get_sift_features(portal['id'])
        else:
            _, d = get_features(portal['id'])
        dlist.append(d)
    if not path.exists("ifs.jpg"):
        print("[IFSolver] No IFS jpg found, exit")
        exit()
    return dlist


def main_split():
    print("[IFSolver] Splitting Images")
    img = cv2.imread('ifs.jpg', cv2.IMREAD_UNCHANGED)
    if not path.exists("split.json"):
        return split_img(img)
    else:
        with open('split.json') as json_file:
            spl = json.load(json_file)
        return split_img(img, pre=spl)


def main_fast_cmp(imgs, portal_list, dlist, imgpos):
    ret = []
    print("[IFSolver] Comparing pictures")
    for idx, img in enumerate(imgs):
        pname, lat, lng, valid = cmpImage(
            img, dlist, portal_list)
        ret.append({
            "name": pname,
            "lat": lat,
            "lng": lng,
            "valid": valid,
            "pos": imgpos[idx]
        })
    return ret


def main_cmp(ifs_img, portal_list, dlist):
    print("[IFSolver] Comparing pictures")
    for idx, d in enumerate(dlist):
        res = cmpEntireImage(
            ifs_img, d, portal_list[idx])


def main_grid(portals):
    rows = grid_judge(portals)
    with open('result.json', 'w') as outfile:
        json.dump(rows, outfile, ensure_ascii=False)
    return rows


def main():
    portal_list = main_download()
    dlist = main_features(portal_list, sift=True)
    img = cv2.imread('ifs.jpg', cv2.IMREAD_UNCHANGED)
    main_cmp(img, portal_list, dlist)


def main_manual():
    portal_list = main_download()
    dlist = main_features(portal_list)
    splitted_img, imgpos = main_split()
    compared_portals = main_fast_cmp(splitted_img, portal_list, dlist, imgpos)
    main_grid(compared_portals)


if __name__ == "__main__":
    create_dir()
    option = input("[IFSolver] Auto(y) or manual(n)?")
    if option == 'y':
        main()
    else:
        main_manual()
    geo()