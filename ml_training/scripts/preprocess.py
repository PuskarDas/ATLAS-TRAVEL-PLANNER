"""Create a small synthetic training dataset for the travel recommender."""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


def build_dataset(rows: int = 250) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    destinations = np.array(["Paris", "Tokyo", "Bali", "New York", "Barcelona"])
    data = pd.DataFrame(
        {
            "destination": rng.choice(destinations, rows),
            "budget": rng.integers(500, 5000, rows),
            "duration_days": rng.integers(2, 15, rows),
            "group_size": rng.integers(1, 8, rows),
            "interest_beach": rng.integers(0, 2, rows),
            "interest_culture": rng.integers(0, 2, rows),
            "interest_food": rng.integers(0, 2, rows),
            "interest_adventure": rng.integers(0, 2, rows),
        }
    )
    destination_boost = data["destination"].map(
        {"Paris": 0.7, "Tokyo": 0.65, "Bali": 0.8, "New York": 0.58, "Barcelona": 0.72}
    )
    interest_score = data[
        ["interest_beach", "interest_culture", "interest_food", "interest_adventure"]
    ].mean(axis=1)
    budget_fit = np.clip(data["budget"] / 5000, 0, 1)
    data["rating"] = np.round(
        2.5 + destination_boost + interest_score + budget_fit, 2
    ).clip(1, 5)
    return data


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    dataset = build_dataset()
    output = PROCESSED / "travel_preferences.csv"
    dataset.to_csv(output, index=False)
    print(f"Wrote {len(dataset)} rows to {output}")


if __name__ == "__main__":
    main()
