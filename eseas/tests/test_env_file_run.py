from typing import Any

import pandas as pd
from eseas import Seasonal
from eseas import Options
from eseas.core.df_operations import make_df_float
from eseas.core.cruncher_classes import get_cruncher
from eseas.core.cruncher_classes import Cruncher
from eseas.core.demetra import get_demetra_files
from eseas.core.picker_classes import OutFilePicker
from eseas.core.seas_testing_utils import get_testing_utils
from eseas.core.seas_utils import filter_xls
from eseas.core.df_operations import get_rand_hash


def create_env_file():
    template = """
java_bin22 = /usr/bin
java_folder22 = /Users/guest/app/jwsacruncher-2.2.6/bin
demetra_source_folder = ./eseas/data_for_testing/unix
local_folder = ./test_out
TestFolderInstance= ./test_out
"""
    with open(".env2", "w") as f:
        f.write(template)


create_env_file()


def test_seasonal_environment_file():
    options = Options(
        None,
        None,
        None,
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
        java_bin=None,
    )
    m = Seasonal(options)
    m.part1()
    m.part2()


def test_seasonal_environment_file2():
    options = Options(
        demetra_folder=None,
        java_folder=None,
        local_folder=None,
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
        java_bin=None,
    )
    m = Seasonal(options)
    m.part1()
    m.part2()
