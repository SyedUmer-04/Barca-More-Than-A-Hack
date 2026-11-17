
import numpy as np

PITCH_LENGTH = 105.3
PITCH_WIDTH = 68.0


def detect_ball_spikes(
    ball_xy,
    jump_m=10.0,
    recovery_m=3.0
):
    """
    Detect isolated, suspicious ball-position jumps.

    ball_xy: Nx2 normalized pitch coordinates.

    A point is suspicious when:
    1. Its neighbours are close to each other.
    2. The middle position is far from both.

    Returns one boolean per frame.
    """
    xy = np.asarray(ball_xy, dtype=float)

    if xy.ndim != 2 or xy.shape[1] != 2:
        raise ValueError("Expected Nx2 coordinates")

    suspicious = np.zeros(len(xy), dtype=bool)

    scale = np.array([PITCH_LENGTH, PITCH_WIDTH])

    for i in range(1, len(xy) - 1):
        prev = xy[i - 1]
        curr = xy[i]
        next_ = xy[i + 1]

        if not np.isfinite(
            [*prev, *curr, *next_]
        ).all():
            continue

        jump_before = np.linalg.norm(
            (curr - prev) * scale
        )

        jump_after = np.linalg.norm(
            (next_ - curr) * scale
        )

        recovery = np.linalg.norm(
            (next_ - prev) * scale
        )

        if (
            jump_before > jump_m
            and jump_after > jump_m
            and recovery < recovery_m
        ):
            suspicious[i] = True

    return suspicious


def test_synthetic():
    ball = np.array([
        [0.50, 0.50],
        [0.51, 0.50],
        [0.90, 0.50],  # Suspicious
        [0.52, 0.50],
        [np.nan, np.nan],
    ])

    result = detect_ball_spikes(ball)

    assert result.tolist() == [
        False, False, True, False, False
    ]

    print("Synthetic tracking-quality test passed!")


if __name__ == "__main__":
    test_synthetic()
