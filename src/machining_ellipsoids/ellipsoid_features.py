from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class EllipsoidFeatures:
    centroid: np.ndarray
    covariance: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    semiaxes: np.ndarray
    a_over_b: float
    b_over_c: float
    mahalanobis_to_origin: float

    def as_dict(self) -> dict[str, float]:
        return {
            "centroid_Fc": float(self.centroid[0]),
            "centroid_Ff": float(self.centroid[1]),
            "centroid_Fp": float(self.centroid[2]),
            "a": float(self.semiaxes[0]),
            "b": float(self.semiaxes[1]),
            "c": float(self.semiaxes[2]),
            "a_over_b": self.a_over_b,
            "b_over_c": self.b_over_c,
            "dM": self.mahalanobis_to_origin,
        }


def trim_signal(
    data: pd.DataFrame | np.ndarray,
    start_fraction: float = 0.10,
    end_fraction: float = 0.10,
) -> pd.DataFrame | np.ndarray:
    """Remove initial and final transient fractions from a force signal."""
    if not 0 <= start_fraction < 1 or not 0 <= end_fraction < 1:
        raise ValueError("Fractions must be in [0, 1).")
    if start_fraction + end_fraction >= 1:
        raise ValueError("The retained signal must contain at least one sample.")

    n = len(data)
    if n < 3:
        raise ValueError("At least three samples are required.")

    i0 = int(np.floor(n * start_fraction))
    i1 = n - int(np.floor(n * end_fraction))
    return data.iloc[i0:i1].copy() if isinstance(data, pd.DataFrame) else data[i0:i1].copy()


def compute_ellipsoid_features(
    forces: pd.DataFrame | np.ndarray,
    columns: Iterable[str] = ("Fc", "Ff", "Fp"),
    regularization: float = 0.0,
    rcond: float = 1e-12,
) -> EllipsoidFeatures:
    """Compute 3D covariance-ellipsoid descriptors.

    Parameters
    ----------
    forces:
        DataFrame containing Fc, Ff and Fp, or an array with shape (n, 3).
    columns:
        Force-column names when ``forces`` is a DataFrame.
    regularization:
        Optional diagonal value added to the covariance matrix.
    rcond:
        Relative cutoff used by the Moore-Penrose pseudoinverse.

    Notes
    -----
    Semiaxes are proportional to the square roots of covariance eigenvalues.
    Ratios are therefore independent of the selected confidence multiplier.
    The Mahalanobis distance is computed from the ellipsoid centroid to the origin.
    """
    if isinstance(forces, pd.DataFrame):
        col_list = list(columns)
        missing = [c for c in col_list if c not in forces.columns]
        if missing:
            raise KeyError(f"Missing force columns: {missing}")
        x = forces[col_list].to_numpy(dtype=float)
    else:
        x = np.asarray(forces, dtype=float)

    if x.ndim != 2 or x.shape[1] != 3:
        raise ValueError("forces must have shape (n_samples, 3).")
    if x.shape[0] < 4:
        raise ValueError("At least four observations are required.")
    if not np.isfinite(x).all():
        raise ValueError("forces contains NaN or infinite values.")
    if regularization < 0:
        raise ValueError("regularization must be non-negative.")

    centroid = x.mean(axis=0)
    covariance = np.cov(x, rowvar=False, ddof=1)
    if regularization:
        covariance = covariance + regularization * np.eye(3)

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = np.clip(eigenvalues[order], 0.0, None)
    eigenvectors = eigenvectors[:, order]
    semiaxes = np.sqrt(eigenvalues)

    eps = np.finfo(float).eps
    a_over_b = float(semiaxes[0] / max(semiaxes[1], eps))
    b_over_c = float(semiaxes[1] / max(semiaxes[2], eps))

    covariance_inv = np.linalg.pinv(covariance, rcond=rcond)
    d2 = float(centroid @ covariance_inv @ centroid)
    mahalanobis = float(np.sqrt(max(d2, 0.0)))

    return EllipsoidFeatures(
        centroid=centroid,
        covariance=covariance,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        semiaxes=semiaxes,
        a_over_b=a_over_b,
        b_over_c=b_over_c,
        mahalanobis_to_origin=mahalanobis,
    )
