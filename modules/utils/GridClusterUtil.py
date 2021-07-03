from sklearn.cluster import KMeans
import numpy as np


def Cluster(matches):
    centerXList = []

    for match in matches:
        for center in match["centers"]:
            centerXList.append(int(center["x"]))
    nClusters = int(input("Number of clusters: "))
    centerXList = np.array(centerXList).reshape(-1, 1)
    kmeans = KMeans(n_clusters=nClusters).fit(centerXList)

    imageCenterList = [[] for x in range(nClusters)]

    for idx1, match in enumerate(matches):
        for idx2, center in enumerate(match["centers"]):
            col = kmeans.predict(
                np.array([int(center["x"])]).reshape(-1, 1)).tolist()[0]
            matches[idx1]["centers"][idx2]["portalID"] = matches[idx1]["portalID"]
            imageCenterList[col].append(matches[idx1]["centers"][idx2])

    imageCenterList = [sorted(x, key=lambda k: k['y'])
                       for x in imageCenterList]
    imageCenterList = sorted(imageCenterList, key=lambda k: k[0]['x'])
    for imageCenters in imageCenterList:
        for idx in range(len(imageCenters) - 1):
            if (abs(imageCenters[idx]["y"] - imageCenters[idx + 1]["y"]) < 50) and imageCenters[idx]["portalID"] != imageCenters[idx + 1]["portalID"]:
                print("[Warning] Please resolve conflict between image ID {} and {} manually!".format(
                    str(imageCenters[idx]["portalID"]), str(imageCenters[idx + 1]["portalID"])))
    return imageCenterList


if __name__ == "__main__":
    import json
    with open("result.match.json") as f:
        j = json.load(f)
    j2 = Cluster(j)
    print(j2)
