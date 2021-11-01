import re
import requests
import os

from collections import OrderedDict
from multiprocessing.pool import ThreadPool


def init():
    if not os.path.exists('input'):
        os.makedirs('input')
    if not os.path.exists('data'):
        os.makedirs('data')


def fetch_url(entry):
    ret = ""
    path = 'data/' + str(entry["id"]) + ".jpg"
    if not os.path.exists(path):
        r = requests.get(entry["Image"], stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        ret = "Downloaded image id " + str(entry["id"])
    return ret


def getPortals(portalListFile):
    portalList = []
    cnt = 0
    try:
        with open("input/" + portalListFile, encoding="utf-8", newline='', errors="replace") as csvfile:
            for line in csvfile:
                tmp = OrderedDict()
                match = re.match(
                    r'^\"([\S\s]+)\"\,(-?\d+\.\d+)\,(-?\d+.\d+)\,\"(.*)\"', line)
                if match:
                    if match.group(4) != '':
                        if ',' in match.group(1):
                            s = re.sub(r'\,', '%u002c', match.group(1))
                        else:
                            s = match.group(1)
                        s = re.sub(r'[\\/:\*\?\"<>\|]', '', s)
                        tmp['Name'] = s
                        tmp['Latitude'] = match.group(2)
                        tmp['Longitude'] = match.group(3)
                        tmp['Image'] = match.group(4)
                        tmp['id'] = cnt
                        portalList.append(tmp)
                        cnt = cnt + 1
    except FileNotFoundError:
        print(f"[ERROR] File not found: input/{portalListFile}. Please place \"{portalListFile}\" to proper location.")
        exit(1)
    return portalList


def fetchData():
    portalList = getPortals(os.environ.get("PORTAL_LIST_FILE", "Portal_Export.csv"))
    while True:
        run = ThreadPool(int(os.environ.get("DOWNLOAD_THREADS", 32)
                             )).imap_unordered(fetch_url, portalList)
        for res in run:
            if res != "":
                print(res)
        if len(portalList) == len([name for name in os.listdir('data') if os.path.isfile(os.path.join('data', name))]):
            break
    return portalList
