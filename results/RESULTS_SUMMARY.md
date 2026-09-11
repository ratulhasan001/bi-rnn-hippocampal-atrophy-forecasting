# Key results

Cohort: 382 subjects, 1957 scans. T1 = final-scan forecast (horizon 1.01 y).

- Persistence: MAE 186.5 ± 0.0 [172.3, 201.0]; skill 0.0%; r(change) nan; growth viol. 0.00%
- Population drift: MAE 141.2 ± 0.2 [130.2, 152.5]; skill 24.3%; r(change) -0.183; growth viol. 0.00%
- Linear extrapolation: MAE 144.2 ± 0.0 [130.8, 157.9]; skill 22.7%; r(change) 0.216; growth viol. 3.14%
- ARIMA(1,1,0): MAE 184.4 ± 0.0 [171.4, 198.2]; skill 1.1%; r(change) 0.182; growth viol. 12.30%
- Linear mixed-effects: MAE 121.4 ± 1.7 [110.6, 132.1]; skill 34.9%; r(change) 0.368; growth viol. 0.17%
- Linear mixed-effects + covariates: MAE 118.2 ± 0.9 [107.8, 128.8]; skill 36.6%; r(change) 0.391; growth viol. 0.09%
- XGBoost: MAE 126.6 ± 1.7 [116.2, 137.3]; skill 32.1%; r(change) 0.302; growth viol. 0.26%
- XGBoost + covariates: MAE 124.5 ± 2.5 [114.4, 135.1]; skill 33.2%; r(change) 0.325; growth viol. 0.09%
- Standard GRU: MAE 129.1 ± 0.3 [118.6, 139.9]; skill 30.8%; r(change) 0.239; growth viol. 0.00%
- Standard LSTM: MAE 128.8 ± 1.3 [118.0, 139.8]; skill 30.9%; r(change) 0.229; growth viol. 0.09%
- Standard Bi-LSTM: MAE 130.5 ± 1.9 [119.6, 141.5]; skill 30.0%; r(change) 0.189; growth viol. 0.00%
- Bio-Informed GRU: MAE 130.2 ± 1.3 [119.2, 141.3]; skill 30.2%; r(change) 0.183; growth viol. 0.00%
- Bio-Informed LSTM: MAE 130.4 ± 0.9 [119.4, 141.7]; skill 30.1%; r(change) 0.180; growth viol. 0.00%
- Bio-Informed Bi-LSTM: MAE 130.6 ± 1.3 [119.5, 141.7]; skill 30.0%; r(change) 0.184; growth viol. 0.00%
- Standard GRU + clip: MAE 129.1 ± 0.3 [118.6, 139.9]; skill 30.8%; r(change) 0.239; growth viol. 0.00%
- Hard-corridor GRU: MAE 128.9 ± 1.6 [118.1, 139.9]; skill 30.9%; r(change) 0.212; growth viol. 0.00%
- Hybrid GRU (no corridor): MAE 120.2 ± 1.0 [109.2, 131.1]; skill 35.5%; r(change) 0.337; growth viol. 0.09%
- Hybrid Bio-Informed LSTM: MAE 121.0 ± 0.9 [110.4, 131.5]; skill 35.1%; r(change) 0.345; growth viol. 0.00%
- Hybrid Bio-Informed GRU: MAE 121.0 ± 0.4 [110.3, 131.5]; skill 35.1%; r(change) 0.355; growth viol. 0.00%

## Planned comparisons (Holm)
- Hybrid Bio-Informed GRU vs Persistence: ΔMAE -65.5 [-77.5, -53.7], p_Holm = 3.56e-21
- Hybrid Bio-Informed GRU vs Population drift: ΔMAE -20.3 [-26.4, -14.0], p_Holm = 1.14e-09
- Hybrid Bio-Informed GRU vs Linear extrapolation: ΔMAE -23.2 [-33.1, -13.6], p_Holm = 0.000775
- Hybrid Bio-Informed GRU vs ARIMA(1,1,0): ΔMAE -63.4 [-75.7, -51.3], p_Holm = 8.38e-20
- Hybrid Bio-Informed GRU vs Linear mixed-effects: ΔMAE -0.4 [-3.6, 2.7], p_Holm = 1
- Hybrid Bio-Informed GRU vs Linear mixed-effects + covariates: ΔMAE +2.8 [0.0, 5.4], p_Holm = 0.257
- Hybrid Bio-Informed GRU vs XGBoost: ΔMAE -5.6 [-10.8, -0.5], p_Holm = 0.0995
- Hybrid Bio-Informed GRU vs XGBoost + covariates: ΔMAE -3.5 [-8.0, 0.9], p_Holm = 0.569
- Hybrid Bio-Informed GRU vs Bio-Informed GRU: ΔMAE -9.3 [-13.1, -5.4], p_Holm = 0.000124
- Hybrid Bio-Informed GRU vs Standard GRU: ΔMAE -8.2 [-11.7, -4.6], p_Holm = 0.000559
- Hybrid Bio-Informed GRU vs Hybrid GRU (no corridor): ΔMAE +0.7 [-1.1, 2.5], p_Holm = 0.37
- Bio-Informed GRU vs Standard GRU: ΔMAE +1.1 [-1.3, 3.5], p_Holm = 1
- Bio-Informed LSTM vs Standard LSTM: ΔMAE +1.6 [-0.1, 3.3], p_Holm = 0.532
- Bio-Informed Bi-LSTM vs Standard Bi-LSTM: ΔMAE +0.1 [-1.4, 1.6], p_Holm = 1

## Equivalence (TOST, ±5 mm³)
- Hybrid Bio-Informed GRU vs Linear mixed-effects + covariates: ΔMAE +2.75, 90% CI [0.49, 4.93], p = 0.0475, equivalent = True
- Hybrid Bio-Informed GRU vs Linear mixed-effects: ΔMAE -0.40, 90% CI [-3.12, 2.26], p = 0.00262, equivalent = True
- Hybrid Bio-Informed GRU vs XGBoost + covariates: ΔMAE -3.53, 90% CI [-7.19, 0.08], p = 0.261, equivalent = False