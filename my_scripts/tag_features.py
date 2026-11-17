
import numpy as np

TEAM_INDEX = {
    "Barcelona": 0,
    "Atletic Club": 1,
}

ATTACK_CODES = {
    "BUILD UP",
    "PROGRESSION",
    "ATTACKING TRANSITION",
}


def build_tag_votes(events, n_frames):
    # Column 0 = evidence for home
    # Column 1 = evidence for away
    votes = np.zeros((n_frames, 2), dtype=np.int16)

    for event in events:
        code = event["code"]
        team = event["tags"].get("Team")

        if code not in ATTACK_CODES:
            continue

        if team not in TEAM_INDEX:
            continue

        start = max(0, event["start_frame"])
        end = min(n_frames, event["end_frame"])

        if start < end:
            votes[start:end, TEAM_INDEX[team]] += 1

    return votes


if __name__ == "__main__":
    # Synthetic events: no real match data
    example = [
        {
            "code": "BUILD UP",
            "start_frame": 2,
            "end_frame": 5,
            "tags": {"Team": "Barcelona"},
        },
        {
            "code": "PROGRESSION",
            "start_frame": 4,
            "end_frame": 7,
            "tags": {"Team": "Atletic Club"},
        },
    ]

    votes = build_tag_votes(example, 8)

    assert votes[2].tolist() == [1, 0]
    assert votes[4].tolist() == [1, 1]
    assert votes[7].tolist() == [0, 0]

    print("Synthetic tag test passed!")
