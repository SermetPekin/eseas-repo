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


from dataclasses import dataclass
from pathlib import Path
import os
from eseas.core.utils_general2 import create_dir
from .utils_general2 import get_os


@dataclass
class TestingUtils:
    demetra_folder: str
    java_folder: str
    local_folder: str


def check_folder(folder):
    print(Path(folder).absolute())
    assert Path(folder).is_dir()


def get_env_java_folder():
    return os.environ.get("JAVA_CRUNCHER_BIN")


def get_testing_utils(check=False):
    """
    jdemetra/jswacruncher
    https://github.com/jdemetra/jwsacruncher/releases/tag/v2.2.4
    :return:
    """

    fold = "win"
    if get_os() != "win":
        fold = "unix"

    demetra_folder = rf"./eseas/data_for_testing/{fold}"
    # /Users/XABC/Downloads/jwsacruncher-2.2.5 3
    java_folder = Path(r"../../../Downloads/jwsacruncher-2.2.5 3/bin")

    if get_env_java_folder():
        java_folder = get_env_java_folder()

    # if GithubActions().is_testing():
    #     java_folder = os.environ["JAVA_CRUNCHER_BIN"]

    local_folder = r"./eseas_output"
    create_dir(local_folder)
    if check:
        _ = tuple(map(check_folder, (demetra_folder, java_folder, local_folder)))

    return TestingUtils(demetra_folder, java_folder, local_folder)
