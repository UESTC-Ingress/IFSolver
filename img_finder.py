import cv2
import numpy as np

def pre_process(infile, mat_size, thres):
    (h,w) = infile.shape[:2]
    mask = np.zeros([h+2, w+2],np.uint8)
    cv2.floodFill(infile, mask, (0,0), (255,255,255), (20,20,20), (5,5,5), cv2.FLOODFILL_FIXED_RANGE)
    infile_gray = cv2.cvtColor(infile, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (mat_size, mat_size))
    infile_gradient = cv2.morphologyEx(infile_gray, cv2.MORPH_GRADIENT, kernel)
    _, infile_bw = cv2.threshold(infile_gradient, thres, 255, cv2.THRESH_BINARY)
    return cv2.findContours(
        infile_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


def process_mainfile(mat_size, thres):
    img = cv2.imread('ifs.jpg', cv2.IMREAD_UNCHANGED)
    conts = pre_process(img, int(mat_size), int(thres))
    img_s = img.copy()
    for f in conts:
        (x, y, w, h) = cv2.boundingRect(f)
        if (w*h > 40000):
            cv2.rectangle(img_s, (x, y), (x+w, y+h), (0, 0, 255), 5)
    cv2.imwrite("result_pre.jpg", img_s)
    return img, conts
