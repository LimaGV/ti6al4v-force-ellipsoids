from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from machining_ellipsoids.modeling import (
    fit_published_model,
    loocv_metrics,
    prepare_model_data,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "experiment_summary.csv"
RESULTS_DIR = ROOT / "results"


def main() -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    prepared = prepare_model_data(df)
    model = fit_published_model(df)
    cv_metrics, cv_predictions = loocv_metrics(df)

    metrics = {
        "R2": float(model.rsquared),
        "R2_adjusted": float(model.rsquared_adj),
        **cv_metrics,
    }

    coefficients = model.params.rename("coefficient").reset_index()
    coefficients.columns = ["term", "coefficient"]
    coefficients.to_csv(RESULTS_DIR / "model_coefficients.csv", index=False)

    pred_df = prepared[
        ["experiment", "a_over_b", "b_over_c", "dM", "dM_x_b_over_c", "Ra"]
    ].copy()
    pred_df["Ra_fitted"] = model.predict()
    pred_df["Ra_LOOCV"] = cv_predictions
    pred_df.to_csv(RESULTS_DIR / "model_predictions.csv", index=False)

    with (RESULTS_DIR / "model_metrics.json").open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(pred_df["Ra"], pred_df["Ra_LOOCV"])
    lower = min(pred_df["Ra"].min(), pred_df["Ra_LOOCV"].min())
    upper = max(pred_df["Ra"].max(), pred_df["Ra_LOOCV"].max())
    ax.plot([lower, upper], [lower, upper])
    ax.set_xlabel("Observed Ra")
    ax.set_ylabel("LOOCV-predicted Ra")
    ax.set_title("Observed versus LOOCV-predicted surface roughness")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "observed_vs_loocv.png", dpi=300)
    plt.close(fig)

    print(model.summary())
    print("\nLOOCV metrics")
    for key, value in metrics.items():
        print(f"{key}: {value:.6f}")


if __name__ == "__main__":
    main()
