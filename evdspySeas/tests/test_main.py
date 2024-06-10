import pandas as pd
from evdspy.EVDSlocal.common.file_classes import mock_file_items
from evdspySeas.core.seasonal_general import SeasonalADV
from evdspySeas.core.seasonal_options import SeasonalOptions
from evdspySeas.core.df_operations import make_df_float
from evdspySeas.core.cruncher_classes import get_cruncher
from evdspySeas.core.cruncher_classes import Cruncher
from evdspySeas.core.demetra import get_demetra_files
from evdspySeas.core.picker_classes import OutFilePicker
from evdspySeas.core.seas_testing_utils import get_testing_utils
from evdspySeas.core.seas_utils import filter_xls

testing_utils = get_testing_utils()
demetra_folder = testing_utils.demetra_folder
java_folder = testing_utils.java_folder
local_folder = testing_utils.local_folder


def test_mevsimsel_general_basic():
    options = SeasonalOptions(
        demetra_folder,
        java_folder,
        local_folder,
    )
    m = SeasonalADV(options)
    m.part1()
    m.part2()


def test_a1():
    c = Cruncher()
    c.set_items(java_folder, local_folder, demetra_folder)
    dem_files = get_demetra_files(demetra_folder)
    for f in dem_files:
        of_picker = OutFilePicker(f)
        of_picker.pick_files()


def test_mevsimsel_general():
    options = SeasonalOptions(
        demetra_folder,
        java_folder,
        local_folder,
        test=False,
        verbose=False,
        replace_original_files=False,
        auto_approve=False,
        result_file_names=(
            "sa",
            "s",
            "cal",
        ),
        workspace_mode=True,
    )
    m = SeasonalADV(options)
    m.part1()
    m.part2()


def test_get_cruncher():
    c = Cruncher()
    c.set_items("", "", "")
    get_cruncher()


def test_make_df_float(capsys):
    with capsys.disabled():
        df = pd.DataFrame({"a": ["1,12", "12"], "b": [15, 20]})
        df2 = make_df_float(df)
        print(df2)


def test_filter_xls(capsys):
    with capsys.disabled():
        items = mock_file_items()
        a = filter_xls(items)
        print(a)



def test_Cruncher():
    c1 = Cruncher()
    c1.crunch_folder = "abc"
    c2 = Cruncher()
    c2.crunch_folder = "abcdefg"
    assert c1.crunch_folder == c2.crunch_folder


def test_Cruncher():
    c1 = Cruncher()
    c1.crunch_folder = "abc"
    c2 = Cruncher()
    c2.crunch_folder = "abcdefg"
    assert c1.crunch_folder == c2.crunch_folder


def test_a1():
    c = Cruncher()
    c.set_items(java_folder, local_folder, demetra_folder)
    dem_files = get_demetra_files(demetra_folder)
    for f in dem_files:
        of_picker = OutFilePicker(f)
        of_picker.pick_files()
