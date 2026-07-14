"""Tools for covariance-ellipsoid features from machining-force signals."""

from .ellipsoid_features import compute_ellipsoid_features, trim_signal
from .modeling import fit_published_model, loocv_metrics

__all__ = [
    "compute_ellipsoid_features",
    "trim_signal",
    "fit_published_model",
    "loocv_metrics",
]
