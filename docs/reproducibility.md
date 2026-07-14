# Reproducibility scope

## Level currently supported

The repository reproduces the published regression and LOOCV metrics from the
processed 19-run experimental summary.

## Level pending raw-data publication

Full end-to-end reproduction requires:

1. original time-series signals for Fc, Ff and Fp;
2. sampling frequency and acquisition metadata;
3. exact file-to-experiment mapping;
4. confirmation of the 10% initial and 10% final trimming rule;
5. exact covariance and numerical-inversion conventions;
6. scripts used to generate all manuscript figures.

## Numerical conventions in the template

- Sample covariance uses `ddof=1`.
- Eigenvalues are ordered from largest to smallest.
- Semiaxes are the square roots of eigenvalues; a confidence multiplier does
  not change the reported axis ratios.
- Mahalanobis distance uses the Moore-Penrose pseudoinverse by default.
- No covariance regularization is applied unless explicitly requested.
