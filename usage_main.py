from eseas import Seasonal, Options
import time


def main():
    # Specify the path to the jwsacruncher bin directory
    java_folder = r"../jwsacruncher-2.2.4/bin"
    demetra_source_folder = r"./demetra_source_folder"
    local_folder = r"./test_out"

    options = Options(
        demetra_source_folder,
        java_folder,
        local_folder,
        result_file_names=("sa", "s_f", "cal"),  # *1
        workspace_mode=True,
        file_name_explanation=True,
    )
    # Note (1)
    # result_file_names see full list of result types from Demetra Components below

    seas = Seasonal(options)

    seas.part1()
    time.sleep(10)
    seas.part2()


if __name__ == "__main__":
    main()
