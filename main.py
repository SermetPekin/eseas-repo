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
        # True creates a workspace folder and copies all demetra files
        workspace_mode=False,  
        # True adds explanations to output file names
        file_name_explanation=True,  
        # Downloads jwsacruncher 
        auto_download=True, 
        # Automatically approve any file replacements without prompting
        auto_approve=True,  
        #special Output filenames . 
        # (can be fullp ath SomeFolder/passengers_combined.xlsx)
        special_names = ["air_passengers_combined.xlsx" , "multi_combined.xlsx" , "multi_Q_combined.xlsx"] , 
        # index for combined excel file True  | False  
        out_index = True,
    )
    seas = Seasonal(options)

    seas.run()


if "__main__" == __name__:
    main()
