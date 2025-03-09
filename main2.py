from eseas import Seasonal
from eseas import Options
import time


def main():
    demetra_source_folder = r"./eseas/data_for_testing/unix"
    java_folder = r"/Users/guest/app/jwsacruncher-2.2.6/bin"
    local_folder = r"./test_out"

    options = Options(
        demetra_source_folder,
        java_folder,
        local_folder,
        result_file_names=(
            "sa",
            "s_f",
            "cal",
        ),
        workspace_mode=True,  # True creates a workspace folder and copies all demetra files
        file_name_explanation=True,  # True adds explanations to output file names 
        java_bin = '/usr/bin' , 
    )
    seas = Seasonal(options)

    seas.part1()
    time.sleep(10)
    seas.part2()


if "__main__" == __name__:
    main()
