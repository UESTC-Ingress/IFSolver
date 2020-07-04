# IFSolver

A tool to find passcodes of IFS @ Home.

## Usage

### Step 1:

Use `IITC Plugin: Ingress Portal CSV Export` to download portal list. And put it in the project directory as `Portal_Export.csv`.

### Step 2:

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