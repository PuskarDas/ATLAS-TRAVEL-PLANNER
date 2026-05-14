"""Train and evaluate a baseline destination rating regressor."""

from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "processed" / "travel_preferences.csv"
REPORT = ROOT / "data" / "processed" / "metrics.txt"


def train() -> dict[str, float]:
    data = pd.read_csv(DATASET)
    features = data.drop(columns=["rating"])
    target = data["rating"]
    categorical = ["destination"]
    numeric = [column for column in features.columns if column not in categorical]

    model = Pipeline(
        steps=[
            (
                "preprocess",
                ColumnTransformer(
                    transformers=[
                        (
                            "category",
                            OneHotEncoder(handle_unknown="ignore"),
                            categorical,
                        ),
                        ("numeric", StandardScaler(), numeric),
                    ]
                ),
            ),
            ("regressor", RandomForestRegressor(n_estimators=80, random_state=42)),
        ]
    )
    x_train, x_test, y_train, y_test = train_test_split(
        features, target, test_size=0.2, random_state=42
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return {
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": mean_squared_error(y_test, predictions, squared=False),
        "r2": r2_score(y_test, predictions),
    }


def main() -> None:
    metrics = train()
    REPORT.write_text(
        "\n".join(f"{key}: {value:.4f}" for key, value in metrics.items()),
        encoding="utf-8",
    )
    print(metrics)


if __name__ == "__main__":
    main()
