import cv2
import os
from FeatureFileUtils import *
from urllib.parse import unquote


sift = cv2.SIFT_create()

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

def unquote_u(string: str):
    result = unquote(string, encoding='utf-8', errors='replace')
    if '%u' in result:
        result = result.replace('%u', '\\u').encode(
            'utf-8').decode('unicode_escape')
    return result


def cmpEntireImage(ifs_img, d, portalinfo):
    ks, des = sift.detectAndCompute(ifs_img, None)
    matches = flann.knnMatch(d.astype("float32"), des.astype("float32"), k=2)
    matches_len = len(matches)

    print("IFS Total Keys: " + str(len(ks)))
    print("Portal Total Keys: " + str(len(d)))
    print("Matches: " + str(matches_len))
    print("Portal Name: " + unquote_u(portalinfo["Name"]))

    store_im = ifs_img.copy()
    for mt in matches:
        kpit0 = ks[mt[0].trainIdx]
        kpit1 = ks[mt[1].trainIdx]
        cv2.circle(store_im, tuple(map(int, kpit0.pt)), 2, (0, 0, 255), 4)
        #cv2.circle(store_im, tuple(map(int, kpit1.pt)), 2, (0, 255, 0), 4)
    cv2.imwrite("cmp/" + unquote_u(portalinfo["Name"]) + ".jpg", store_im)
    return True


def get_sift_features(pid):
    if not os.path.exists('data_feature_sift/' + str(pid) + ".jpg.npy"):
        img = cv2.imread('data/' + str(pid) + ".jpg", 0)
        kp, des = sift.detectAndCompute(img, None)

        img_color = cv2.imread('data/' + str(pid) + ".jpg")
        for kpit in kp:
            cv2.circle(img_color, tuple(map(int, kpit.pt)), 1, (0, 0, 255), 4)
        cv2.imwrite("data_feature_sift_preview/" + str(pid) + ".jpg", img_color)

        kpp, desp = pack_keypoint(kp, des)
        write_features('data_feature_sift/' + str(pid) + ".jpg", kpp, desp)
    else:
        fr = read_features('data_feature_sift/' + str(pid) + ".jpg.npy")
        kp, des = unpack_keypoint(fr)
    return kp, des
