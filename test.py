import cv2
import numpy as np

def pre_process(infile):
    infile_gray = cv2.cvtColor(infile, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    infile_gradient = cv2.morphologyEx(infile_gray, cv2.MORPH_GRADIENT, kernel)
    _, infile_bw = cv2.threshold(infile_gradient, 15, 255, cv2.THRESH_BINARY)
    cv2.imshow("Result", infile_gradient)
    cv2.waitKey()
    return cv2.findContours(
        infile_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


def main():
    cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
    img = cv2.imread('ifs.png', cv2.IMREAD_UNCHANGED)
    conts = pre_process(img)
    print(conts)
    for cont in conts:
        (x, y, w, h) = cv2.boundingRect(cont)
        if (w*h > 300*300):
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 5)
            process(img[y:y+h, x:x+w])
    cv2.imshow("Result", img)
    cv2.waitKey()


if __name__ == "__main__":
    main()
