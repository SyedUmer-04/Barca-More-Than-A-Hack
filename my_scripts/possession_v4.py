
import numpy as np

from games import asset_paths
from starter.baseline import (
    build, smooth, write_submission, NOBODY
)
from starter.load_smart_tagging import load

from my_scripts.tracking_quality import detect_ball_spikes
from my_scripts.tag_features import build_tag_votes
from my_scripts.possession_v2 import apply_tag_evidence
from my_scripts.boundary_features import build_dead_ball_candidates
from my_scripts.possession_v3 import apply_dead_ball_candidates


def remove_unreliable_predictions(raw, suspicious):
    result = raw.copy()
    result[suspicious] = NOBODY
    return result


def test_synthetic():
    raw = np.array([0, 0, 1, 1])
    suspicious = np.array([False, False, True, False])

    result = remove_unreliable_predictions(raw, suspicious)

    assert result.tolist() == [0, 0, -1, 1]
    print("Synthetic V4 test passed!")


def main():
    test_synthetic()

    # 1. Read ball positions
    ball_texts = []
    ball_xy = []

    with open(asset_paths()["atd_raw"]) as file:
        for line in file:
            ball = line.strip().split(":")[-1]
            ball_texts.append(ball)

            values = ball.split(",")
            ball_xy.append([
                float(values[0]),
                float(values[1])
            ])

    ball_xy = np.asarray(ball_xy, dtype=float)

    # 2. Identify suspicious ball detections
    suspicious = detect_ball_spikes(ball_xy)

    # 3. Generate original tracking predictions
    raw = build()

    if len(raw) != len(suspicious):
        raise ValueError("Frame counts do not match")

    # 4. Ignore suspicious tracking observations
    cleaned = remove_unreliable_predictions(raw, suspicious)

    # 5. Add Smart Tagging evidence
    events = load()
    votes = build_tag_votes(events, len(cleaned))

    improved = apply_tag_evidence(cleaned, votes)

    # 6. Smooth predictions
    labels = smooth(improved, 50)

    # 7. Apply boundary evidence
    candidates = np.asarray(
        build_dead_ball_candidates(
            ball_texts,
            margin=0.005,
            min_run=25
        ),
        dtype=bool
    )

    candidates[suspicious] = False

    labels = apply_dead_ball_candidates(labels, candidates)

    # 8. Save result
    write_submission(
        "evaluation/results/possession_v4.csv",
        labels
    )

    print("V4 generated successfully!")


if __name__ == "__main__":
    main()
