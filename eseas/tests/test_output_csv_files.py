import pytest
from pathlib import Path
from eseas import Seasonal, Options
from eseas.tests.test_utils import skip_if_no_cruncher

@skip_if_no_cruncher
def test_output_csv_files_creation(tmp_path):
    """
    Test that jwsacruncher actually produces the expected CSV output files.
    Checks explicitly for 'series_sa.csv', 'series_ycal.csv' and other specified files 
    inside the output structure.
    """
    # Use real test data
    from eseas.core.seas_testing_utils import get_testing_utils
    testing_utils = get_testing_utils()
    
    demetra_folder = testing_utils.demetra_folder
    java_folder = testing_utils.java_folder
    
    # We will point the local_folder (output destination) to our test tmp_path
    local_output = tmp_path / "eseas_output"
    
    options = Options(
        demetra_folder=demetra_folder,
        java_folder=java_folder,
        local_folder=str(local_output),
        test=False,
        verbose=True,
        replace_original_files=False,
        auto_approve=True,  # No manual prompts
        result_file_names=("sa", "ycal", "cal", "s_f"),
        workspace_mode=True, 
    )
    
    m = Seasonal(options)
    m.run()
    
    # After run(), output should be generated under the local_output folder. 
    # Use glob to find the deeply nested generated files.
    sa_files = list(local_output.rglob("series_sa.csv"))
    ycal_files = list(local_output.rglob("series_ycal.csv"))
    cal_files = list(local_output.rglob("series_cal.csv"))
    
    assert len(sa_files) > 0, f"Expected to find 'series_sa.csv' inside {local_output}, but found none."
    assert len(ycal_files) > 0, f"Expected to find 'series_ycal.csv' inside {local_output}, but found none."
    assert len(cal_files) > 0, f"Expected to find 'series_cal.csv' inside {local_output}, but found none."

    # In some Windows configurations, JDemetra produces 0-byte result files when it hits 
    # permission issues, path truncation, or frozen workspace bugs.
    # Check that at least some 'series_sa.csv' has valid contents.
    some_sa_has_size = any(f.stat().st_size > 10 for f in sa_files)
    assert some_sa_has_size, "The created 'series_sa.csv' files are completely empty (0 bytes). JDemetra+ crunching failed internally without raising OS exception."

    some_ycal_has_size = any(f.stat().st_size > 10 for f in ycal_files)
    assert some_ycal_has_size, "The created 'series_ycal.csv' files are completely empty (0 bytes)."

