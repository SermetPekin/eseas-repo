from dataclasses import dataclass
from pathlib import Path

from eseas.core.utils_general_copy import create_dir

from .utils_general_copy import get_os


@dataclass
class TestingUtils:
    demetra_folder: str
    java_folder: str
    local_folder: str


def check_folder(folder):
    print(Path(folder).absolute())
    assert Path(folder).is_dir()


def get_testing_utils():
    """
    jdemetra/jswacruncher
    https://github.com/jdemetra/jwsacruncher/releases/tag/v2.2.4
    :return:
    """

    fold = "win"
    if get_os() != "win":
        fold = "unix"

    demetra_folder = rf"./eseas/data_for_testing/{fold}"
    java_folder = r"../jwsacruncher-2.2.4/bin"
    local_folder = r"./evdspyseas_output"
    create_dir(local_folder)

    _ = tuple(map(check_folder, (demetra_folder, java_folder, local_folder)))

    return TestingUtils(demetra_folder, java_folder, local_folder)
