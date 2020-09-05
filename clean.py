import shutil

import os

def main():
    if input('Do you want to clean generated data? (y/n)') == 'y':
        shutil.rmtree('cmp')
        os.remove('result_pre.jpg')
        os.remove('result.jpg')
        os.remove('result_full.jpg')
    if input('Do you want to clean portals dataset? (y/n)') == 'y':
        os.rmtree('data')
        os.rmtree('data_feature')
        os.rmtree('data_feature_preview')

if __name__ == "__main__":
    main()

