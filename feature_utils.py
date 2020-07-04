import os
import numpy as np
import cv2

def read_features(filename):
    if os.path.getsize(filename) <= 0:
        return np.array([]), np.array([])
    f = np.load(filename)
    if f.size == 0:
        return np.array([]), np.array([])
    f = np.atleast_2d(f)
    # return f[:, :7], f[:, 7:]
    return f


def write_features(filename, locs, desc):
    np.save(filename, np.hstack((locs, desc)))


def pack_keypoint(keypoints, descriptors):
    kpts = np.array([[kp.pt[0], kp.pt[1], kp.size,
                      kp.angle, kp.response, kp.octave,
                      kp.class_id]
                     for kp in keypoints])
    desc = np.array(descriptors)
    return kpts, desc


def unpack_keypoint(array):
    try:
        kpts = array[:, :7]
        desc = array[:, 7:]
        keypoints = [cv2.KeyPoint(x, y, _size, _angle, _response, int(_octave), int(_class_id))
                     for x, y, _size, _angle, _response, _octave, _class_id in list(kpts)]
        return keypoints, np.array(desc, np.uint8)
    except(IndexError):
        return np.array([]), np.array([])
