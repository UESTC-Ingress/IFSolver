from modules.utils import DownloadUtil, PreviewUtil
from modules.extractors import SIFTExtractor
from modules.matchers import BFMatcher
from dotenv import load_dotenv
from os.path import join, dirname
import os
from shutil import copyfile
from modules.utils import DecodeUtil
import argparse
import json

load_dotenv(join(dirname(__file__), '.env'))

parser = argparse.ArgumentParser(prog='ifsolver')
parser.add_argument('--clean', help="Clear generated files",
                    dest="clean", action='store_true')
parser.add_argument('--clean-all', help="Clear all files",
                    dest="cleanall", action='store_true')
parser.add_argument('--download-only', help="Only download portal images (without IFS image)",
                    dest="downloadonly", action='store_true')
parser.add_argument('--no-ifs-image', help="Only download portal images and extract features (without IFS image)",
                    dest="noifsimage", action='store_true')
args = parser.parse_args()


def init():
    DownloadUtil.init()
    SIFTExtractor.init()
    PreviewUtil.init()


def main(extract=True, match=True, draw=True, ocr=True):
    print("[STEP] Fetching Data...")
    portalList = DownloadUtil.fetchData()
    if extract:
        print("[STEP] Extracting Features...")
        dList = []
        for portal in portalList:
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
                        j = json.load(jf)
                        matched_cnt = j[-1]["portalID"]
                        print("Recovered from ID {}".format(matched_cnt))
                for idx, d in enumerate(dList):
                    if idx >= matched_cnt:
                        if idx % 50 == 0:
                            print("Current progress: {} images.".format(idx))
                        bestMatches = BFMatcher.matchDescriptor(d, dFull)
                        if len(bestMatches) > 3:
                            print("Found match: ID [{}] Name {}".format(
                                idx, next(DecodeUtil.unquoteName(it["Name"]) for it in portalList if it["id"] == idx)))
                            kp, _ = SIFTExtractor.getSIFTFeatures(str(idx))
                            center = BFMatcher.getMatchedCenter(
                                str(idx) + ".jpg", kp, kpFull, bestMatches)
                            if center != None:
                                PreviewUtil.saveMatchedFeaturePreview(
                                    str(idx) + ".jpg", kp, kpFull, bestMatches)
                                matchedList.append({
                                    "portalID": idx,
                                    "center": {"x": center[0], "y": center[1]}
                                })
                                with open("result.match.json", "w") as f:
                                    json.dump(matchedList, f)
                                PreviewUtil.saveMatchedCenter(matchedList)
                with open("result.match.json", "w") as f:
                    json.dump(matchedList, f)
                with open("flag.matched.json", "w") as f:
                    json.dump({}, f)
                PreviewUtil.saveMatchedCenter(matchedList)
            else:
                with open("result.match.json") as f:
                    matchedList = json.load(f)


if __name__ == "__main__":
    if args.clean:
        pass
    elif args.cleanall:
        pass
    else:
        init()
        if args.downloadonly:
            main(extract=False)
        elif args.noifsimage:
            main(match=False)
        else:
            main()
