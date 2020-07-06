# IFSolver

A tool to find passcodes of IFS @ Home.

## Preview

### Image Match

![image](http://github.com/UESTC-Ingress/IFSolver/raw/master/doc/result.jpg)

### Passcode

![image](http://github.com/UESTC-Ingress/IFSolver/raw/master/doc/code.jpg)

### Log

```
......
Result for pic 911
Total Keys: 500
Max Match Keys: 1012
Matches: 347
Portal Name: Chinese Academy of Science
Lat: 30.63279
Lng: 104.071148
----------------------------
Result for pic 912
Total Keys: 487
Max Match Keys: 172
Matches: 344
Portal Name: 汉易酒店狮
Lat: 30.616864
Lng: 104.070239
----------------------------
Result for pic 935
Total Keys: 500
Max Match Keys: 609
Matches: 346
Portal Name: 四脚蛇
Lat: 30.628775
Lng: 104.086282
----------------------------
Result for pic 936
Total Keys: 479
Max Match Keys: 1219
Matches: 288
Portal Name: 浮雕5
Lat: 30.637155
Lng: 104.081622
----------------------------
Result for pic 1171
Total Keys: 500
Max Match Keys: 867
Matches: 356
Portal Name: 川大花园
Lat: 30.625708
Lng: 104.076478
.......
```

## Usage

> Notice: Features of nearby portals can be pregenerated without put `ifs.png` in the directory. 

> You can prepare for this part once the IFS portal is determined to reduce the time of processing when the IFS Challenge image is available.

### Step 1:

Use `IITC Plugin: Ingress Portal CSV Export` to download portal list. And put it in the project directory as `Portal_Export.csv`.

### Step 2:

Put IFS Challenge image at the project directory as `ifs.png`. (Please use raw PNG instead of JPG to avoid noise caused by compression)

Use `python3 main.py`.

### Step 3:

The matched image is `result.jpg`.

The passcode image is `result_full.jpg`. 

### Optional:

You may need to change these parameters:

- img_finder.py
```
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
_, infile_bw = cv2.threshold(infile_gradient, 15, 255, cv2.THRESH_BINARY)
```

- img_cmp.py
```
if pic_match[0]["matches"] < 200:
```

You can use `python3 test.py` to test if all portal images are matched correctly.
