"""Demetra output types """

from typing import Dict, Optional

full_content_dem = """
y|Original series
y_f|Forecasts of the original series
y_ef|Standard errors of the forecasts of the original
y_c|Interpolated series
yc_f|Forecasts of the interpolated series
yc_ef|Standard errors of the forecasts of the interpolated
y_lin|Linearised series (not transformed)
l|Linearised series (transformed)
ycal|Series corrected for calendar effects
ycal_f|Forecasts of the series corrected for calendar effects
l_f|Forecasts of the linearised series
l_b|Backcasts of the linearised series
t|Trend (including deterministic effects)
t_f|Forecasts of the trend
sa|Seasonally adjusted series (including deterministic effects)
sa_f|Forecasts of the seasonally adjusted series
s|Seasonal component (including deterministic effects)
s_f|Forecasts of the seasonal component
i|Irregular component (including deterministic effects)
i_f|Forecasts of the irregular component
det|All deterministic effects
det_f| Forecasts of the deterministic effects
cal|Calendar effects
cal_f| Forecasts of the calendar effects
tde|Trading day effect
tde_f|Forecasts of the trading day effect
mhe|Moving holidays effects
mhe_f|Forecasts of the moving holidays effects
ee|Easter effect
ee_f|Forecasts of the Easter effect
omhe|Other moving holidays effects
omhe_f|Forecasts of the other moving holidays effects
out|All outliers effects
out_f|Forecasts of all outliers effects
out_i|Outliers effects related to irregular (AO, TC)
out_i_f|Forecasts of outliers effects related to irregular (TC)
out_t|Outliers effects related to trend (LS)
out_t_f|Forecasts of outliers effects related to trend (LS)
out_s|Outliers effects related to seasonal (SO)
out_s_f|Forecasts of outliers effects related to seasonal (SO)
reg|All other regression effects
reg_f|Forecasts of all other regression effects
reg_i|Regression effects related to irregular
reg_i_f|Forecasts of regression effects related to irregular
reg_t|Regression effects related to trend
reg_t_f|Forecasts of regression effects related to trend
reg_s|Regression effects related to seasonal
reg_s_f|Forecasts of regression effects related to seasonal
reg_sa|Regression effects related to seasonally adjusted series
reg_sa_f|Forecasts of regression effects related to seasonally adjusted
reg_y|Separate regression effects
reg_y_f|Forecasts of separate regression effects
fullresiduals|Full residuals of the RegARIMA model
decomposition.y_lin|Linearised series used as input in the
decomposition.y_lin_f|Forecast of the linearised series used as
decomposition.t_lin|Trend produced by the decomposition
decomposition.t_lin_f|Forecasts of the trend produced by the
decomposition.s_lin|Seasonal component produced by the decomposition
decomposition.s_lin_f|Forecasts of the Seasonal component produced by
decomposition.i_lin|Irregular produced by the decomposition
decomposition.i_lin_f|Forecasts of the irregular produced by the
decomposition.sa_lin|Seasonally adjusted series produced by the decomposition
decomposition.sa_lin_f|Forecasts of the seasonally adjusted series produced
decomposition.si_lin|Seasonal-Irregular produced by the decomposition
lambda decomposition_a-tables_a1| For X-13ARIMA-SEATS only. Series
benchmarking_result| Benchmarked seasonally adjusted series
benchmarking_target| Target for the benchmarking
"""

local_separator = "|"

load_dict_once = False


def get_dict_of_demetra() -> Dict[str, str]:
    dem_dict = {}

    def make_dict(element):
        parts = element.split(local_separator)
        obj = {parts[0]: parts[1]}
        dem_dict.update(obj)
        return obj

    lines = full_content_dem.splitlines()
    lines = filter(lambda x: x.strip(), lines)
    _ = tuple(map(make_dict, lines))
    return dem_dict


if not load_dict_once:
    load_dict_once = get_dict_of_demetra()


def get_meaning_demetra_file(name: str) -> Optional[str]:
    global load_dict_once
    return load_dict_once.get(name, None)


