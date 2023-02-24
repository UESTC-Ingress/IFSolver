# IFSolver

A tool to find passcodes of IFS @ Home.

## Requirements

`pip install -r requirements.txt`

virtualenv is strongly recommended.

## Usage

- Put `Portal_Export.csv` into `./input`.

  You can grab portal list with userscripts, like [Portal CSV Exporter](http://github.com/Zetaphor/IITC-Ingress-Portal-CSV-Export) or [IITC plugin: Portal Multi Export](https://iitc.aradiv.de/plugin/37/multi_export.user.js). Modification of the userscript may be required.

- Put `ifs.jpg` into `./input`. (Optional if you use `--download-only` arg)
- Run `python3 main.py`. (With optional args, see below)
- Resolve conflicts in `result.match.json` according to images in `data_features_preview/` manually and run again. (Optional)

### Args

- `--clean-result`: Clear result files (passcode image and json result files)
- `--clean`: Clear generated files (including result files)
- `--clean-all`: Clear all files (including input files)
- `--download-only`: Only download portal images (without IFS image)
- `--no-ifs-image`: Only download portal images and extract features (without IFS image)
- `--no-preview`: Do not generate feature previewing images for manual intervention

## Generated Files

- `result_full.jpg`: Full matched passcode image.
- `result_{}.jpg`: Matched character image for specific column.
- `result.match.json`: Matched image and center information.
- `flag.matched.json`: A flag file to indicate that all images have been matched.
- `data_features_preview/` and `data_features_matches/`: Some useful images for manual intervention if the result is incorrect.
- `data_features/`: Extracted features for each portal image.
- `data/`: Portal images.

## Status

- [x] Download images of portals.
- [x] Fetch features of portal images.
- [x] Match portal images and puzzle image.
- [x] Multiple match.
- [x] Clustering for grid layout.
- [x] Generate glyphs.
- [ ] OCR.
- [ ] Automatic conflict resolution.
