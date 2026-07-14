from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import LeaveOneOut, cross_val_predict


MODEL_COLUMNS = ("a_over_b", "dM_x_b_over_c")


def prepare_model_data(df: pd.DataFrame) -> pd.DataFrame:
    required = {"a_over_b", "b_over_c", "dM", "Ra"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise KeyError(f"Missing columns: {missing}")

    out = df.copy()
    out["dM_x_b_over_c"] = out["dM"] * out["b_over_c"]
    return out


def fit_published_model(df: pd.DataFrame):
    """Fit Ra ~ (a/b) + dM*(b/c) using ordinary least squares."""
    prepared = prepare_model_data(df)
    x = sm.add_constant(prepared[list(MODEL_COLUMNS)], has_constant="add")
    return sm.OLS(prepared["Ra"], x).fit()


def loocv_metrics(df: pd.DataFrame) -> tuple[dict[str, float], np.ndarray]:
    """Return LOOCV R², MAE, RMSE and out-of-fold predictions."""
    prepared = prepare_model_data(df)
    x = prepared[list(MODEL_COLUMNS)].to_numpy(dtype=float)
    y = prepared["Ra"].to_numpy(dtype=float)

    predictions = cross_val_predict(
        LinearRegression(),
        x,
        y,
        cv=LeaveOneOut(),
    )
    metrics = {
        "R2_LOOCV": float(r2_score(y, predictions)),
        "MAE_LOOCV": float(mean_absolute_error(y, predictions)),
        "RMSE_LOOCV": float(np.sqrt(mean_squared_error(y, predictions))),
    }
    return metrics, predictions
