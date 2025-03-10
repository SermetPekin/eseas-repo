# This file is part of the eseas project
# Copyright (C) 2024 Sermet Pekin 
#
# This source code is free software; you can redistribute it and/or
# modify it under the terms of the European Union Public License
# (EUPL), Version 1.2, as published by the European Commission.
#
# You should have received a copy of the EUPL version 1.2 along with this
# program. If not, you can obtain it at:
# <https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12>.
#
# This source code is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# European Union Public License for more details.
#
# Alternatively, if agreed upon, you may use this code under any later
# version of the EUPL published by the European Commission.

from pathlib import Path
from evdspy.EVDSlocal.common.files import Write


def _create_general_params(folder=".", file_name="general.params"):
    content = get_general_params()
    file_name_full = Path(folder) / file_name
    if file_name_full.is_file():
        return
    return Write(file_name_full, content)


def get_general_params():
    return """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<wsaConfig bundle="10000" csvlayout="list" csvseparator=";" ndecs="6">
    <policy>parameters</policy>
    <refreshall>true</refreshall>
    <matrix>
        <item>period</item>
        <item>span.start</item>
        <item>span.end</item>
        <item>span.n</item>
        <item>span.missing</item>
        <item>espan.start</item>
        <item>espan.end</item>
        <item>espan.n</item>
        <item>log</item>
        <item>adjust</item>
        <item>regression.lp</item>
        <item>regression.ntd</item>
        <item>regression.nmh</item>
        <item>regression.td-derived</item>
        <item>regression.td-ftest</item>
        <item>regression.easter</item>
        <item>regression.nout</item>
        <item>regression.noutao</item>
        <item>regression.noutls</item>
        <item>regression.nouttc</item>
        <item>regression.noutso</item>
        <item>regression.td(*)</item>
        <item>regression.out(*)</item>
        <item>regression.user(*)</item>
        <item>likelihood.neffectiveobs</item>
        <item>likelihood.np</item>
        <item>likelihood.logvalue</item>
        <item>likelihood.adjustedlogvalue</item>
        <item>likelihood.ssqerr</item>
        <item>likelihood.aic</item>
        <item>likelihood.aicc</item>
        <item>likelihood.bic</item>
        <item>likelihood.bicc</item>
        <item>residuals.ser</item>
        <item>residuals.ser-ml</item>
        <item>residuals.mean</item>
        <item>residuals.skewness</item>
        <item>residuals.kurtosis</item>
        <item>residuals.dh</item>
        <item>residuals.lb</item>
        <item>residuals.lb2</item>
        <item>residuals.seaslb</item>
        <item>residuals.bp</item>
        <item>residuals.bp2</item>
        <item>residuals.seasbp</item>
        <item>residuals.nudruns</item>
        <item>residuals.ludruns</item>
        <item>residuals.nruns</item>
        <item>residuals.lruns</item>
        <item>arima</item>
        <item>arima.mean</item>
        <item>arima.p</item>
        <item>arima.d</item>
        <item>arima.q</item>
        <item>arima.bp</item>
        <item>arima.bd</item>
        <item>arima.bq</item>
        <item>arima.phi(*)</item>
        <item>arima.bphi(*)</item>
        <item>arima.th(*)</item>
        <item>arima.bth(*)</item>
        <item>decomposition.seasonality</item>
        <item>decomposition.trendfilter</item>
        <item>decomposition.seasfilter</item>
        <item>m-statistics.m1</item>
        <item>m-statistics.m2</item>
        <item>m-statistics.m3</item>
        <item>m-statistics.m4</item>
        <item>m-statistics.m5</item>
        <item>m-statistics.m6</item>
        <item>m-statistics.m7</item>
        <item>m-statistics.m8</item>
        <item>m-statistics.m9</item>
        <item>m-statistics.m10</item>
        <item>m-statistics.m11</item>
        <item>m-statistics.q</item>
        <item>m-statistics.q-m2</item>
        <item>method</item>
        <item>variancedecomposition.cycle</item>
        <item>variancedecomposition.seasonality</item>
        <item>variancedecomposition.irregular</item>
        <item>variancedecomposition.tdh</item>
        <item>variancedecomposition.others</item>
        <item>variancedecomposition.total</item>
        <item>diagnostics.logstat</item>
        <item>diagnostics.levelstat</item>
        <item>diagnostics.fcast-insample-mean</item>
        <item>diagnostics.fcast-outsample-mean</item>
        <item>diagnostics.fcast-outsample-variance</item>
        <item>diagnostics.seas-lin-f</item>
        <item>diagnostics.seas-lin-qs</item>
        <item>diagnostics.seas-lin-kw</item>
        <item>diagnostics.seas-lin-friedman</item>
        <item>diagnostics.seas-lin-periodogram</item>
        <item>diagnostics.seas-lin-spectralpeaks</item>
        <item>diagnostics.seas-si-combined</item>
        <item>diagnostics.seas-si-evolutive</item>
        <item>diagnostics.seas-si-stable</item>
        <item>diagnostics.seas-res-f</item>
        <item>diagnostics.seas-res-qs</item>
        <item>diagnostics.seas-res-kw</item>
        <item>diagnostics.seas-res-friedman</item>
        <item>diagnostics.seas-res-periodogram</item>
        <item>diagnostics.seas-res-spectralpeaks</item>
        <item>diagnostics.seas-res-combined</item>
        <item>diagnostics.seas-res-combined3</item>
        <item>diagnostics.seas-res-evolutive</item>
        <item>diagnostics.seas-res-stable</item>
        <item>diagnostics.seas-i-f</item>
        <item>diagnostics.seas-i-qs</item>
        <item>diagnostics.seas-i-kw</item>
        <item>diagnostics.seas-i-periodogram</item>
        <item>diagnostics.seas-i-spectralpeaks</item>
        <item>diagnostics.seas-i-combined</item>
        <item>diagnostics.seas-i-combined3</item>
        <item>diagnostics.seas-i-evolutive</item>
        <item>diagnostics.seas-i-stable</item>
        <item>diagnostics.seas-sa-f</item>
        <item>diagnostics.seas-sa-qs</item>
        <item>diagnostics.seas-sa-kw</item>
        <item>diagnostics.seas-sa-friedman</item>
        <item>diagnostics.seas-sa-periodogram</item>
        <item>diagnostics.seas-sa-spectralpeaks</item>
        <item>diagnostics.seas-sa-combined</item>
        <item>diagnostics.seas-sa-combined3</item>
        <item>diagnostics.seas-sa-evolutive</item>
        <item>diagnostics.seas-sa-stable</item>
        <item>diagnostics.seas-sa-ac1</item>
        <item>diagnostics.td-sa-all</item>
        <item>diagnostics.td-sa-last</item>
        <item>diagnostics.td-i-all</item>
        <item>diagnostics.td-i-last</item>
        <item>diagnostics.td-res-all</item>
        <item>diagnostics.td-res-last</item>
        <item>diagnostics.ic-ratio-henderson</item>
        <item>diagnostics.ic-ratio</item>
        <item>diagnostics.msr-global</item>
        <item>diagnostics.msr(*)</item>
        <item>decomposition.parameters_cutoff</item>
        <item>decomposition.model_changed</item>
        <item>decomposition.tvar-estimator</item>
        <item>decomposition.tvar-estimate</item>
        <item>decomposition.tvar-pvalue</item>
        <item>decomposition.savar-estimator</item>
        <item>decomposition.savar-estimate</item>
        <item>decomposition.savar-pvalue</item>
        <item>decomposition.svar-estimator</item>
        <item>decomposition.svar-estimate</item>
        <item>decomposition.svar-pvalue</item>
        <item>decomposition.ivar-estimator</item>
        <item>decomposition.ivar-estimate</item>
        <item>decomposition.ivar-pvalue</item>
        <item>decomposition.tscorr-estimator</item>
        <item>decomposition.tscorr-estimate</item>
        <item>decomposition.tscorr-pvalue</item>
        <item>decomposition.ticorr-estimator</item>
        <item>decomposition.ticorr-estimate</item>
        <item>decomposition.ticorr-pvalue</item>
        <item>decomposition.sicorr-estimator</item>
        <item>decomposition.sicorr-estimate</item>
        <item>decomposition.sicorr-pvalue</item>
        <item>decomposition.ar_root(*)</item>
        <item>decomposition.ma_root(*)</item>
        <item>diagnostics.basic checks.definition:2</item>
        <item>diagnostics.basic checks.annual totals:2</item>
        <item>diagnostics.visual spectral analysis.spectral seas peaks</item>
        <item>diagnostics.visual spectral analysis.spectral td peaks</item>
        <item>diagnostics.regarima residuals.normality:2</item>
        <item>diagnostics.regarima residuals.independence:2</item>
        <item>diagnostics.regarima residuals.spectral td peaks:2</item>
        <item>diagnostics.regarima residuals.spectral seas peaks:2</item>
        <item>diagnostics.outliers.number of outliers:2</item>
        <item>diagnostics.out-of-sample.mean:2</item>
        <item>diagnostics.out-of-sample.mse:2</item>
        <item>diagnostics.seats.seas variance:2</item>
        <item>diagnostics.seats.irregular variance:2</item>
        <item>diagnostics.seats.seas/irr cross-correlation:2</item>
        <item>diagnostics.m-statistics.q:2</item>
        <item>diagnostics.m-statistics.q-m2:2</item>
        <item>diagnostics.residual trading days tests.f-test on sa (td):2</item>
        <item>diagnostics.residual trading days tests.f-test on i (td):2</item>
        <item>diagnostics.residual seasonality tests.qs test on sa:2</item>
        <item>diagnostics.residual seasonality tests.qs test on i:2</item>
        <item>diagnostics.residual seasonality tests.f-test on sa (seasonal dummies):2</item>
        <item>diagnostics.residual seasonality tests.f-test on i (seasonal dummies):2</item>
        <item>diagnostics.combined seasonality test.combined seasonality test on sa:2</item>
        <item>diagnostics.combined seasonality test.combined seasonality test on sa (last 3 years):2</item>
        <item>diagnostics.combined seasonality test.combined seasonality test on irregular:2</item>
        <item>diagnostics.quality</item>
    </matrix>
    <tsmatrix>
        <series>y</series>
        <series>y_f</series>
        <series>y_ef</series>
        <series>yc</series>
        <series>yc_f</series>
        <series>yc_ef</series>
        <series>l</series>
        <series>y_lin</series>
        <series>y_lin_f</series>
        <series>ycal</series>
        <series>ycal_f</series>
        <series>det</series>
        <series>det_f</series>
        <series>l_f</series>
        <series>l_b</series>
        <series>cal</series>
        <series>cal_f</series>
        <series>tde</series>
        <series>tde_f</series>
        <series>mhe</series>
        <series>mhe_f</series>
        <series>ee</series>
        <series>ee_f</series>
        <series>omhe</series>
        <series>omhe_f</series>
        <series>out</series>
        <series>out_f</series>
        <series>out_i</series>
        <series>out_i_f</series>
        <series>out_t</series>
        <series>out_t_f</series>
        <series>out_s</series>
        <series>out_s_f</series>
        <series>reg</series>
        <series>reg_f</series>
        <series>reg_t</series>
        <series>reg_t_f</series>
        <series>reg_s</series>
        <series>reg_s_f</series>
        <series>reg_i</series>
        <series>reg_i_f</series>
        <series>reg_sa</series>
        <series>reg_sa_f</series>
        <series>reg_y</series>
        <series>reg_y_f</series>
        <series>reg_u</series>
        <series>reg_u_f</series>
        <series>fullresiduals</series>
        <series>fcasts(?)</series>
        <series>bcasts(?)</series>
        <series>lin_fcasts(?)</series>
        <series>lin_bcasts(?)</series>
        <series>efcasts(?)</series>
        <series>decomposition.y_cmp</series>
        <series>decomposition.y_cmp_f</series>
        <series>decomposition.t_cmp</series>
        <series>decomposition.t_cmp_f</series>
        <series>decomposition.sa_cmp</series>
        <series>decomposition.s_cmp</series>
        <series>decomposition.s_cmp_f</series>
        <series>decomposition.i_cmp</series>
        <series>decomposition.a-tables.a1</series>
        <series>decomposition.a-tables.a1a</series>
        <series>decomposition.a-tables.a1b</series>
        <series>decomposition.a-tables.a6</series>
        <series>decomposition.a-tables.a7</series>
        <series>decomposition.a-tables.a8</series>
        <series>decomposition.a-tables.a8t</series>
        <series>decomposition.a-tables.a8s</series>
        <series>decomposition.a-tables.a8i</series>
        <series>decomposition.a-tables.a9</series>
        <series>decomposition.a-tables.a9sa</series>
        <series>decomposition.a-tables.a9u</series>
        <series>decomposition.a-tables.a9ser</series>
        <series>decomposition.b-tables.b1</series>
        <series>decomposition.b-tables.b2</series>
        <series>decomposition.b-tables.b3</series>
        <series>decomposition.b-tables.b4</series>
        <series>decomposition.b-tables.b5</series>
        <series>decomposition.b-tables.b6</series>
        <series>decomposition.b-tables.b7</series>
        <series>decomposition.b-tables.b8</series>
        <series>decomposition.b-tables.b9</series>
        <series>decomposition.b-tables.b10</series>
        <series>decomposition.b-tables.b11</series>
        <series>decomposition.b-tables.b12</series>
        <series>decomposition.b-tables.b13</series>
        <series>decomposition.b-tables.b14</series>
        <series>decomposition.b-tables.b15</series>
        <series>decomposition.b-tables.b16</series>
        <series>decomposition.b-tables.b17</series>
        <series>decomposition.b-tables.b18</series>
        <series>decomposition.b-tables.b19</series>
        <series>decomposition.b-tables.b20</series>
        <series>decomposition.c-tables.c1</series>
        <series>decomposition.c-tables.c2</series>
        <series>decomposition.c-tables.c3</series>
        <series>decomposition.c-tables.c4</series>
        <series>decomposition.c-tables.c5</series>
        <series>decomposition.c-tables.c6</series>
        <series>decomposition.c-tables.c7</series>
        <series>decomposition.c-tables.c8</series>
        <series>decomposition.c-tables.c9</series>
        <series>decomposition.c-tables.c10</series>
        <series>decomposition.c-tables.c11</series>
        <series>decomposition.c-tables.c12</series>
        <series>decomposition.c-tables.c13</series>
        <series>decomposition.c-tables.c14</series>
        <series>decomposition.c-tables.c15</series>
        <series>decomposition.c-tables.c16</series>
        <series>decomposition.c-tables.c17</series>
        <series>decomposition.c-tables.c18</series>
        <series>decomposition.c-tables.c19</series>
        <series>decomposition.c-tables.c20</series>
        <series>decomposition.d-tables.d1</series>
        <series>decomposition.d-tables.d2</series>
        <series>decomposition.d-tables.d3</series>
        <series>decomposition.d-tables.d4</series>
        <series>decomposition.d-tables.d5</series>
        <series>decomposition.d-tables.d6</series>
        <series>decomposition.d-tables.d7</series>
        <series>decomposition.d-tables.d8</series>
        <series>decomposition.d-tables.d9</series>
        <series>decomposition.d-tables.d10</series>
        <series>decomposition.d-tables.d10a</series>
        <series>decomposition.d-tables.d10b</series>
        <series>decomposition.d-tables.d11</series>
        <series>decomposition.d-tables.d11a</series>
        <series>decomposition.d-tables.d12</series>
        <series>decomposition.d-tables.d12a</series>
        <series>decomposition.d-tables.d13</series>
        <series>decomposition.d-tables.d14</series>
        <series>decomposition.d-tables.d15</series>
        <series>decomposition.d-tables.d16</series>
        <series>decomposition.d-tables.d16a</series>
        <series>decomposition.d-tables.d16b</series>
        <series>decomposition.d-tables.d18</series>
        <series>decomposition.d-tables.d19</series>
        <series>decomposition.d-tables.d20</series>
        <series>decomposition.e-tables.e1</series>
        <series>decomposition.e-tables.e2</series>
        <series>decomposition.e-tables.e3</series>
        <series>decomposition.e-tables.e11</series>
        <series>t</series>
        <series>t_f</series>
        <series>sa</series>
        <series>sa_f</series>
        <series>s</series>
        <series>s_f</series>
        <series>i</series>
        <series>i_f</series>
        <series>benchmarking.original</series>
        <series>benchmarking.target</series>
        <series>benchmarking.result</series>
        <series>decomposition.y_lin</series>
        <series>decomposition.y_lin_f</series>
        <series>decomposition.y_lin_ef</series>
        <series>decomposition.t_lin</series>
        <series>decomposition.t_lin_f</series>
        <series>decomposition.t_lin_e</series>
        <series>decomposition.t_lin_ef</series>
        <series>decomposition.sa_lin</series>
        <series>decomposition.sa_lin_f</series>
        <series>decomposition.sa_lin_e</series>
        <series>decomposition.sa_lin_ef</series>
        <series>decomposition.s_lin</series>
        <series>decomposition.s_lin_f</series>
        <series>decomposition.s_lin_e</series>
        <series>decomposition.s_lin_ef</series>
        <series>decomposition.i_lin</series>
        <series>decomposition.i_lin_f</series>
        <series>decomposition.i_lin_e</series>
        <series>decomposition.i_lin_ef</series>
        <series>decomposition.sa_cmp_f</series>
        <series>decomposition.i_cmp_f</series>
        <series>decomposition.i_cmp_e</series>
        <series>decomposition.t_cmp_e</series>
        <series>decomposition.s_cmp_e</series>
        <series>decomposition.sa_cmp_e</series>
        <series>decomposition.i_cmp_ef</series>
        <series>decomposition.t_cmp_ef</series>
        <series>decomposition.s_cmp_ef</series>
        <series>decomposition.sa_cmp_ef</series>
        <series>decomposition.si_cmp</series>
    </tsmatrix>
</wsaConfig>"""
