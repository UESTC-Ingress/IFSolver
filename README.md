# IFSolver

A tool to find passcodes of IFS @ Home.

## Preview

### Image Match

#### Step 1

This step is split the Images. 

![image](/doc/result_pre.jpg)

#### Step 2

Result of matching.

![image](/doc/result.jpg)

#### Optional

There is a `cmp` dir for debugging.

![image](/doc/cmp.jpg)

### Passcode

Red points are portals with matching errors.

![image](/doc/result_full.jpg)

### Log

```
[IFSolver] Auto(y) or manual(n)? n
[IFSolver] Downloading latest intel package
[IFSolver] Getting Features
[IFSolver] Splitting Images
[IFSolver] Comparing pictures
Result for pic 0
Total Keys: 500
Max Match Keys: 208
Matches: 344
Portal Name: 石头龙
Lat: 30.64381
Lng: 104.07672
----------------------------
Result for pic 1
Total Keys: 500
Max Match Keys: 143
Matches: 335
Portal Name: 黑妇人舞裙
Lat: 30.639512
Lng: 104.084023
----------------------------
Result for pic 2
Total Keys: 500
Max Match Keys: 400
Matches: 310
Portal Name: 四川大学纪念品店壁画
Lat: 30.629904
Lng: 104.076834
----------------------------
.......
```

## Usage

### Pre-generate

> Notice: Features of nearby portals can be pregenerated without put `ifs.jpg` in the directory. 

> You can prepare for this part once the IFS portal is determined to reduce the time of processing when the IFS Challenge image is available.

### Step 1:

Use [IITC Plugin: Ingress Portal CSV Export](https://github.com/Zetaphor/IITC-Ingress-Portal-CSV-Export) to download portal list. And put it in the project directory as `Portal_Export.csv`.

### Step 2:

Put IFS Challenge image at the project directory as `ifs.jpg`.

Use `python3 main.py`.

### Step 3:

Follow the guide.

Auto split image is not finished yet.

Split images manually:
- Right-click and drag to select images.
- Press Enter to confirm.
- Press Q to end this step.

### Step 4:

The matched image is `result.jpg`.

The passcode image is `result_full.jpg`. 

### Optional:

`download_utils.py` can run independently if there is a `Portal_Export.csv`.

`geo.py` can run independently if there is a `result.json`.
