import os
import cv2
from modules.utils import FeatureFileUtil, PreviewUtil

sift = cv2.SIFT_create()


def init():
    if not os.path.exists('data_features'):
        os.makedirs('data_features')


def getSIFTFeaturesFullPhoto():
    if not os.path.exists('data_features/ifs.jpg.npy'):
        img = cv2.imread("input/" + os.environ.get("IFS_PHOTO_FILE", "ifs.jpg"), 0)
        if img is None:
            print("[Error] Could not read IFS photo file. Did you forget to place it to input/ifs.jpg?")
            exit(1)
        kp, des = sift.detectAndCompute(img, None)

        PreviewUtil.saveFullImageFeaturePreview(kp)

        kpp, desp = FeatureFileUtil.packKeypoint(kp, des)
        FeatureFileUtil.writeFeatures(
            'data_features/ifs.jpg', kpp, desp)
    else:
        fr = FeatureFileUtil.readFeatures(
            'data_features/ifs.jpg.npy')
        kp, des = FeatureFileUtil.unpackKeypoint(fr)
    return kp, des


def getSIFTFeatures(pid):
    if not os.path.exists('data_features/' + str(pid) + ".jpg.npy"):
        img = cv2.imread('data/' + str(pid) + ".jpg", 0)
        kp, des = sift.detectAndCompute(img, None)

        PreviewUtil.saveImageFeaturePreview(str(pid) + ".jpg", kp)

        kpp, desp = FeatureFileUtil.packKeypoint(kp, des)
        FeatureFileUtil.writeFeatures(
            'data_features/' + str(pid) + ".jpg", kpp, desp)
    else:
        fr = FeatureFileUtil.readFeatures(
            'data_features/' + str(pid) + ".jpg.npy")
        kp, des = FeatureFileUtil.unpackKeypoint(fr)
    return kp, des
