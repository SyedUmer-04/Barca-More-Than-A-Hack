import math

FPS = 25

def parse_ball_xy(ball_text):
    x_str, y_str = ball_text.split(",")[:2]
    x = float(x_str)
    y = float(y_str)
    return x, y

def is_visible(ball_text):
    x, y = parse_ball_xy(ball_text)
    return math.isfinite(x) and math.isfinite(y)

def is_outside(ball_text, margin=0.005):
    x, y = parse_ball_xy(ball_text)

    if not (math.isfinite(x) and math.isfinite(y)):
        return False

    return (
        x < -margin or x > 1 + margin
        or y < -margin or y > 1 + margin
    )

def find_true_runs(flags):
    """
    Return list of (start, end) inclusive for consecutive True runs.
    """
    runs = []
    start = None

    for i, flag in enumerate(flags):
        if flag and start is None:
            start = i
        elif not flag and start is not None:
            runs.append((start, i - 1))
            start = None

    if start is not None:
        runs.append((start, len(flags) - 1))

    return runs

def build_outside_flags(ball_texts, margin=0.005):
    return [is_outside(ball, margin=margin) for ball in ball_texts]

def build_dead_ball_candidates(ball_texts, margin=0.005, min_run=25):
    """
    Mark frames as dead-ball candidates if the ball is outside
    for a sustained run of at least min_run frames.
    """
    outside = build_outside_flags(ball_texts, margin=margin)
    candidates = [False] * len(outside)

    for start, end in find_true_runs(outside):
        run_len = end - start + 1
        if run_len >= min_run:
            for i in range(start, end + 1):
                candidates[i] = True

    return candidates

def test_synthetic():
    # visible inside / outside toy example
    ball_texts = [
        "0.50,0.50",   # inside
        "1.02,0.40",   # outside
        "1.03,0.41",   # outside
        "1.04,0.42",   # outside
        "0.80,0.40",   # inside
        "NaN,NaN",     # missing
        "-0.02,0.50",  # outside
        "-0.03,0.51",  # outside
    ]

    outside = build_outside_flags(ball_texts, margin=0.005)
    assert outside == [False, True, True, True, False, False, True, True]

    runs = find_true_runs(outside)
    assert runs == [(1, 3), (6, 7)]

    dead = build_dead_ball_candidates(ball_texts, margin=0.005, min_run=3)
    assert dead == [False, True, True, True, False, False, False, False]

    print("Synthetic boundary test passed!")

if __name__ == "__main__":
    test_synthetic()