def convert_demetra_file_md() -> str:
    items = list(load_dict_once.items())

    def f(item):
        k, v = item
        return f"{k} : {v } "

    return "\n".join(map(f, items))


def create_md_demetra() -> None:
    content = convert_demetra_file_md()
    from evdspy.EVDSlocal.common.files import Write

    Write("./demetra_components.md", content)


"""

    y : Original series
    y_f : Forecasts of the original series
    y_ef : Standard errors of the forecasts of the original
    y_c : Interpolated series
    yc_f : Forecasts of the interpolated series
    yc_ef : Standard errors of the forecasts of the interpolated
    y_lin : Linearised series (not transformed)
    l : Linearised series (transformed)
    ycal : Series corrected for calendar effects
    ycal_f : Forecasts of the series corrected for calendar effects
    l_f : Forecasts of the linearised series
    l_b : Backcasts of the linearised series
    t : Trend (including deterministic effects)
    t_f : Forecasts of the trend
    sa : Seasonally adjusted series (including deterministic effects)
    sa_f : Forecasts of the seasonally adjusted series
    s : Seasonal component (including deterministic effects)
    s_f : Forecasts of the seasonal component
    i : Irregular component (including deterministic effects)
    i_f : Forecasts of the irregular component
    det : All deterministic effects
    det_f :  Forecasts of the deterministic effects
    cal : Calendar effects
    cal_f :  Forecasts of the calendar effects
    tde : Trading day effect
    tde_f : Forecasts of the trading day effect
    mhe : Moving holidays effects
    mhe_f : Forecasts of the moving holidays effects
    ee : Easter effect
    ee_f : Forecasts of the Easter effect
    omhe : Other moving holidays effects
    omhe_f : Forecasts of the other moving holidays effects
    out : All outliers effects
    out_f : Forecasts of all outliers effects
    out_i : Outliers effects related to irregular (AO, TC)
    out_i_f : Forecasts of outliers effects related to irregular (TC)
    out_t : Outliers effects related to trend (LS)
    out_t_f : Forecasts of outliers effects related to trend (LS)
    out_s : Outliers effects related to seasonal (SO)
    out_s_f : Forecasts of outliers effects related to seasonal (SO)
    reg : All other regression effects
    reg_f : Forecasts of all other regression effects
    reg_i : Regression effects related to irregular
    reg_i_f : Forecasts of regression effects related to irregular
    reg_t : Regression effects related to trend
    reg_t_f : Forecasts of regression effects related to trend
    reg_s : Regression effects related to seasonal
    reg_s_f : Forecasts of regression effects related to seasonal
    reg_sa : Regression effects related to seasonally adjusted series
    reg_sa_f : Forecasts of regression effects related to seasonally adjusted
    reg_y : Separate regression effects
    reg_y_f : Forecasts of separate regression effects
    fullresiduals : Full residuals of the RegARIMA model
    decomposition.y_lin : Linearised series used as input in the
    decomposition.y_lin_f : Forecast of the linearised series used as
    decomposition.t_lin : Trend produced by the decomposition
    decomposition.t_lin_f : Forecasts of the trend produced by the
    decomposition.s_lin : Seasonal component produced by the decomposition
    decomposition.s_lin_f : Forecasts of the Seasonal component produced by
    decomposition.i_lin : Irregular produced by the decomposition
    decomposition.i_lin_f : Forecasts of the irregular produced by the
    decomposition.sa_lin : Seasonally adjusted series
      produced by the decomposition
    decomposition.sa_lin_f : Forecasts of the seasonally
      adjusted series produced
    decomposition.si_lin : Seasonal-Irregular produced by the decomposition
    lambda decomposition_a-tables_a1 :  For X-13ARIMA-SEATS only. Series
    benchmarking_result :  Benchmarked seasonally adjusted series
    benchmarking_target :  Target for the benchmarking

"""


if __name__ == "__main__":

    a = load_dict_once
    print(a)
    md = convert_demetra_file_md()
    print(md)
