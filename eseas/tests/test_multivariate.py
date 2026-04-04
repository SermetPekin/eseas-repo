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


import pytest
from pathlib import Path
from eseas import Seasonal
from eseas import Options
from eseas.core.seas_testing_utils import get_testing_utils
from eseas.tests.test_utils import skip_if_no_cruncher


testing_utils = get_testing_utils()
demetra_folder = testing_utils.demetra_folder
java_folder = testing_utils.java_folder
local_folder = testing_utils.local_folder


@skip_if_no_cruncher
def test_multivariate_monthly(tmp_path):
    """Test multivariate workspace with monthly data (4 series)"""

    # Create a temporary output folder
    temp_local_folder = tmp_path / "multivariate_output"
    temp_local_folder.mkdir()

    # Set up options pointing to the multivariate workspace
    workspace_path = Path(demetra_folder) / "multivariate.xml"
    assert workspace_path.exists(), f"Multivariate workspace not found at {workspace_path}"

    options = Options(
        demetra_folder=str(workspace_path.parent),
        java_folder=java_folder,
        local_folder=str(temp_local_folder),
        test=False,
        verbose=True,
        replace_original_files=False,
        result_file_names=("sa", "s", "cal"),
        workspace_mode=True,
        java_bin=None,
        replace_general_params=True,
        auto_approve=True,
        csvlayout="list"
    )

    m = Seasonal(options)
    m.run()

    # Verify output was generated
    # The structure should be: temp_local_folder/@eseas_wspace/test_output/multivariate/SAProcessing-1/
    output_dir = temp_local_folder / "@eseas_wspace" / "test_output" / "multivariate" / "SAProcessing-1"

    # Check that output directory exists
    assert output_dir.exists(), f"Output directory not created at {output_dir}"

    # Check that CSV files were generated
    csv_files = list(output_dir.glob("*.csv"))
    assert len(csv_files) > 0, "No CSV files generated"

    # Should have a reasonable number of output files for 2 series
    # Each series generates multiple CSV files, so we expect at least 20 files total
    assert len(csv_files) >= 20, f"Expected at least 20 CSV files for 2 series, got {len(csv_files)}"


@skip_if_no_cruncher
def test_multivariate_quarterly(tmp_path):
    """Test multivariate workspace with quarterly data (3 series)"""

    # Create a temporary output folder
    temp_local_folder = tmp_path / "multivariate_quarterly_output"
    temp_local_folder.mkdir()

    # Set up options pointing to the multivariate_quarterly workspace
    workspace_path = Path(demetra_folder) / "multivariate_quarterly.xml"
    assert workspace_path.exists(), f"Multivariate quarterly workspace not found at {workspace_path}"

    options = Options(
        demetra_folder=str(workspace_path.parent),
        java_folder=java_folder,
        local_folder=str(temp_local_folder),
        test=False,
        verbose=True,
        replace_original_files=False,
        result_file_names=("sa", "s", "cal"),
        workspace_mode=True,
        java_bin=None,
        replace_general_params=True,
        auto_approve=True,
        csvlayout="list"
    )

    m = Seasonal(options)
    m.run()

    # Verify output was generated
    output_dir = temp_local_folder / "@eseas_wspace" / "test_output" / "multivariate_quarterly" / "SAProcessing-1"

    # Check that output directory exists
    assert output_dir.exists(), f"Output directory not created at {output_dir}"

    # Check that CSV files were generated
    csv_files = list(output_dir.glob("*.csv"))
    assert len(csv_files) > 0, "No CSV files generated"

    # Should have a reasonable number of output files for 2 series
    # Each series generates multiple CSV files, so we expect at least 20 files total
    assert len(csv_files) >= 20, f"Expected at least 20 CSV files for 2 series, got {len(csv_files)}"


@skip_if_no_cruncher
def test_multivariate_combined_output(tmp_path):
    """Test that combined output is properly generated for multivariate data"""

    temp_local_folder = tmp_path / "multivariate_combined"
    temp_local_folder.mkdir()

    workspace_path = Path(demetra_folder) / "multivariate.xml"

    options = Options(
        demetra_folder=str(workspace_path.parent),
        java_folder=java_folder,
        local_folder=str(temp_local_folder),
        test=False,
        verbose=False,
        replace_original_files=False,
        result_file_names=("sa", "s"),
        workspace_mode=True,
        java_bin=None,
        replace_general_params=True,
        auto_approve=True,
        csvlayout="vtable"
    )

    m = Seasonal(options)
    m.run()

    # Check for combined.xlsx output
    expected_output = temp_local_folder / "test_output" / "multivariate" / "combined.xlsx"
    assert expected_output.exists(), "Combined output file was not generated"

    # Verify the combined file has data
    import pandas as pd
    df = pd.read_excel(expected_output)
    assert len(df) > 0, "Combined output file is empty"

    # Should have data for multiple series
    assert len(df) > 50, f"Expected substantial data in combined output, got {len(df)} rows"
