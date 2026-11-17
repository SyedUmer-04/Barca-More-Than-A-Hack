
import numpy as np

from starter.baseline import (
    build, smooth, write_submission,
    HOME, AWAY, NOBODY
)
from starter.load_smart_tagging import load
from my_scripts.tag_features import build_tag_votes


def apply_tag_evidence(raw, votes):
    """Use team tags only when tracking has no answer."""

    result = raw.copy()

    missing = raw == NOBODY

    # Evidence exclusively supports home
    home_only = (votes[:, 0] > 0) & (votes[:, 1] == 0)

    # Evidence exclusively supports away
    away_only = (votes[:, 1] > 0) & (votes[:, 0] == 0)

    result[missing & home_only] = HOME
    result[missing & away_only] = AWAY

    return result


def test_with_fake_data():
    """Test logic without using the real match."""

    raw = np.array([HOME, NOBODY, NOBODY, NOBODY, AWAY])

    votes = np.array([
        [0, 1],
        [1, 0],
        [0, 1],
        [1, 1],
        [1, 0],
    ])

    result = apply_tag_evidence(raw, votes)

    expected = np.array([
        HOME, HOME, AWAY, NOBODY, AWAY
    ])

    assert np.array_equal(result, expected)
    print("Synthetic test passed!")


def main():
    test_with_fake_data()

    # Existing baseline predictions
    raw = build()

    # Automatic Smart Tagging events
    events = load()

    # Convert events to home/away evidence
    votes = build_tag_votes(events, len(raw))

    # Improve predictions where tracking is missing
    improved = apply_tag_evidence(raw, votes)

    # Apply original baseline smoothing
    labels = smooth(improved, 50)

    # Save a new CSV
    write_submission(
        "evaluation/results/possession_v2.csv",
        labels
    )

    print("V2 generated successfully!")


if __name__ == "__main__":
    main()
