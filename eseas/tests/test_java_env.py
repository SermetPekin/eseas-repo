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
from eseas.core.java_environ import JavaEnviron

import os


def test_java_environ(capsys):
    with capsys.disabled():
        java_environ = JavaEnviron(None)
        assert java_environ.java_bin is None
        folder = "/usr/bin"
        j = JavaEnviron(folder)
        assert j.java_bin == folder

        assert folder in os.environ["PATH"].split(j.separator)
