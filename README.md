# IFSolver

A tool to find passcodes of IFS @ Home.

> This version of IFSolver is currently WIP.

## Usage

- Put `Portal_Export.csv` into `./input`.
- Put `ifs.jpg` into `./input`. (Optional)
- Run `python3 main.py`. (With optional args)
- Resolve conflicts in `result.match.json` according to images in `data_features_preview/` manually and run again. (Optional)

## Generated Files

- `result_full.jpg`: Full matched passcode image.
- `result_{}.jpg`: Matched character image for specific column.
- `result.match.json`: Matched image and center information.
- `flag.matched.json`: A flag file to indicate that all images have been matched.
- `data_features_preview/` and `data_features_matches/`: Some useful images for manual intervention if the result is incorrect.
- `data_features/`: Extracted features for each portal image.
- `data/`: Portal images.

## Status

[x] Download images of portals.
[x] Fetch features of portal images.
[x] Match portal images and puzzle image.
[x] Multiple match.
[x] Clustering for grid layout.
[x] Generate glyphs.
[ ] OCR.
[ ] Automatic conflict resolution.