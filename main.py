from dataclasses import dataclass
from pathlib import Path
from eseas import SeasonalADV
from eseas import SeasonalOptions
from typing import Union

TESTING_FOLDER = r"./eseas/data_for_testing"
# TESTING_FOLDER = r"../data_for_testing"


def check_folder(folder):
    print(Path(folder).absolute())
    assert Path(folder).is_dir()


check_folder(TESTING_FOLDER)


def add_absolute(folder: str):
    p = Path(folder)
    return Path(p.absolute())


TESTING_FOLDER = add_absolute(TESTING_FOLDER)
# java_folder = add_absolute(r"../jwsacruncher-2.2.3-bin/bin")  # Crunch folder

java_folder = add_absolute(r"../jwsacruncher-2.2.4/bin")  # Crunch folder

check_folder(java_folder)


@dataclass
class Options:
    java_folder: Union[str, Path]
    local_folder: Union[str, Path]
    demetra_source_folder: Union[str, Path]


def seasonal_main(options, part=1):
    options_ = SeasonalOptions(
        options.demetra_source_folder,
        options.java_folder,
        options.local_folder,
        result_file_names=(
            "sa",
            "s_f",
            "cal",
        ),
        workspace_mode=True,  # True
        file_name_explanation=True,  # True
    )
    m = Seasonal(options_)
    if part == 1:
        m.part1()  # first this part should run and refresh data
    else:
        m.part2()  # after first run is complete this part should run and collect results
        # according to preferences


def m1(part=1):
    """1"""
    # demetra_source_folder = r"C:\Users\ppdsppe\PycharmProjects\testevds\some_demetra_folder" # TESTING_FOLDER  # r"../test_evds\source"
    demetra_source_folder = (
        r"C:\Users\ppdsppe\PycharmProjects\testevds\demetra_folder_source"
    )
    local_folder = r"../testevds/test_out"
    options = Options(java_folder, local_folder, demetra_source_folder)
    seasonal_main(options, part=part)


def m2(part=1):
    """m2"""
    demetra_source_folder = TESTING_FOLDER
    local_folder = r"../test_evds/test_out"
    check_folder(java_folder)
    check_folder(demetra_source_folder)
    check_folder(local_folder)
    # local_folder = r'/Users/sermetpekin/Documents/eseasPri/testevds/test_out'
    options = Options(java_folder, local_folder, demetra_source_folder)
    seasonal_main(options, part=part)


if "__main__" == __name__:
    m1(1)
    m1(2)
    # m2(1)
    # m2(2)
