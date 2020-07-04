import cv2


fast = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def cmpImage(cmpim, dlist, portal_list):
    ks, des = fast.detectAndCompute(cmpim, None)
    pic_match = []
    for idx, d in enumerate(dlist):
        matches = bf.match(des, d)
        pic_match.append({"id": idx, "matches": len(matches)})
    pic_match = sorted(pic_match, key=lambda k: k['matches'], reverse=True)

    print("Total Keys: " + str(len(ks)))
    print("Max Match Keys: " + str(pic_match[0]["id"]))
    print("Matches: " + str(pic_match[0]["matches"]))
    print("Portal Name: " + unquote(portal_list[pic_match[0]["id"]]
                                    ["Name"], encoding='utf-8', errors='replace'))
    print("Lat: " + portal_list[pic_match[0]["id"]]["Latitude"])
    print("Lng: " + portal_list[pic_match[0]["id"]]["Longitude"])

    rdimg = cv2.imread("data/" + str(pic_match[0]["id"]) + ".jpg")
    # cv2.imshow("Result1", cmpim)
    # cv2.imshow("Result2", rdimg)
    # cv2.waitKey(9999)

    valid = True
    if pic_match[0]["matches"] < 200:
        valid = False

    return unquote(portal_list[pic_match[0]["id"]]
                   ["Name"], encoding='utf-8', errors='replace'), portal_list[pic_match[0]["id"]]["Latitude"], portal_list[pic_match[0]["id"]]["Longitude"], valid


def get_features(pid):
    if not os.path.exists('data_feature/' + str(pid) + ".jpg.npy"):
        img = cv2.imread('data/' + str(pid) + ".jpg", 0)
        kp, des = fast.detectAndCompute(img, None)
        # img = cv2.drawKeypoints(img, kp, np.array([]))
        # cv2.imshow("Image", img)
        kpp, desp = pack_keypoint(kp, des)
        write_features('data_feature/' + str(pid) + ".jpg", kpp, desp)
    else:
        fr = read_features('data_feature/' + str(pid) + ".jpg.npy")
        kp, des = unpack_keypoint(fr)
    return kp, des