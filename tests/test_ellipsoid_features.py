import numpy as np

from machining_ellipsoids.ellipsoid_features import compute_ellipsoid_features


def test_features_are_finite_for_well_conditioned_signal():
    rng = np.random.default_rng(42)
    covariance = np.diag([9.0, 4.0, 1.0])
    forces = rng.multivariate_normal([20.0, 10.0, 5.0], covariance, size=2000)

    features = compute_ellipsoid_features(forces)

    assert np.isfinite(features.semiaxes).all()
    assert features.a_over_b > 1.0
    assert features.b_over_c > 1.0
    assert features.mahalanobis_to_origin > 0.0
