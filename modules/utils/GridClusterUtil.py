from sklearn.cluster import KMeans
import numpy as np


def Cluster(matches):
    centerXList = []
    for match in matches:
        for center in match["centers"]:
            centerXList.append(int(center["x"]))
    nClusters = input("Number of clusters: ")
    print(centerXList)
    centerXList = np.array(centerXList).reshape(-1, 1)
    print(centerXList.shape)
    kmeans = KMeans(n_clusters=nClusters).fit(centerXList)
    for centr in kmeans.cluster_centers_:
        centroidLabel = kmeans.predict([centr])
        print(centroidLabel)


if __name__ == "__main__":
    import json
    with open("result.match.json") as f:
        j = json.load(f)
    Cluster(j)
