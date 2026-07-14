# Covariance Ellipsoids of Machining Forces for Surface-Roughness Modeling

Reproducibility repository for the study:

**“Multivariate Ellipsoidal Representations of Machining Forces for Surface-Roughness Modeling in Ti-6Al-4V Turning.”**

The study uses a 19-run central composite design, three-component machining-force signals, covariance ellipsoids, geometric descriptors, and multiple linear regression to model average surface roughness (`Ra`) in dry turning of Ti-6Al-4V.

## End-to-end reproduced model

Using the original force signals and the full numerical precision of the extracted features, the repository reproduces:

```text
Ra = -1.758866 + 0.531748(a/b) + 0.00740784[dM × (b/c)]
```

The coefficients reported from the rounded manuscript table are nearly identical:

```text
Ra = -1.758970 + 0.531757(a/b) + 0.007408[dM × (b/c)]
```

Expected end-to-end validation results:

| Metric | Value |
|---|---:|
| Adjusted R² | 0.9463 |
| LOOCV R² | 0.9294 |
| LOOCV MAE | 0.3394 |
| LOOCV RMSE | 0.4040 |

## Main notebook

```text
notebooks/00_metodologia_reprodutivel_dados_reais.ipynb
```

The notebook:

1. reads the original workbook containing all 19 force signals;
2. removes the first and last 10% of each experiment;
3. calculates the 3D covariance matrix and eigendecomposition;
4. extracts `a/b`, `b/c`, and Mahalanobis distance;
5. verifies the results against the original model-input workbook;
6. fits the OLS model and performs leave-one-out cross-validation;
7. exports coefficients, predictions, figures, and a reproducibility summary.

The maximum differences between the recalculated features and the original reference workbook are below `1e-9`.

## Repository structure

```text
.
├── data/
│   ├── raw/Forcas_C50_R08.xlsx
│   ├── metadata/DOE_titanio_C50_R08_CCD.xlsx
│   ├── validation/teste_OLS_referencia.xlsx
│   └── processed/experiment_summary.csv
├── notebooks/
│   ├── 00_metodologia_reprodutivel_dados_reais.ipynb
│   ├── 00_metodologia_resumida.ipynb
│   ├── 01_reproduce_published_model.ipynb
│   └── 02_extract_ellipsoid_features_template.ipynb
├── src/machining_ellipsoids/
├── scripts/
├── tests/
├── figures/
├── results/
└── CITATION.cff
```

## Quick start

```bash
python -m venv .venv
```

Activate the environment:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# Linux/macOS
source .venv/bin/activate
```

Install dependencies and open the main notebook:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
jupyter lab notebooks/00_metodologia_reprodutivel_dados_reais.ipynb
```

Run automated tests:

```bash
pytest
```

## Data status

The raw force-signal workbook, DOE metadata, and validation workbook are included in this package. Before making the repository public, all coauthors should confirm that public distribution is authorized.

## Citation

Update `CITATION.cff` with the final GitHub URL, DOI, ORCIDs, publication status, and conference metadata. After creating a release, archive it in Zenodo to obtain a DOI.

## Licenses

- Source code: MIT License.
- Processed data and original repository documentation: CC BY 4.0.
- Raw signals, manuscript, publisher layout, and third-party figures are excluded from those licenses unless explicitly approved and stated otherwise.

## Authors

- Gabriel V. de Lima
- Marlon M. de Oliveira
- Mirelli de C. Cesário
- Paulo H. S. Campos
- Anderson P. de Paiva

Universidade Federal de Itajubá — UNIFEI, Brazil.
