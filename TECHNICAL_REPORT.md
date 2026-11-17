# Ball Possession Estimation from Automatic Tracking and Tactical Tags

**More Than a Hack 2027 — Phase 1 | Technical Report | Submitted method: V4**

## 1. Problem and objective

The objective is to predict one of four framewise states for the tactical match video: `H` (home-team possession), `A` (away-team possession), `D` (dead ball), or `X` (uncertain/outside the labelled period). The submission contains 199,319 consecutive zero-based video-frame labels. The system is deterministic and rule-based; its purpose is to combine incomplete automatic ball tracking, team proximity, automated tactical tags and temporal consistency into a possession sequence.

The final submission method described here is **V4**. Later experiments with independent video ball detectors, long-gap trajectory hypotheses and tag-driven V5 overlays were investigated but are **not part of the submitted V4 inference pipeline**.

## 2. Data sources and scope

- **Tactical Automatic Tracking Data (ATD):** FIFA/EPTS raw player and ball observations and tracking metadata, including the team corresponding to each temporary track slot. Normalized pitch positions are converted to physical distances using the pitch dimensions provided in the starter project.
- **Smart Tagging:** Automatic, time-aligned tactical phases and set-piece annotations. Attacking, defending and restart evidence is treated as potentially noisy evidence, **not** ground-truth possession.
- **Tactical video:** Used locally for qualitative debugging and understanding tracking failures. The final V4 inference path does not require an independently trained video ball detector.
- **Not used by the submitted V4 method:** Broadcast-video timeline, separately trained YOLO ball detectors, exploratory player-anchor methods, or V5 dead-ball overrides. Homography was an exploratory visualization resource, not a required V4 prediction feature.

The organisers provide the match assets under restricted licence. The public code repository contains source code and documentation, not match recordings, tracking exports, tag extracts, generated framewise predictions, or other restricted assets.

## 3. Implemented inference pipeline (V4)

1. **Align frames and identify teams.** Work in the 0-based tactical-video frame index. Read tracking-slot team assignments from the provided ATD metadata; track slots are not assumed to be permanent player identities.
2. **Tracking-based possession evidence.** Where a finite ball observation and valid players exist, derive a candidate team from the nearest tracked player using distance measured in pitch metres. Proximity is treated as a heuristic rather than proof of a touch.
3. **Missing observations and continuity.** Where the ball is not observed, apply the existing possession-continuity/smoothing logic and supporting evidence from available automatic Smart Tagging phases. Short-gap reconstruction was studied separately; long gaps are not filled with invented exact ball coordinates in V4.
4. **Boundary and stoppage evidence.** Treat sustained out-of-pitch ball observations as possible dead-ball evidence, rather than using isolated outliers. The implemented boundary heuristic requires a sustained run before forcing the `D` state.
5. **Ball-quality filtering.** Reject isolated implausible one-frame ball-coordinate spikes (teleport-like artifacts) before letting them influence the possession state.
6. **Temporal regularisation and export.** Apply the implemented smoothing/continuity stages to reduce rapid state flicker, then write exactly one label per tactical-video frame in `frame,label` order.

The implementation is contained in `my_scripts/possession_v4.py` and its imported project modules. The repository code is the authority for exact ordering and numerical parameters; no manual per-frame label corrections are part of inference.

## 4. Development methodology and training data

**Training data:** None. V4 does not fit a supervised classifier to human-labelled examples, does not use hand-labelled annotations from the provided match, and does not need a private trained model. The automatically generated tactical tags are inputs, not possession labels.

Development checks used synthetic examples and automatically hidden subsets of existing ATD observations to probe reconstruction and team-proxy hypotheses. These are algorithmic diagnostics, not human-labelled possession ground truth. The organisers' public five-minute reference was reserved for pipeline alignment/format checking, **not** model training, parameter tuning or choosing among submissions.

Exploratory comparisons showed the practical limitation of long-gap interpolation: even when a line between observed endpoints beats holding the last position, it need not represent the real route through multiple passes or interceptions. Candidate player-interaction and movement-aware rules were therefore not promoted to V4. Similarly, experimental V5 tag overlays were not promoted because their effect on true possession-spell accuracy was unverified.

## 5. Possession decisions and key limitations

- **Loose balls, duels and player proximity:** The nearest player is a weak proxy. A player may be closest without controlling the ball; observed positions can be missing or erroneous. The approach favours continuity over instant reassignments when observations are unreliable.
- **Missing ball:** Ball absence is not synonymous with `D`; a goalkeeper holding the ball or a crowded challenge may be live play. Long occlusions remain a major source of uncertainty.
- **Restarts and stoppages:** Smart Tagging set-piece intervals indicate possible restart context but do not reveal an exact whistle frame or the full duration of a dead-ball period. Sustained boundary evidence is used conservatively.
- **Temporary track identities:** ATD track slots can be reassigned, preventing robust long-term player identification without additional tracking logic.
- **Temporal segmentation:** Smoothing reduces flicker but can delay genuine turnovers, merge separate possessions or leave fragmented possession spells. Framewise classification quality and possession-spell quality are distinct.

**With more time:** Independently validate stoppage boundaries with permitted external footage or properly licensed labels from other matches; improve event-to-state timing; use a probabilistic temporal model with explicit uncertainty; and assess generalisation on independent matches.

## 6. Reproduction and output contract

1. Clone the submitted **public code repository** and install its pinned `requirements.txt` using Python.
2. Obtain the restricted match bundle directly from the organisers, without redistributing it. Place it in a local `data/` folder with `tactical/` subdirectory, or set `MTAH_DATA_DIR` accordingly.
3. Run the actual V4 entry point from the repository root: `python -m my_scripts.possession_v4`
4. Validate the resulting CSV using `python evaluation/validate_submission.py evaluation/results/possession_v4.csv`
5. Confirm `frame,label` header; precisely 199,319 rows indexed `0` through `199318`; labels only `H`, `A`, `D` or `X`; no blank values.

The submission CSV is uploaded separately to the organisers' form. It should not be published in the source repository, nor should any original or derived restricted match assets.

## References

- Official project repository: https://github.com/metrica-sports/more-than-a-hack-2027
- Submission specification: https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/SUBMISSION.md
- Dataset description: https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/DATA.md
- Rules and evaluation: https://github.com/metrica-sports/more-than-a-hack-2027/blob/main/RULES.md
