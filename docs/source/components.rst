Demetra Components
==================

Below is a list of the available components and their descriptions:

Original and Forecasted Series
------------------------------
- **y** : Original series
- **y_f** : Forecasts of the original series
- **y_ef** : Standard errors of the forecasts of the original
- **y_c** : Interpolated series
- **yc_f** : Forecasts of the interpolated series
- **yc_ef** : Standard errors of the forecasts of the interpolated

Linearized and Corrected Series
-------------------------------
- **y_lin** : Linearised series (not transformed)
- **l** : Linearised series (transformed)
- **ycal** : Series corrected for calendar effects
- **ycal_f** : Forecasts of the series corrected for calendar effects
- **l_f** : Forecasts of the linearised series
- **l_b** : Backcasts of the linearised series

Trend and Seasonally Adjusted Components
----------------------------------------
- **t** : Trend (including deterministic effects)
- **t_f** : Forecasts of the trend
- **sa** : Seasonally adjusted series (including deterministic effects)
- **sa_f** : Forecasts of the seasonally adjusted series

Seasonal, Irregular, and Deterministic Components
-------------------------------------------------
- **s** : Seasonal component (including deterministic effects)
- **s_f** : Forecasts of the seasonal component
- **i** : Irregular component (including deterministic effects)
- **i_f** : Forecasts of the irregular component
- **det** : All deterministic effects
- **det_f** : Forecasts of the deterministic effects

Calendar and Holiday Effects
----------------------------
- **cal** : Calendar effects
- **cal_f** : Forecasts of the calendar effects
- **tde** : Trading day effect
- **tde_f** : Forecasts of the trading day effect
- **mhe** : Moving holidays effects
- **mhe_f** : Forecasts of the moving holidays effects
- **ee** : Easter effect
- **ee_f** : Forecasts of the Easter effect
- **omhe** : Other moving holidays effects
- **omhe_f** : Forecasts of the other moving holidays effects

Outliers and Regression Effects
-------------------------------
- **out** : All outliers effects
- **out_f** : Forecasts of all outliers effects
- **out_i** : Outliers effects related to irregular (AO, TC)
- **out_i_f** : Forecasts of outliers effects related to irregular (TC)
- **out_t** : Outliers effects related to trend (LS)
- **out_t_f** : Forecasts of outliers effects related to trend (LS)
- **out_s** : Outliers effects related to seasonal (SO)
- **out_s_f** : Forecasts of outliers effects related to seasonal (SO)

- **reg** : All other regression effects
- **reg_f** : Forecasts of all other regression effects
- **reg_i** : Regression effects related to irregular
- **reg_i_f** : Forecasts of regression effects related to irregular
- **reg_t** : Regression effects related to trend
- **reg_t_f** : Forecasts of regression effects related to trend
- **reg_s** : Regression effects related to seasonal
- **reg_s_f** : Forecasts of regression effects related to seasonal
- **reg_sa** : Regression effects related to seasonally adjusted series
- **reg_sa_f** : Forecasts of regression effects related to seasonally adjusted
- **reg_y** : Separate regression effects
- **reg_y_f** : Forecasts of separate regression effects

RegARIMA Model and Decomposition Components
-------------------------------------------
- **fullresiduals** : Full residuals of the RegARIMA model

- **decomposition.y_lin** : Linearised series used as input in the decomposition
- **decomposition.y_lin_f** : Forecast of the linearised series used as input
- **decomposition.t_lin** : Trend produced by the decomposition
- **decomposition.t_lin_f** : Forecasts of the trend produced by the decomposition
- **decomposition.s_lin** : Seasonal component produced by the decomposition
- **decomposition.s_lin_f** : Forecasts of the seasonal component produced by the decomposition
- **decomposition.i_lin** : Irregular component produced by the decomposition
- **decomposition.i_lin_f** : Forecasts of the irregular component produced by the decomposition
- **decomposition.sa_lin** : Seasonally adjusted series produced by the decomposition
- **decomposition.sa_lin_f** : Forecasts of the seasonally adjusted series produced by the decomposition
- **decomposition.si_lin** : Seasonal-Irregular component produced by the decomposition

Benchmarking and Other Components
---------------------------------
- **lambda decomposition_a-tables_a1** : For X-13ARIMA-SEATS only. Series
- **benchmarking_result** : Benchmarked seasonally adjusted series
- **benchmarking_target** : Target for the benchmarking
