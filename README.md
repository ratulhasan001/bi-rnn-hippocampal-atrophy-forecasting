# Biology-Informed Recurrent Neural Networks for Longitudinal Hippocampal Atrophy Forecasting in Alzheimer's Disease

Code for our two-semester group undergraduate thesis (CSE-4000) in Computer Science and Engineering at Bangladesh Army University of Engineering & Technology (BAUET), completed in July 2026. The work forecasts a subject's next hippocampal volume from their earlier MRI scans in ADNI-1 (382 subjects, 1,957 scans), and tests whether a "biology-informed" loss that penalises biologically implausible forecasts (volume growth, or faster loss than a set annual rate) helps recurrent neural networks (GRU, LSTM, Bi-LSTM).

The repository contains no ADNI data. To run the code you need your own approved ADNI access (see [Data](#data)).

## Contents

| Path | What it is |
|---|---|
| [01_thesis_pipeline.ipynb](01_thesis_pipeline.ipynb) | The thesis pipeline as run on Google Colab (GPU): builds a subject-level split from the organised ADNI scans, trains 3D-CNN/ResNet + GRU/LSTM classifiers (CN / MCI / AD), segments the hippocampus with FastSurfer, extracts hippocampal volumes, and runs the first forecasting experiments on a single 80/20 subject split. |
| [02_bi_rnn_forecasting_cv.ipynb](02_bi_rnn_forecasting_cv.ipynb) | The latest and complete forecasting analysis (September 2026). Starts from the volume table, evaluates every model with repeated subject-level cross-validation, and writes all tables and figures in `results/`. Runs locally on a CPU. |
| [results/](results) | Output of notebook 02: aggregate tables (`tables/*.csv`, `*.tex`), figures (`figures/*.png`, `*.pdf`), `RESULTS_SUMMARY.md` and `paper_numbers.json` (every reported number, with the configuration and package versions). |
| [figures/](figures) | Diagrams of the BI-RNN framework and of the biological corridor loss (draw.io sources and PNG exports). |
| [scripts/plot_baseline_segmentations.py](scripts/plot_baseline_segmentations.py) | Colab script that plots one baseline scan per diagnostic group with its FastSurfer hippocampus mask and volume. |

The raw ADNI downloads were flattened to one file per visit with the companion tool [adni-scan-organizer](https://github.com/ratulhasan001/adni-scan-organizer).

## Pipeline

### 1. Data preparation and volumetry (notebook 01)

1. **Organise the scans.** After [adni-scan-organizer](https://github.com/ratulhasan001/adni-scan-organizer), each subject folder holds `<Visit>.nii` files (`sc`, `m06`, `m12`, …).
2. **Build the image list and split.** Joins every scan with its diagnosis (`Group` column of the ADNI collection CSV, matching `bl` and `sc`), then splits subjects 70 / 15 / 15 into Train / Val / Test so that no subject appears in two splits. Writes `final_dataset_split.csv` (`SubjectID, Visit, FilePath, Diagnosis, Split`).
3. **Classification experiments.** Each subject's scans (up to 6 visits, resized to 96³ with MONAI, random 90° rotations for training) go through a shared 3D CNN or a light 3D ResNet; a GRU or LSTM then reads the per-visit features and predicts CN / MCI / AD. A static 3D CNN on baseline scans is the reference. Training uses class-weighted cross-entropy and Adam.
4. **Hippocampal segmentation.** Runs FastSurfer (`FastSurferCNN.run_prediction`) on every scan and keeps labels 17 and 53 (left and right hippocampus) as a binary mask, `<Visit>_seg.nii.gz`.
5. **Volume extraction.** Counts mask voxels × voxel volume and writes `hippocampal_volumes.csv` (`SubjectID, Visit, Diagnosis, Volume_mm3`).
6. **First forecasting runs.** Uses all earlier scans of a subject to forecast the last one, on one 80/20 subject split. Compares last-observation-carried-forward (LOCF), linear regression, a linear mixed-effects model, ARIMA(1,1,0), XGBoost, standard GRU / LSTM / Bi-LSTM and biology-informed GRU / LSTM. The biology-informed loss is MSE plus λ · mean(ReLU(predicted growth − 1 % of the last volume)²), computed on min-max scaled volumes with λ = 2. The notebook also plots Bland–Altman, residual, Q–Q and trajectory figures.
7. **Figures.** Renders example raw scans and segmentation overlays with nilearn.

### 2. Cross-validated forecasting analysis (notebook 02)

1. **Cohort.** Merges the volume table with the ADNI collection CSV to get scan dates, age and sex (if a visit has several images, the one with the highest Image ID is used). Time is measured in years since the first scan. Visits `sc/bl, m06, m12, m18, m24, m36` are kept.
2. **Tasks.** A forecast window is at least two earlier scans plus the next scan as target. **T1** (primary): forecast each subject's final scan (one target per subject, horizon about 12 months). **T2**: every next-scan forecast.
3. **Evaluation.** 5-fold subject-level cross-validation stratified by diagnosis, repeated 3 times (15 splits). 15 % of the training subjects form an inner validation set used only for early stopping. Hyper-parameters are fixed in advance.
4. **Baselines.** Persistence, population drift, per-subject linear extrapolation, ARIMA(1,1,0), linear mixed-effects models (random intercept and slope; forecasts from the BLUP given the history) with and without covariates (diagnosis × time, age, sex), and XGBoost on history features with and without covariates.
5. **Sequence-only RNNs.** GRU, LSTM and Bi-LSTM read the scaled volume and time of each scan and predict an annual rate of change, so the forecast is anchored to the last scan. Each is trained with MSE (standard) or with the biological corridor loss:
   L = MSE + λ_traj · mean ReLU(Δv)/R + λ_bio · mean ReLU(Δv − τ_noise · v_last)/R + λ_smooth · mean ReLU(−Δv − τ_drop · Δt · v_last)/R,
   with λ = (1, 2, 1), τ_noise = 1 % and τ_drop = 10 %/year. Comparators are post-hoc clipping and a GRU whose output is confined to the corridor by construction.
6. **Hybrid model.** The covariate mixed-effects model supplies a forecast (prior), a subject slope and the residuals of the fitted history. A GRU (or LSTM) reads the scans plus these residuals and static covariates and outputs a correction to the prior. The output layer starts at zero, so training starts from the statistical forecast. Training priors are cross-fitted (each subject's prior comes from a model fitted without that subject). Five networks with different seeds are averaged.
7. **Prediction intervals.** Analytic mixed-effects intervals and split-conformal intervals calibrated on the inner validation subjects.
8. **Statistics.** MAE, RMSE, MAPE, skill vs persistence, correlation of predicted and observed change, growth- and atrophy-violation rates, Bland–Altman bias. Subject-level bootstrap 95 % CIs, paired Wilcoxon tests with Holm correction, and TOST equivalence tests (±5 mm³).
9. **Robustness.** Ablation of each loss term, ablation of the hybrid, λ and τ sensitivity, the earlier absolute-output protocol (as in notebook 01) under the same cross-validation, and all-visit (T2) forecasting.

## Results (notebook 02, T1, mean over 3 repeats)

| Model | MAE (mm³) [95 % CI] | Growth violations |
|---|---|---|
| Persistence | 186.5 [172.3, 201.0] | 0.00 % |
| ARIMA(1,1,0) | 184.4 [171.4, 198.2] | 12.30 % |
| Linear mixed-effects + covariates | 118.2 [107.8, 128.8] | 0.09 % |
| XGBoost + covariates | 124.5 [114.4, 135.1] | 0.09 % |
| Standard GRU | 129.1 [118.6, 139.9] | 0.00 % |
| Bio-Informed GRU | 130.2 [119.2, 141.3] | 0.00 % |
| Hybrid Bio-Informed GRU | 121.0 [110.3, 131.5] | 0.00 % |

- The covariate mixed-effects model had the lowest MAE.
- The corridor loss did not lower the error of the sequence-only RNNs (no Bio-Informed vs Standard difference was significant after Holm correction).
- The hybrid Bio-Informed GRU was statistically equivalent to the covariate mixed-effects model within ±5 mm³ (TOST p = 0.048) and produced no forecasts with more than 1 % growth.

All models and metrics are in [results/RESULTS_SUMMARY.md](results/RESULTS_SUMMARY.md) and [results/tables](results/tables). The numbers in notebook 01 come from a single train/test split and are superseded by notebook 02.

## Data

The code uses data from the [Alzheimer's Disease Neuroimaging Initiative (ADNI)](https://adni.loni.usc.edu). ADNI data cannot be redistributed. Apply for access at [adni.loni.usc.edu](https://adni.loni.usc.edu) and accept the Data Use Agreement, then download:

1. **MRI scans**: the ADNI1 "Complete 3Yr 1.5T" image collection (NIfTI). Flatten it with [adni-scan-organizer](https://github.com/ratulhasan001/adni-scan-organizer) so that each subject folder contains `<Visit>.nii`.
2. **Collection metadata CSV** exported with the collection (here `ADNI1_Complete_3Yr_1.5T_10_02_2025.csv`). Columns used: `Image Data ID`, `Subject`, `Group`, `Sex`, `Age`, `Visit`, `Acq Date`, `Description`.

Notebook 01 produces `hippocampal_volumes.csv` (`SubjectID, Visit, Diagnosis, Volume_mm3`, diagnosis `CN`, `MCI` or `AD`). Notebook 02 expects:

```
data/
├── hippocampal_volumes_382.csv               # volume table from notebook 01
└── ADNI1_Complete_3Yr_1.5T_10_02_2025.csv    # ADNI collection metadata
```

`data/` is listed in `.gitignore`. In this repository, the outputs of notebook cells that printed ADNI subject IDs or rendered individual MRI scans have been cleared, and the per-subject prediction caches (`results/predictions/`) and the one figure that labels individual subjects (Fig 8) are not included. Figure files keep the numbering of the write-up; Figs 1 and 2 are diagrams that are not produced by the notebook.

## How to run

**Notebook 01** is a Colab notebook. Open it in Google Colab with a GPU runtime, mount Google Drive, and set the paths at the top of each cell (`ROOT_DIR`, `META_FILE`, `CSV_PATH`, `VOL_CSV`) to where you keep the data. Run the cells in order: split, classification, FastSurfer setup and segmentation, volume extraction, forecasting. It needs `monai`, `nibabel`, `nilearn`, FastSurfer (cloned by the notebook) and `numpy<2`.

**Notebook 02** runs on a CPU:

```bash
pip install numpy==1.26.4 pandas==2.2.2 torch statsmodels xgboost scikit-learn scipy joblib matplotlib seaborn patsy jupyter
jupyter notebook 02_bi_rnn_forecasting_cv.ipynb    # then Kernel → Restart & Run All
```

Put the two CSV files in `data/` first. A full run takes about 20 minutes on an 8-core laptop; trained models are cached in `results/predictions/`. Set the environment variable `BIRNN_QUICK=1` for a fast smoke test with small settings (outputs go to `results_quick/`). The saved outputs were produced with Python 3.12.7, PyTorch 2.9.1, statsmodels 0.14.2 and XGBoost 3.2.0 on macOS (arm64).

## Known limitations

- Notebook 01 is a working Colab notebook kept as it was run: paths point to Google Drive, some cells are repeated variants (FastSurfer setup, classification runs), and its forecasting cells use one 80/20 split without a validation set.
- `scripts/plot_baseline_segmentations.py` has a line break inside an f-string (lines 91–92), so Python reports a syntax error; replacing that line break with `\n` fixes it. It is kept as written.

## Authors

Ratul Hasan, Yousuf Oley and Ruhani Akter, Department of Computer Science and Engineering, BAUET.

Ratul Hasan · [ratulhasan.dev](https://ratulhasan.dev)
