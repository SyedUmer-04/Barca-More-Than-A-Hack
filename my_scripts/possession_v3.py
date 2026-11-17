
import numpy as np

from games import asset_paths
from starter.baseline import build, smooth, write_submission
from starter.load_smart_tagging import load

from my_scripts.tag_features import build_tag_votes
from my_scripts.possession_v2 import apply_tag_evidence
from my_scripts.boundary_features import build_dead_ball_candidates


def apply_dead_ball_candidates(labels, candidates):
    """Override predicted labels only at candidate dead-ball frames."""

    result = np.asarray(labels).copy()
    mask = np.asarray(candidates, dtype=bool)

    if result.shape != mask.shape:
        raise ValueError("Labels and candidate lengths differ")

    result[mask] = "D"
    return result


def test_synthetic():
    labels = np.array(["H", "H", "A", "A", "D"])
    candidates = [False, True, False, True, False]

    result = apply_dead_ball_candidates(labels, candidates)

    expected = np.array(["H", "D", "A", "D", "D"])

    assert np.array_equal(result, expected)
    print("Synthetic V3 test passed!")


def main():
    test_synthetic()

    # Step 1: Get baseline predictions
    raw = build()

    # Step 2: Generate Smart Tagging evidence
    events = load()
    votes = build_tag_votes(events, len(raw))

    # Step 3: Apply Smart Tagging
    improved = apply_tag_evidence(raw, votes)

    # Step 4: Apply baseline smoothing
    labels = smooth(improved, 50)

    # Step 5: Load ball positions
    with open(asset_paths()["atd_raw"], encoding="utf-8") as file:
        ball_texts = [
            line.strip().split(":")[-1]
            for line in file
        ]

    # Step 6: Find sustained outside-pitch runs
    candidates = build_dead_ball_candidates(
        ball_texts,
        margin=0.005,
        min_run=25
    )

    # Step 7: Apply boundary evidence
    labels = apply_dead_ball_candidates(labels, candidates)

    # Step 8: Save CSV
    path = write_submission(
        "evaluation/results/possession_v3.csv",
        labels
    )

    print("V3 generated successfully!")
    print("Saved:", path)


if __name__ == "__main__":
    main()
