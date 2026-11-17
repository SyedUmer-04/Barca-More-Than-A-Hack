# More Than a Hack 2027 - Phase 1 possession (V4)

**Team:** Data Enthusiasts

Rule-based framewise ball-possession prediction for the tactical video. Labels: `H` (home), `A` (away), `D` (dead ball), and `X` (uncertain). This repository contains code only; restricted match assets and generated predictions are not published.

## Method

- Read provided tactical ATD player/ball tracking and track-slot team metadata.
- Assign a tentative team by proximity to a valid tracked ball observation.
- Use temporal smoothing and automatic Smart Tagging as additional evidence when observations are missing.
- Detect sustained out-of-pitch ball readings as dead-ball evidence; filter isolated implausible ball-coordinate spikes.
- Emit one label per tactical video frame. No manually annotated match labels or trained model are required in the final inference pipeline.

Full explanation: `TECHNICAL_REPORT.md` (add the supplied file after generating this staging folder).

## Required match data

This repository does not include the restricted match assets.

To reproduce the submission, obtain the authorised dataset from the competition organisers and place the tactical files in:

`data/tactical/`

Expected files:

- `BAR-ATH_tactical.mp4`
- `BAR-ATH_tactical_atd.xml`
- `BAR-ATH_tactical_atd.txt`
- `BAR-ATH_tactical_homography.csv`
- `BAR-ATH_tactical_smart_tagging.xml`

Alternatively, set the `MTAH_DATA_DIR` environment variable to the directory containing the `tactical/` folder.

For Windows PowerShell:

```powershell
$env:MTAH_DATA_DIR = "C:\path\to\licensed-data"
```

Install dependencies from the repository root:

```powershell
python -m pip install -r requirements.txt
```

Generate the possession predictions:

```powershell
python -m my_scripts.possession_v4
```

Validate the output:

```powershell
python evaluation/validate_submission.py evaluation/results/possession_v4.csv
```

## Source files collected automatically

  - `evaluation/possession_metrics.py`
  - `evaluation/validate_submission.py`
  - `games.py`
  - `LICENSE`
  - `my_scripts/boundary_features.py`
  - `my_scripts/possession_v2.py`
  - `my_scripts/possession_v3.py`
  - `my_scripts/possession_v4.py`
  - `my_scripts/tag_features.py`
  - `my_scripts/tracking_quality.py`
  - `starter/baseline.py`
  - `starter/load_smart_tagging.py`

## Limitations

Tracking can miss the ball or assign wrong objects; nearest-player is not confirmed possession; Smart Tagging events can be imperfect and are phases rather than true possession intervals. Distinguishing live play from dead ball without a visible ball remains challenging. This is a rule-based submission, not a claim of validated full-match accuracy.

## Attribution

Built for [Metrica Sports - More than a Hack 2027](https://github.com/metrica-sports/more-than-a-hack-2027). Any copied starter files retain their original licensing; see `LICENSE` where applicable.
