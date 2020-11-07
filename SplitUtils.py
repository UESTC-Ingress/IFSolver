import cv2
from WindowUtils import *
from os import path
import json

def rect_img(im, pts):
    cv2.rectangle(im, (pts[0][0], pts[0][1]),
                  (pts[1][0], pts[1][1]), (0, 0, 255), 4)


def crop_img(im, pts_list):
    img_arr = []
    pos_arr = []
    tmp_col = []
    for pts in pts_list:
        x1, y1 = pts[0]
        x2, y2 = pts[1]
        img_arr.append(im[y1:y2, x1:x2])
        pos_arr.append(((x1+x2)/2, (y1+y2)/2))
    return img_arr, pos_arr


def split_img(im, pre=None):
    arr = []
    pure_im = im.copy()
    if pre != None:
        arr = pre
        for pts in pre:
            rect_img(im, pts)
    ret = get_img(im)
    if ret != None:
        rect_img(im, ret)
        arr.append(ret)
    while ret != None:
        ret = get_img(im)
        if ret != None:
            rect_img(im, ret)
            arr.append(ret)
    with open('split.json', 'w') as outfile:
        json.dump(arr, outfile)
    return crop_img(pure_im, arr)


if __name__ == "__main__":
    img = cv2.imread('ifs.jpg', cv2.IMREAD_UNCHANGED)
    split_img(img)
