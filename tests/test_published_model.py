from pathlib import Path

import pandas as pd
import pytest

from machining_ellipsoids.modeling import fit_published_model, loocv_metrics


ROOT = Path(__file__).resolve().parents[1]


def test_published_model_reproduces_reported_results():
    df = pd.read_csv(ROOT / "data" / "processed" / "experiment_summary.csv")
    model = fit_published_model(df)
    metrics, _ = loocv_metrics(df)

    assert model.params["const"] == pytest.approx(-1.758970, abs=1e-5)
    assert model.params["a_over_b"] == pytest.approx(0.531757, abs=1e-5)
    assert model.params["dM_x_b_over_c"] == pytest.approx(0.007408, abs=1e-6)
    assert model.rsquared_adj == pytest.approx(0.946274, abs=1e-5)
    assert metrics["R2_LOOCV"] == pytest.approx(0.929371, abs=1e-5)
    assert metrics["MAE_LOOCV"] == pytest.approx(0.339360, abs=1e-5)
    assert metrics["RMSE_LOOCV"] == pytest.approx(0.403975, abs=1e-5)
