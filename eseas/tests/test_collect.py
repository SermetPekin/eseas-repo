import pandas as pd

from eseas.core.collect import collect_parts_of_results, make_float
from eseas.core.seasonal_options import SeasonalOptions as Options


def test_make_float():
    df = pd.DataFrame(
        {
            "Unnamed: 0": ["0", "1"],
            "a": ["1,12", "12,00"],
            "b": ["15,0", "20,0"],
        }
    )
    df_float = make_float(df)
    assert df_float["a"].iloc[0] == 1.12
    assert df_float["a"].iloc[1] == 12.0
    assert df_float["b"].iloc[0] == 15.0
    assert df_float["b"].iloc[1] == 20.0


def test_collect_parts_of_results(tmp_path, monkeypatch):
    # Mock get_cruncher to return a dummy cruncher with local_work_space
    class DummyCruncher:
        def __init__(self, ws):
            self.local_work_space = str(ws)

    # Use a separate mock workspace for our inputs
    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()

    import eseas.core.collect as collect_mod

    monkeypatch.setattr(
        collect_mod, "get_cruncher", lambda: DummyCruncher(workspace_dir)
    )

    # We will simulate collecting two folders: f1, f2
    for parent in ["f1", "f2"]:
        # create mock files inside our mock workspace (where get_cruncher().local_work_space points)
        dir_path = workspace_dir / "test_output" / parent / "SAProcessing-1"
        dir_path.mkdir(parents=True, exist_ok=True)

        # Create Dummy CSVs for default parts
        for part in ["sa", "s", "cal"]:
            df = pd.DataFrame({"Unnamed: 0": ["0"], f"series_{part}": ["1,0"]})
            df.to_csv(dir_path / f"series_{part}.csv", index=False, sep=";")

    # Mock Demetra folder search if needed, but we can pass xml_folders directly
    options = Options(
        demetra_folder=str(tmp_path),
        local_folder=str(tmp_path / "final_output"),
        result_file_names=("sa", "s", "cal"),
    )

    # Run the function
    collect_parts_of_results(options, xml_folders=["f1", "f2"])

    # Check that final combined excels were written to options.local_folder
    final_output = tmp_path / "final_output" / "test_output"

    f1_excel = final_output / "f1" / "combined.xlsx"
    assert f1_excel.exists()
    assert set(pd.ExcelFile(f1_excel).sheet_names) == {"sa", "s", "cal"}

    f2_excel = final_output / "f2" / "combined.xlsx"
    assert f2_excel.exists()
    assert set(pd.ExcelFile(f2_excel).sheet_names) == {"sa", "s", "cal"}


def test_collect_parts_out_folder(tmp_path, monkeypatch):
    class DummyCruncher:
        def __init__(self, ws):
            self.local_work_space = str(ws)

    workspace_dir = tmp_path / "workspace"
    workspace_dir.mkdir()

    import eseas.core.collect as collect_mod

    monkeypatch.setattr(
        collect_mod, "get_cruncher", lambda: DummyCruncher(workspace_dir)
    )

    dir_path = workspace_dir / "test_output" / "f3" / "SAProcessing-1"
    dir_path.mkdir(parents=True, exist_ok=True)

    for part in ["sa"]:
        df = pd.DataFrame({"Unnamed: 0": ["0"], f"series_{part}": ["1,0"]})
        df.to_csv(dir_path / f"series_{part}.csv", index=False, sep=";")

    options = Options(
        demetra_folder=str(tmp_path),
        local_folder=str(tmp_path / "final_output"),
        result_file_names=("sa",),
    )

    custom_out = tmp_path / "custom_out"

    collect_parts_of_results(
        options, xml_folders=["f3"], out_folder=str(custom_out), out_file_name="special"
    )

    f3_excel = custom_out / "f3" / "special.xlsx"
    assert f3_excel.exists()
    assert set(pd.ExcelFile(f3_excel).sheet_names) == {"sa"}
