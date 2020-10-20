import re
import requests
import os
import csv

from multiprocessing.pool import ThreadPool

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

def getPortals(portals_file):
    portal_list = []
    cnt = 0
    with open(portals_file, encoding="utf-8", newline='') as csvfile:
        portal_reader = csv.DictReader(csvfile, skipinitialspace=True)
        for row in portal_reader:
            row['Name'] = re.sub(r'[\\/:*\?"<>\|]', '', row['Name'])
            if row["Image"]:
                row['id'] = cnt
                portal_list.append(row)
                cnt = cnt + 1
    return portal_list

def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    portal_list = getPortals("Portal_Export.csv")
    run = ThreadPool(12).imap_unordered(fetch_url, portal_list)
    for res in run:
        if res != "":
            print(res)

if __name__ == "__main__":
    main()
