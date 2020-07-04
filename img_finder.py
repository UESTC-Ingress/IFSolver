import cv2


def pre_process(infile):
    infile_gray = cv2.cvtColor(infile, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    infile_gradient = cv2.morphologyEx(infile_gray, cv2.MORPH_GRADIENT, kernel)
    _, infile_bw = cv2.threshold(infile_gradient, 15, 255, cv2.THRESH_BINARY)
    return cv2.findContours(
        infile_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


def process_mainfile():
    img = cv2.imread('ifs.png', cv2.IMREAD_UNCHANGED)
    conts = pre_process(img)
    return img, conts