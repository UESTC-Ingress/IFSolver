import json


def findbd(bd, bds):
    for x in bds:
        if str(x["idx"]) == str(bd):
            return x


def mergep(pic1, pic2):
    with open("result_pics.json", 'r') as fp:
        bds = json.loads(fp.read())

    bd1 = findbd(pic1, bds)
    bd2 = findbd(pic2, bds)

    (x1, y1, w1, h1) = bd1["bd"]
    (x2, y2, w2, h2) = bd2["bd"]

    rw = max(w1, w2)
    rh = max(h1, h2)

    if y1 > y2:
        rx = x1
        ry = y2
    else:
        rx = x1
        ry = y1

    rw = rw + abs(x1 - x2)
    rh = rh + abs(y1 - y2)

    bds.remove(bd1)
    bds.remove(bd2)
    bds.append({"idx": bd1["idx"], "bd": (rx, ry, rw, rh)})

    with open('result_pics.json', 'w') as fp:
        json.dump(bds, fp)

def fix_p():
    print("[IFSolver] Start fixing.")
    id1 = input("Image ID 1: ")
    id2 = input("Image ID 2: ")
    mergep(id1, id2)

if __name__ == "__main__":
    while true:
        fix_p()
