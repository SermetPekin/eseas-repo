from eseas import Seasonal
from eseas import Options


def main():
    java_folder = r"../Downloads/jwsacruncher-2.2.5"
    demetra_source_folder = r"./eseas/data_for_testing/unix"
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
        workspace_mode=False,  # True creates a workspace folder and copies all demetra files
        file_name_explanation=True,  # True adds explanations to output file names
        auto_download=True,
        auto_approve=True,  # Automatically approve any file replacements without prompting
    )
    seas = Seasonal(options)

    seas.run()


if "__main__" == __name__:
    main()
