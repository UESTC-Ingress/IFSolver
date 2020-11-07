from multiprocessing.pool import ThreadPool
import cv2
from os import path, makedirs
import json

from FeatureFileUtils import *
from DownloadUtils import *
from CmpUtils import *
from GeoUtils import geo
from SplitUtils import *


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


def main_split():
    print("[IFSolver] Splitting Images")
    img = cv2.imread('ifs.jpg', cv2.IMREAD_UNCHANGED)
    if not path.exists("split.json"):
        return split_img(img)
    else:
        with open('split.json') as json_file:
            spl = json.load(json_file)
        return split_img(img, pre=spl)


def main_cmp(imgs, portal_list, dlist):
    print("[IFSolver] Comparing pictures")
    for idx, img in enumerate(imgs):
        pname, lat, lng, valid = cmpImage(
            img, dlist, portal_list)


def main():
    portal_list = main_download()
    dlist = main_features(portal_list)
    splitted_img, imgpos = main_split()
    main_cmp(splitted_img, portal_list, dlist)


if __name__ == "__main__":
    create_dir()
    main()
