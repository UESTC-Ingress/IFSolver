import shutil
import glob
import os

def main():
    if input('Do you want to clean generated data? (y/n)') == 'y':
        if os.path.isdir('cmp'):
            shutil.rmtree('cmp')
        if os.path.exists('result_pre.jpg'):
            os.remove('result_pre.jpg')
        if os.path.exists('result.jpg'):
            os.remove('result.jpg')
        if os.path.exists('result_full.jpg'):
            os.remove('result_full.jpg')
        if os.path.exists('result.json'):
            os.remove('result.json')
        fileList = glob.glob('result_*.jpg')
        for filePath in fileList:
            os.remove(filePath)
    if input('Do you want to clean portals dataset? (y/n)') == 'y':
        if os.path.isdir('data'):
            os.rmtree('data')
        if os.path.isdir('data_feature'):
            os.rmtree('data_feature')
        if os.path.isdir('data_feature_preview'):
            os.rmtree('data_feature_preview')

if __name__ == "__main__":
    main()

