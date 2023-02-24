from modules.utils import DownloadUtil, PreviewUtil
from modules.extractors import SIFTExtractor
from modules.matchers import BFMatcher
from dotenv import load_dotenv
from os.path import join, dirname
import os
from shutil import copyfile, rmtree
from modules.utils import DecodeUtil, GridClusterUtil, GeoUtil
import argparse
import glob
import json
import progressbar

load_dotenv(join(dirname(__file__), '.env'))

parser = argparse.ArgumentParser(prog='ifsolver')
parser.add_argument('--clean-result', help="Clear result files",
                    dest="cleanresult", action='store_true')
parser.add_argument('--clean', help="Clear generated files",
                    dest="clean", action='store_true')
parser.add_argument('--clean-all', help="Clear all files",
                    dest="cleanall", action='store_true')
parser.add_argument('--no-preview', help="Do not generate preview images",
                    dest="nopreview", action='store_false')
parser.add_argument('--download-only', help="Only download portal images (without IFS image)",
                    dest="downloadonly", action='store_true')
parser.add_argument('--no-ifs-image', help="Only download portal images and extract features (without IFS image)",
                    dest="noifsimage", action='store_true')
args = parser.parse_args()


def init(preview=True):
    print("""
  ___ _____ ____        _                
 |_ _|  ___/ ___|  ___ | |_   _____ _ __ 
  | || |_  \___ \ / _ \| \ \ / / _ \ '__|
  | ||  _|  ___) | (_) | |\ V /  __/ |   
 |___|_|   |____/ \___/|_| \_/ \___|_|   
===========================================
GitHub: https://github.com/UESTC-Ingress/IFSolver

Please read README.md first!!!

    """)
    DownloadUtil.init()
    SIFTExtractor.init()
    PreviewUtil.init(set_enabled=preview)


def main(extract=True, match=True):
    print("[STEP] Fetching Data...")
    portalList = DownloadUtil.fetchData()
    if extract:
        print("[STEP] Extracting Features...")
        dList = []
        for portal in progressbar.progressbar(portalList, widgets=[
            'Extracting Feature: ',
            progressbar.Bar(),
            ' ',
            progressbar.Counter(format='%(value)d/%(max_value)d'),
        ], redirect_stdout=True):
            kp, d = SIFTExtractor.getSIFTFeatures(portal['id'])
            dList.append(d)
        if match:
            print("[STEP] Matching Features...")
            kpFull, dFull = SIFTExtractor.getSIFTFeaturesFullPhoto()
            matchedList = []
            matched_cnt = 0
            if not os.path.exists('flag.matched.json'):
                if os.path.exists('result.match.json'):
                    with open('result.match.json') as jf:
                        matchedList = json.load(jf)
                        matched_cnt = matchedList[-1]["portalID"]
                        print("Recovered from ID {}".format(matched_cnt))
                for idx, d in enumerate(progressbar.progressbar(dList, widgets=[
                    'Matching Feature: ',
                    progressbar.Bar(),
                    ' ',
                    progressbar.Counter(format='%(value)d/%(max_value)d'),
                ], redirect_stdout=True)):
                    if idx >= matched_cnt:
                        bestMatches = BFMatcher.matchDescriptor(d, dFull)
                        if len(bestMatches) > 1:
                            print("Processing possible match: ID [{}] Name {}".format(
                                idx, next(DecodeUtil.unquoteName(it["Name"]) for it in portalList if it["id"] == idx)))
                            kp, _ = SIFTExtractor.getSIFTFeatures(str(idx))
                            centers = BFMatcher.getMatchedCenterMultiple(
                                str(idx) + ".jpg", kp, kpFull, bestMatches)
                            if len(centers) != 0:
                                matchedList.append({
                                    "portalID": idx,
                                    "centers": [{"x": center[0], "y": center[1]} for center in centers]
                                })
                                with open("result.match.json", "w") as f:
                                    json.dump(matchedList, f)
                                PreviewUtil.saveMatchedCenterMultiple(
                                    matchedList)
                with open("result.match.json", "w") as f:
                    json.dump(matchedList, f)
                with open("flag.matched.json", "w") as f:
                    json.dump({}, f)
                PreviewUtil.saveMatchedCenterMultiple(matchedList)
            else:
                with open("result.match.json") as f:
                    matchedList = json.load(f)
                PreviewUtil.saveMatchedCenterMultiple(matchedList)
            print("[STEP] Clustering Grid...")
            matchedGridList = GridClusterUtil.Cluster(matchedList)
            PreviewUtil.saveGridInfo(matchedGridList)
            print("[STEP] Generating Final Image...")
            GeoUtil.GenGeoImage(matchedGridList, portalList)
            print("[DONE] Preview your passcode at result_full.jpg")


def del_if_dir_exist(dir):
    if os.path.exists(dir) and os.path.isdir(dir):
        rmtree(dir)


def clean_result_dir():
    del_if_dir_exist("data_features_matches")
    del_if_dir_exist("data_features_preview")
    fl = glob.glob('result_*.jpg')
    for fp in fl:
        os.remove(fp)
    fl = glob.glob('*.json')
    for fp in fl:
        os.remove(fp)


def clean_data_dir():
    del_if_dir_exist("data")
    del_if_dir_exist("data_features")


if __name__ == "__main__":
    if args.cleanresult:
        clean_result_dir()
    elif args.clean:
        clean_result_dir()
        clean_data_dir()
    elif args.cleanall:
        del_if_dir_exist("input")
        clean_result_dir()
        clean_data_dir()
    else:
        init(preview=args.nopreview)
        if args.downloadonly:
            main(extract=False)
        elif args.noifsimage:
            main(match=False)
        else:
            main()
